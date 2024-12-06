import sys
import os
import subprocess
from positron_common.cli.console import console, print_boxed_messages
from positron_common.build_env import build_env
from positron_common.utils import get_version
from positron_common.env_defaults import current
from positron_common.env_config import env
from positron_common.user_config import user_config
from positron_common.cli_args import args

def common_dump():
    console.print("Dumping Robbie local environment...")
    print_boxed_messages(sys.executable, "Python executable (sys.executable)")
    print_boxed_messages(os.__file__, "Python executable (os.__file__)")
    print_boxed_messages(get_version(), "Robbie Python SDK version - importlib.metadata.version('robbie')")
    result = subprocess.run(["pip", "show", "robbie"], capture_output=True, text=True)
    print_boxed_messages(result.stdout, "Robbie SDK version (% pip show robbie)")
    result = subprocess.run(["pip", "list"], capture_output=True, text=True)
    print_boxed_messages(result.stdout, "Installed Python Packages (% pip list)")
    if os.path.exists("./requirements.txt"):
        try:
            with open("./requirements.txt", 'r') as file:
                # Read the content of the file
                file_content = file.read()
                print_boxed_messages(file_content, "./requirements.txt")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    print_boxed_messages(str(build_env), "build_env")
    print_boxed_messages(env.to_string(), "EnvConfig (env)")
    print_boxed_messages(current.to_string(), "EnvDefaults (current)")
    print_boxed_messages(user_config.to_string(), "User Config (user_config)")     
    print_boxed_messages(args.to_string(), "CLI Arguments (args)")

def dump_data():
    """All the same data as common_dump, but returned as a dict"""
    return {
        "Python executable (sys.executable)": sys.executable,
        "Python executable (os.__file__)": os.__file__,
        "Robbie Python SDK version - importlib.metadata.version('robbie')": get_version(),
        "Robbie SDK version (% pip show robbie)": subprocess.run(["pip", "show", "robbie"], capture_output=True, text=True).stdout,
        "Installed Python Packages (% pip list)": subprocess.run(["pip", "list"], capture_output=True, text=True).stdout,
        "./requirements.txt": open("./requirements.txt", 'r').read() if os.path.exists("./requirements.txt") else None,
        "build_env": str(build_env),
        "EnvConfig (env)": env.to_string(),
        "EnvDefaults (current)": current.to_string(),
        "User Config (user_config)": user_config.to_string(),
        "CLI Arguments (args)": args.to_string(),
    }