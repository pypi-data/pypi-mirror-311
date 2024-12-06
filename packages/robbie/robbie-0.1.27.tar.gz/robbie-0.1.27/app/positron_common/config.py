from pydantic import BaseModel, field_validator
from typing import Dict, Optional, List, Union
import os
import copy
import yaml
import re
from yaml import dump
from enum import Enum
from positron_common.utils import get_version, _current_python_version
from positron_common.exceptions import RobbieException
from positron_common.user_config import user_config, REMOTE_FUNCTION_SECRET_KEY_NAME
from positron_common.constants import JOB_CONF_YAML_PATH, RUNTIME_ENV_PREFIX
from positron_common.cli.logging_config import logger
from positron_common.enums import JobRunType

class PositronJob(BaseModel):
    """
    The Job details as defined in the `python_job` from the `job_config.yaml` file.
    """
    name: Optional[str] = None
    funding_group_id: Optional[str] = None
    environment_id: Optional[str] = None
    image: Optional[str] = None # this is not written to the config file
    job_type: Optional[JobRunType] = None
    commands: Optional[List[str]] = None
    workspace_dir: Optional[str] = None
    max_tokens: Optional[int] = None
    max_time: Optional[int] = None
    env: Optional[Dict[str, str]] = None
    dependencies: Optional[str] = None
    conda_env: Optional[str] = None
    # below are values not writtent to the config file
    cluster: Optional[str] = None
    python_version: Optional[str] = _current_python_version()
    robbie_sdk_version: Optional[str] = get_version()
    image_selection: Optional[str] = None
    funding_selection: Optional[str] = None
    environment_selection: Optional[str] = None

    @field_validator('commands', mode='after')
    def ensure_non_empty(cls, commands):
        return commands if len(commands) else None

    @field_validator('env', mode='after')
    def ensure_env_is_dict(cls, v):
        if isinstance(v, dict):
            return v
        raise ValueError('env must be a dictionary')

    @field_validator('max_time', mode='before')
    def ensure_max_time_is_int(cls, max_time: Union[int, str, None]) -> Union[int, None]:
        return cls._max_time_to_minutes(max_time)

    @field_validator('max_tokens', mode='before')
    def ensure_max_tokens_is_int(cls, max_tokens: Union[int, str, None]) -> Union[int, None]:
        return cls._max_tokens_to_int(max_tokens)

    def create_runtime_env(self) -> Dict[str, str]:
        """
        Used on the client side to create the prefixed runtime environment variables
        to avoid conflicts with the local environment variables.
        """
        env: Dict[str, str] = {}
        # without env_prefix?? yes, but maybe not in this file, but part of the deploy.py file.
        env[REMOTE_FUNCTION_SECRET_KEY_NAME] = user_config.user_auth_token
        if not self.env:
            return env
        for key, value in self.env.items():
            if (value == ""):
                env_var = os.environ.get(key)
                if env_var is None:
                    raise ValueError(f"The env prop {key} is unset inside job_config.yaml and also unset in local env vars. Please set this value.")
                env[f'{RUNTIME_ENV_PREFIX}{key}'] = env_var
            else:
                env[f'{RUNTIME_ENV_PREFIX}{key}'] = value
        return env

    @staticmethod
    def _max_time_to_minutes(max_time: Union[int, str, None]) -> Union[int, None]:
        if not max_time:
            return None
        if isinstance(max_time, int):
            return max_time
        matches = re.search(r'^(\d+):(\d{2})$', max_time)
        if matches is None:
            raise ValueError(f'Invalid Job Config: Field "max_time" ({max_time}) must have the format "HH:MM" or be a positive integer')
        try:
            hours = int(matches.group(1))
            minutes = int(matches.group(2))
        except:
            raise ValueError(f'Invalid Job Config: Field "max_time" ({max_time}) must have the format "HH:MM" or be a positive integer')
        if minutes >= 60:
            raise ValueError('Invalid Job Config: Field "max_time" ({max_time}) has invalid minutes! Must be 0 <= minutes < 60!')
        return hours * 60 + minutes

    @staticmethod
    def _max_tokens_to_int(max_tokens: Union[int, str, None]) -> Union[int, None]:
        if not max_tokens:
            return None
        if isinstance(max_tokens, int):
            return max_tokens
        try:
            max_tokens = int(max_tokens)
        except:
            raise ValueError(f'Invalid Job Config: "max_tokens" ({max_tokens}) needs to be a positive integer.')
        if max_tokens <= 0:
            raise ValueError(f'Invalid Job Config: "max_tokens" ({max_tokens}) needs to be a positive integer.')
        return max_tokens

    def validate_values(self) -> None:
        errors = []
        if self.env and not validate_env_vars(self.env):
            errors.append('At least one of the environment variables provided is invalid')
        if errors:
            raise RobbieException(f'Invalid configuration. Errors: {errors}')
        return None
    
    def namestr(self, obj, namespace):
        return [name for name in namespace if namespace[name] is obj]

    def to_string(self, title: str = 'None'):
        message = f"""
- python_version: {self.python_version}
- robbie_sdk_version: {self.robbie_sdk_version}
- name: {self.name}
- funding_group_id: {self.funding_group_id}
    - funding_selection: {self.funding_selection}
- environment_id: {self.environment_id}
    - environment_selection: {self.environment_selection}
- image: {self.image}
    - image_selection: {self.image_selection}
- cluster: {self.cluster}
- dependencies: {self.dependencies}
- conda_env: {self.conda_env}
- job_type: {self.job_type}
- workspace_dir: {self.workspace_dir}
- max_tokens: {self.max_tokens}
- max_time: {self.max_time}
- env: {self.env}
- commands: {self.commands}"""

        if title:
            return f"========== {title} ==========\n{message}"
        else:
            return message
        

