import signal
import json
import time
import sentry_sdk
from rich.prompt import Confirm
from positron_common.aws.s3_presigned_handler import S3PresignedHandler
from positron_common.deployment.stored_function import StoredFunction
from positron_common.utils import get_default_workspace_dir, _exit_by_mode, SUCCESS, FAILURE, _nb
from positron_common.exceptions import RemoteFunctionException, RemoteCallException
from positron_common.config import PositronJob
from positron_common.enums import JobStatus, failed_job_statuses
from positron_common.job_api.stream_logs import start_stdout_stream
from positron_common.job_api.get_job import get_job_status, get_job
from positron_common.job_api.start_job import start_job
from positron_common.job_api.terminate_job import terminate_job
from positron_common.job_api.create_job import create_job
from positron_common.cli_args import args as cli_args
from positron_common.compression import create_workspace_tar, check_workspace_dir
from positron_common.env_config import env
from positron_common.user_config import user_config
from positron_common.constants import temp_path
from positron_common.cli.console import console, ROBBIE_BLUE
from positron_common.cli.logging_config import logger
from positron_common.job_api.terminate_job import terminate_job
from positron_common.print import print_robbie_configuration_banner, print_job_details_banner, print_known_error, print_job_complete_banner

# TODO: update env var to just be base url
PORTAL_BASE = env.API_BASE.rstrip('/api')

# global for signal handler
job = None

class Deploy:
    @staticmethod
    def remote_function_deploy(func, args, kwargs, job_config: PositronJob):
        global job
        signal.signal(signal.SIGINT, handle_sigint)
        try:
            # TODO: lots of this code is the same as the other `deploy` file, need to consolidate
            logger.debug(f'Job Config: {job_config}')
            job_config.validate_values()
            logger.debug(f'Runtime Environment: {job_config.create_runtime_env()}')

            job = create_job(job_config)
            print_robbie_configuration_banner(job, job_config)
            logger.debug(f"Created Run Details: {json.dumps(job, indent=2)}")

            # prompt the user if they don't pass the -y option
            if not cli_args.skip_prompts:
                user_input = input("Run with these settings? (Y/n)")
                if not user_input.lower() in ["", "yes", "y", "Yes", "Y"]:
                    terminate_job(job["id"], "User declined from CLI")
                    console.print("[yellow]See you soon![/yellow]")
                    return

            console.print("[bold]Local Machine: [/bold]", style=ROBBIE_BLUE)    
            workspace_dir = (job_config.workspace_dir if job_config.workspace_dir else get_default_workspace_dir())
            logger.debug(f"Workspace Directory: {workspace_dir}")

            if not check_workspace_dir(workspace_dir):
                console.print("[yellow]See you soon![/yellow]")
                terminate_job(job["id"], "User declined run from CLI")
                _exit_by_mode(SUCCESS)
                return

            # Create stored function from func and arguments
            stored_function = StoredFunction(func, args, kwargs)
            stored_function.set_job_id(job['id'])
            stored_function.serialize_function()
            stored_function.create_function_metadata(hmac_key=user_config.user_auth_token)
            file_count = create_workspace_tar(workspace_dir=workspace_dir)
            console.print("[green]✔[/green] Packaged up workspace artifacts...(1 of 3)", style=ROBBIE_BLUE)

            if file_count == 0:
                if not Confirm.ask("No files were found in the workspace directory. Would you like to continue anyway?", default=True):
                    console.print("[yellow]See you soon![/yellow]")
                    terminate_job(job["id"], "User declined run from CLI")
                    _exit_by_mode(SUCCESS)
                    return

            stored_function.upload_to_s3()
            S3PresignedHandler.upload_file_to_job_folder(f"{temp_path}/{env.COMPRESSED_WS_NAME}", job['id'], env.COMPRESSED_WS_NAME)
            console.print("[green]✔[/green] Uploaded compressed workspace to Robbie...(2 of 3)", style=ROBBIE_BLUE)

            if cli_args.create_only:
                console.print(f"[green]✔[/green] Run created successfully. (3 of 3)")
                console.print(f"JOB_ID: {job.get('id')}")
                _exit_by_mode(SUCCESS)

                return

            # start job
            runtime_env = job_config.create_runtime_env()
            logger.debug(f"Runtime Environment: {runtime_env}")
            start_job(job_id=job['id'], data=runtime_env)
            console.print("[green]✔[/green] Submitted run to Robbie...(3 of 3)", style=ROBBIE_BLUE)
            
            start = time.perf_counter()
            print_job_details_banner(job)
            console.print(f"You can also monitor run status in the Robbie portal at: {PORTAL_BASE}/portal/app/my-runs?jobId={job['id']}\n", style=ROBBIE_BLUE)

            # Start standard output stream if option selected
            console.print("Waiting for remote job to finish...", style=ROBBIE_BLUE)
            if cli_args.stream_stdout:
                start_stdout_stream(job['id'])

            #  Wait for the remote function run to finnish
            last_status_change = "Starting..."

            while True:
                job = get_job_status(job['id'])
                if job['status'] == JobStatus.complete:
                    console.print(f"[green]✔[/green] Done! Now processing results...")
                    result, exception = stored_function.load_and_validate_results(hmac_key=user_config.user_auth_token)
                    console.print("Passing back result.")
                    if exception is not None:
                        raise RemoteFunctionException(exception)
                    else:
                        return  result
                elif job['status'] == JobStatus.failed or job['status'] == JobStatus.execution_error:
                    raise RemoteCallException(user_friendly_message="The remote run has failed, please check job output logs for further details!")
                elif job['status'] == JobStatus.terminated:
                    # users terminated
                    break
                elif job['status'] != last_status_change:
                    # there has been a status change
                    time1 = time.strftime("%H:%M:%S")
                    console.print(f"\t{time1}: {job['status']}")
                    last_status_change = job['status']
                time.sleep(5)
            # get the job info a final time
            job = get_job(job['id'])
            print_job_complete_banner(job, start)
            # print details if error for debugging.
            if job['status'] in failed_job_statuses:
                console.print(f"We are sorry that your job has run in to an issue. If you continue to have issues, please contact support@robbie.run and provide the following traceback.\nTrace ID: {sentry_sdk.get_current_span().trace_id}")
            _exit_by_mode(SUCCESS)

            
        except RemoteCallException as e:
            """For known errors we dont print exceptions, we just print the user friendly message"""
            print_known_error(e)
            _exit_by_mode(FAILURE)
        except RemoteFunctionException as e:
            """
                When the result of a remote function call is an Exception being raised
                this is how we let the deserialized exception bubble up back to the client side
            """
            raise e.rf_exception
        except Exception:
            console.print_exception()

def handle_sigint(signum, frame):
    global job
    if Confirm.ask("Interrupt received, do you want to terminate the run?", default=False):
        console.print("[yellow]Terminating run...[/yellow]")
        terminate_job(job['id'], "User interrupted")
