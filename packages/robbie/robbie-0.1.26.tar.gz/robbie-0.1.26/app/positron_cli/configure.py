from positron_common.cli.console import console
from positron_common.cli.interactive import prompt_and_build_positron_job_config
from positron_common.constants import JOB_CONF_YAML_PATH
from positron_common.observability.main import track_command_usage

@track_command_usage("configure")
def configure() -> None:
    """
    Build a Robbie job configure file (job_config.yaml) interactively.

    """
    print("Please follow the prompts to build a 'job_config.yaml' in your current directory.")
    print("Values in brackets [] are default, use the <tab> key to see a menu of options.\n")
    
    cfg = prompt_and_build_positron_job_config()

    if cfg:
        cfg.write_to_file(filename=JOB_CONF_YAML_PATH)
        console.print(f"[green]Successfully wrote config file {JOB_CONF_YAML_PATH}'")
        console.print("File contents:")
        with open(JOB_CONF_YAML_PATH, 'r') as f:
            print(f.read())





    
