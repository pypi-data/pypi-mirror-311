from pydantic import BaseModel
from typing import List, Optional
from positron_common.cli.console import console, print_boxed_messages
from rich.text import Text

class PositronCLIArgs(BaseModel):
    """
    Positron CLI command line arguments.
    """
    is_init: bool = False
    name: Optional[str] = None
    local: bool = False
    deploy: bool = False
    stream_stdout: bool = False
    job_args: Optional[List[str]] = None
    skip_prompts: bool = False
    monitor_status: bool = False
    commands_to_run: Optional[str] = None
    interactive: bool = False
    create_only: bool = False
    results_from_job_id: str = ""
    download: Optional[str] = None
    local_path: Optional[str] = None
    auto_capture_deps: bool = False


    def init(self,
        name: Optional[str] = None,
        local: bool = False,
        deploy: bool = False,
        stream_stdout: bool = False,
        job_args: Optional[List[str]] = None,
        skip_prompts: bool = False,
        monitor_status: bool = False,
        commands_to_run: Optional[str] = None,
        interactive: bool = False,
        create_only: bool = False,
        results_from_job_id: str = "",
        download: Optional[str] = None,
        local_path: Optional[str] = None,
        auto_capture_deps: bool = False
    ):
        if self.is_init:
            raise ValueError('CLI Args already initialized')
        
        self.name = name
        self.local = local
        self.deploy = deploy
        self.stream_stdout = stream_stdout
        self.job_args = job_args
        self.is_init = True
        self.skip_prompts=skip_prompts
        self.monitor_status=monitor_status
        self.commands_to_run = commands_to_run
        self.interactive = interactive
        self.create_only = create_only
        self.results_from_job_id = results_from_job_id
        self.download = download
        self.local_path = local_path
        self.auto_capture_deps = auto_capture_deps

    def to_string(self, include_title: bool = False) -> str:
        message = f"""- name: {self.name}
- local: {self.local}
- deploy: {self.deploy}
- stream_stdout: {self.stream_stdout}
- job_args: {self.job_args}
- skip_prompts: {self.skip_prompts}
- monitor_status: {self.monitor_status}
- commands_to_run: {self.commands_to_run}
- interactive: {self.interactive}
- create_only: {self.create_only}
- results_from_job_id: {self.results_from_job_id}
- download: {self.download}
- local_path: {self.local_path}
- auto_capture_deps: {self.auto_capture_deps}
- is_init: {self.is_init}"""
        
        if include_title:
            return f"========== CLI Arguments (args) ==========\n{message}"
        else:
            return message

    


#
# Export global (singleton)
#
args = PositronCLIArgs()
"""
Global CLI arguments singleton, make sure you call init() before using it.
"""
