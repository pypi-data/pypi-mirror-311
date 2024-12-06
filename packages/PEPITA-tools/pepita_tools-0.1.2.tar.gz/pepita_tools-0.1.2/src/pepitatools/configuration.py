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
    "keyence_lenses_file": None,
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
    else:
        config_file = pathlib.Path(config_file)
    # If the config file isn't created, keep going to try and use config options passed in from the
    # command line
    if not config_file.exists():
        return None

    parsed_config = configparser.ConfigParser()
    parsed_config.read(str(config_file))

    # Update the config, falling back on the default
    global _CONFIGURATION
    _CONFIGURATION["absolute_max_infection"] = parsed_config.get(
        _CONFIG_SECTION, "absolute_max_infection", fallback=26249
    )
    _CONFIGURATION["absolute_min_infection"] = parsed_config.get(
        _CONFIG_SECTION, "absolute_min_infection", fallback=431
    )
    _CONFIGURATION["absolute_max_ototox"] = parsed_config.get(
        _CONFIG_SECTION, "absolute_max_ototox", fallback=26249
    )
    _CONFIGURATION["absolute_min_ototox"] = parsed_config.get(
        _CONFIG_SECTION, "absolute_min_ototox", fallback=431
    )
    _CONFIGURATION["channel_main_ototox"] = parsed_config.get(
        _CONFIG_SECTION, "channel_main_ototox", fallback=1
    )
    _CONFIGURATION["channel_main_infection"] = parsed_config.get(
        _CONFIG_SECTION, "channel_main_infection", fallback=0
    )
    _CONFIGURATION["channel_subtr_ototox"] = parsed_config.get(
        _CONFIG_SECTION, "channel_subtr_ototox", fallback=0
    )
    _CONFIGURATION["channel_subtr_infection"] = parsed_config.get(
        _CONFIG_SECTION, "channel_subtr_infection", fallback=1
    )
    _CONFIGURATION["filename_replacement_delimiter"] = parsed_config.get(
        _CONFIG_SECTION, "filename_replacement_delimiter", fallback="|"
    )
    _CONFIGURATION["filename_replacement_brightfield_infection"] = parsed_config.get(
        _CONFIG_SECTION,
        "filename_replacement_brightfield_infection",
        fallback="CH2|CH4",
    )
    _CONFIGURATION["filename_replacement_brightfield_ototox"] = parsed_config.get(
        _CONFIG_SECTION, "filename_replacement_brightfield_ototox", fallback="CH1|CH4"
    )
    _CONFIGURATION["filename_replacement_mask_infection"] = parsed_config.get(
        _CONFIG_SECTION, "filename_replacement_mask_infection", fallback="CH2|mask"
    )
    _CONFIGURATION["filename_replacement_mask_ototox"] = parsed_config.get(
        _CONFIG_SECTION, "filename_replacement_mask_ototox", fallback="CH1|mask"
    )
    _CONFIGURATION["filename_replacement_subtr_infection"] = parsed_config.get(
        _CONFIG_SECTION, "filename_replacement_subtr_infection", fallback="CH2|CH1"
    )
    _CONFIGURATION["filename_replacement_subtr_ototox"] = parsed_config.get(
        _CONFIG_SECTION, "filename_replacement_subtr_ototox", fallback="CH1|CH2"
    )
    _CONFIGURATION["log_dir"] = parsed_config.get(
        _CONFIG_SECTION, "log_dir", fallback="/path/to/log/dir"
    )
    _CONFIGURATION["keyence_lenses_file"] = parsed_config.get(
        _CONFIG_SECTION, "keyence_file", fallback=None
    )

    # Make sure the keyence_file isn't just the default, if it is set it to None for easier handling elsewhere
    if _CONFIGURATION["keyence_lenses_file"] == "/path/to/keyence/file":
        _CONFIGURATION["keyence_lenses_file"] = None
