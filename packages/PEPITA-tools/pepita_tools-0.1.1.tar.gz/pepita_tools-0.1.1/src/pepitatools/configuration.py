"""
Provide global configuration
"""

# Imports
# Standard Library Imports
import configparser
import os
import pathlib
from typing import Union

# External Imports

# Local Imports

__all__ = ["get_config_setting", "set_config_setting", "read_config"]

_CONFIG_SECTION = "Main"

# Set Default Configuration Options
_CONFIGURATION = {
    "absolute_max_infection": 26249,
    "absolute_min_infection": 431,
    "absolute_max_ototox": 26249,
    "absolute_min_ototox": 431,
    "channel_main_ototox": 1,
    "channel_main_infection": 0,
    "channel_subtr_ototox": 0,
    "channel_subtr_infection": 1,
    "filename_replacement_delimiter": "|",
    "filename_replacement_brightfield_infection": "CH2|CH4",
    "filename_replacement_brightfield_ototox": "CH1|CH4",
    "filename_replacement_mask_infection": "CH2|mask",
    "filename_replacement_mask_ototox": "CH1|mask",
    "filename_replacement_subtr_infection": "CH2|CH1",
    "filename_replacement_subtr_ototox": "CH1|CH2",
    "log_dir": "/path/to/log/dir",
    "keyence_file": None,
}

_DEFAULT_CONFIG_STR = """
[Main]
absolute_max_infection = 26249
absolute_min_infection = 431
absolute_max_ototox = 26249
absolute_min_ototox = 431
channel_main_ototox = 1
channel_main_infection = 0
channel_subtr_ototox = 0
channel_subtr_infection = 1
filename_replacement_delimiter = |
filename_replacement_brightfield_infection = CH2|CH4
filename_replacement_brightfield_ototox = CH1|CH4
filename_replacement_mask_infection = CH2|mask
filename_replacement_mask_ototox = CH1|mask
filename_replacement_subtr_infection = CH2|CH1
filename_replacement_subtr_ototox = CH1|CH2
log_dir = /path/to/log/dir
keyence_lenses_file = /path/to/keyence/file
"""


def get_config_setting(setting):
    return _CONFIGURATION.get(setting, None)


def set_config_setting(setting, value):
    _CONFIGURATION[setting] = value


def read_config(config_file: Union[str, os.PathLike, None] = None) -> None:
    if config_file is None:
        config_file = pathlib.Path(".") / "config.ini"

    parsed_config = configparser.ConfigParser()
    parsed_config.read(str(config_file))

    _CONFIGURATION["absolute_max_infection"] = parsed_config[_CONFIG_SECTION][
        "absolute_max_infection"
    ]
    _CONFIGURATION["absolute_min_infection"] = parsed_config[_CONFIG_SECTION][
        "absolute_min_infection"
    ]
    _CONFIGURATION["absolute_max_ototox"] = parsed_config[_CONFIG_SECTION][
        "absolute_max_ototox"
    ]
    _CONFIGURATION["absolute_min_ototox"] = parsed_config[_CONFIG_SECTION][
        "absolute_min_ototox"
    ]
    _CONFIGURATION["channel_main_ototox"] = parsed_config[_CONFIG_SECTION][
        "channel_main_ototox"
    ]
    _CONFIGURATION["channel_main_infection"] = parsed_config[_CONFIG_SECTION][
        "channel_main_infection"
    ]
    _CONFIGURATION["channel_subtr_ototox"] = parsed_config[_CONFIG_SECTION][
        "channel_subtr_ototox"
    ]
    _CONFIGURATION["channel_subtr_infection"] = parsed_config[_CONFIG_SECTION][
        "channel_subtr_infection"
    ]
    _CONFIGURATION["filename_replacement_delimiter"] = parsed_config[_CONFIG_SECTION][
        "filename_replacement_delimiter"
    ]
    _CONFIGURATION["filename_replacement_brightfield_infection"] = parsed_config[
        _CONFIG_SECTION
    ]["filename_replacement_brightfield_infection"]
    _CONFIGURATION["filename_replacement_brightfield_ototox"] = parsed_config[
        _CONFIG_SECTION
    ]["filename_replacement_brightfield_ototox"]
    _CONFIGURATION["filename_replacement_mask_infection"] = parsed_config[
        _CONFIG_SECTION
    ]["filename_replacement_mask_infection"]
    _CONFIGURATION["filename_replacement_mask_ototox"] = parsed_config[_CONFIG_SECTION][
        "filename_replacement_mask_ototox"
    ]
    _CONFIGURATION["filename_replacement_subtr_infection"] = parsed_config[
        _CONFIG_SECTION
    ]["filename_replacement_subtr_infection"]
    _CONFIGURATION["filename_replacement_subtr_ototox"] = parsed_config[
        _CONFIG_SECTION
    ]["filename_replacement_subtr_ototox"]
    _CONFIGURATION["log_dir"] = parsed_config[_CONFIG_SECTION]["log_dir"]
    # Make sure the keyence_file isn't just the default, if it is set it to None for easier handling elsewhere
    _CONFIGURATION["keyence_lenses_file"] = (
        None
        if (
            parsed_config[_CONFIG_SECTION]["keyence_lenses_file"]
            == "/path/to/keyence/file"
        )
        else parsed_config[_CONFIG_SECTION]["keyence_lenses_file"]
    )
