from positron_common.utils import get_version
from positron_common.build_env import build_env
from positron_common.env_defaults import current
from positron_common.cli.console import console
from positron_common.observability.main import track_command_usage

@track_command_usage("version")
def version():
    console.print(f"Robbie SDK Version: {get_version()}, build_env: {build_env.value}, current_env: {current.name}")
