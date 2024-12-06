from positron_common.common_dump import common_dump
from positron_common.observability.main import track_command_usage

# robbie "dump" command
@track_command_usage("dump")
def dump():
    common_dump()
