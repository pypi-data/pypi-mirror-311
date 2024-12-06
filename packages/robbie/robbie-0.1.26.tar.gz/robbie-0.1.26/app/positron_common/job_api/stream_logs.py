import asyncio
import socketio
import nest_asyncio
import json
import time
from rich.prompt import Confirm
from positron_common.env_config import env
from positron_common.exceptions import RobbieException
from positron_common.job_api.terminate_job import terminate_job
from ..cli.console import console, ROBBIE_BLUE
from ..cli.logging_config import logger
from positron_common.cli_args import args as cli_args

my_job_id = None

sio = socketio.AsyncClient(ssl_verify=False)
nest_asyncio.apply() # enabled nested event loops

@sio.event(namespace='/stdout-stream')
async def connect():
    console.print("Connected to your run's log stream!")

@sio.event(namespace='/stdout-stream')
async def message(message: str):
    try:
        log: dict = json.loads(message)
        level_name = log.get('log_level')
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S:%MS", time.gmtime(log.get('timestamp') / 1000))
        message = log.get('message')
        level_string = level_name.ljust(8)
        logger_name = log.get('app_name')

        if level_name == "INFO":
            level_string = f"[green]{level_name}[/green]"
        elif level_name == "DEBUG":
            level_string = f"[blue]{level_name}[/blue]"
        elif level_name == "ERROR":
            level_string = f"[red]{level_name}[/red]"
        elif level_name == "WARNING":
            level_string = f"[yellow]{level_name}[/yellow]"

        formatted_log = f"{logger_name}: {timestamp} {level_string}: {message}"
        console.print(formatted_log)
    except:
        console.print(log['message'], style=ROBBIE_BLUE)

@sio.event(namespace='/stdout-stream')
async def disconnect():
    logger.debug("Disconnecting from the log stream")
    pass

@sio.event(namespace='/stdout-stream')
async def error(err):
    console.print('An error occurred in the streaming process')
    logger.error(err)

async def start_stream(job_id: str):
    custom_headers = {
        "PositronAuthToken": env.USER_AUTH_TOKEN,
        "PositronJobId": job_id
    }
    await sio.connect(env.SOCKET_IO_DOMAIN, headers=custom_headers, socketio_path=env.SOCKET_IO_PATH)
    # TODO: I don't think we want to actually do this long term.
    try:
        await sio.wait()
    except asyncio.exceptions.CancelledError as error:
        # keyboard interrupt
        global my_job_id
        if my_job_id:
            if Confirm.ask("Interrupt received, do you want to terminate the run?", default=False):
                console.print("[yellow]Terminating run...[/yellow]")
                terminate_job(my_job_id, "User interrupted")
                # kind of a kluge, but we need to set this to false so it doesn't download results
                cli_args.download = False
            else:
                console.print("[yellow]Streaming ended. Please monitor run progress in the portal.[/yellow]")  
    finally:
        logger.debug("Done waiting...")

def start_stdout_stream(job_id: str):
    global my_job_id
    my_job_id = job_id 
    try:
        # Start the stream
        asyncio.get_event_loop().run_until_complete(start_stream(job_id))
    except Exception as error:
        raise RobbieException(error)