class PositronJobConfig(BaseModel):
    """
    The `job_config.yaml` schema class.
    """
    version: float
    python_job: PositronJob

    def write_to_file(this, filename: str = JOB_CONF_YAML_PATH):
        copy_of_config = copy.deepcopy(this)
        del copy_of_config.python_job.robbie_sdk_version
        del copy_of_config.python_job.python_version
        del copy_of_config.python_job.cluster
        del copy_of_config.python_job.image_selection
        del copy_of_config.python_job.funding_selection
        del copy_of_config.python_job.environment_selection
        config_dict = copy_of_config.model_dump(
            exclude_unset=True
        )
        config_dict = convert_enums_to_values(config_dict)

        with open(filename, 'w') as file:
            file.write(dump(config_dict, sort_keys=False))


def convert_enums_to_values(d: dict) -> dict:
    """
    Converts Enum type values in the dictionary to their respective values.
    """
    for key, value in d.items():
        if isinstance(value, Enum):
            d[key] = value.value
        elif isinstance(value, dict):
            convert_enums_to_values(value)
    return d


def is_valid_key_value(keyvalue):
    """
    Validate that the key-value contains only alphanumeric characters, dashes, and underscores, and has no spaces.
    """
    return bool(re.match(r'^[\w-]+$', keyvalue))

def validate_env_vars(env_dict):
    """
    Validate the environment variables from the given dictionary.
    """
    valid = True
    for key, value in env_dict.items():
        if not is_valid_key_value(key):
            print(f"Invalid key (contains invalid characters or spaces): {key}")
            valid = False
        if value != "" and not is_valid_key_value(value):
            print(f"Invalid value (contains invalid characters or spaces): {value}")
            valid = False
    return valid

def merge_config(base_config: PositronJob, override_config: PositronJob) -> PositronJob:
    """
    Makes it easy to merge decorator configs on top of the YAML config.
    """
    update_data = override_config.dict(exclude_unset=True)
    updated_config = base_config.copy(update=update_data)
    return updated_config


def invalid_yaml_keys(yaml_job_keys) -> bool:
    """
    Validates the yaml keys against the PositronJob class.
    """
    # Get only attributes from PositronJob
    base_attrs = set(dir(BaseModel))
    derived_attrs = set(dir(PositronJob()))
    additional_attrs = derived_attrs - base_attrs

    # Exclude built-in attributes (e.g., __init__, __module__)
    validKeys = [attr for attr in additional_attrs if not attr.startswith('__')]
    
    weHaveInvalidYamlKeys = False
    for key in yaml_job_keys:
        if key not in validKeys:
            weHaveInvalidYamlKeys = True
            raise RobbieException(f'Error: wrong param in the job_config.yaml: -> {key}')

    return weHaveInvalidYamlKeys

def parse_job_config(config_path: str = 'job_config.yaml') -> Optional[PositronJob]:
    """
    Load the job configuration from the `job_config.yaml` file if it exists
    """
    
    if not os.path.exists(config_path):
        logger.debug('job_config.yaml file not found')
        return None
    
    try:
        # this happens sometimes and it causes the job to fail
        if os.path.getsize(config_path) == 0:
            logger.debug('job_config.yaml file is empty')
            return None
        with open(config_path, 'r') as job_config_file:
            job_config_dict = yaml.safe_load(job_config_file)
            job = job_config_dict["python_job"]
            if invalid_yaml_keys(job.keys()):
                return None
            job_config = PositronJobConfig(**job_config_dict)
            return job_config.python_job
    except Exception as e:
        print(f'Error loading job configuration! {str(e)}')
        return None

# if main then load and validate
if __name__ == "__main__":
    job_config = parse_job_config()
    if job_config:
        job_config.validate_values()
        print(job_config)
