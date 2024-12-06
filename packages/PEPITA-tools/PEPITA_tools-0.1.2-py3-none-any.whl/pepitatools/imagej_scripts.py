"""
Functions for writing ImageJ Scripts to provided directory
"""

# Imports
# Standard Library Imports
from __future__ import annotations
import importlib.resources
import os
import pathlib
from typing import Union, Literal

# External Imports

# Local Imports


def write_script(
    scriptname: Literal[
        "openformasking",
        "openformaskingsingle",
        "savefishmask",
        "savefishnullmask",
        "macroize",
    ],
    outdir: Union[str, os.PathLike],
) -> None:
    outdir = pathlib.Path(outdir)  # Convert to a pathlib Path
    scriptname = (
        scriptname.lower()
    )  # Convert to lower to avoid issues of capitalization
    scriptname = scriptname.split(".")[
        0
    ]  # If an extension is provided, just take the script name
    if scriptname == "openformasking":
        target_file = outdir / "OpenForMasking.ijm"
        with importlib.resources.open_text(
            "pepitatools.data", "OpenForMasking.ijm"
        ) as script:
            with open(target_file, "w") as f:
                f.write(script.read())
    elif scriptname == "openformaskingsingle":
        target_file = outdir / "OpenForMaskingSingle.ijm"
        with importlib.resources.open_text(
            "pepitatools.data", "OpenForMaskingSingle.ijm"
        ) as script:
            with open(target_file, "w") as f:
                f.write(script.read())
    elif scriptname == "savefishmask":
        target_file = outdir / "SaveFishMask.ijm"
        with importlib.resources.open_text(
            "pepitatools.data", "SaveFishMask.ijm"
        ) as script:
            with open(target_file, "w") as f:
                f.write(script.read())
    elif scriptname == "savefishnullmask":
        target_file = outdir / "SaveFishNullMask.ijm"
        with importlib.resources.open_text(
            "pepitatools.data", "SaveFishNullMask.ijm"
        ) as script:
            with open(target_file, "w") as f:
                f.write(script.read())
    elif scriptname == "macroize":
        target_file = outdir / "macroize.sh"
        with importlib.resources.open_text("pepitatools.data", "macroize.sh") as script:
            with open(target_file, "w") as f:
                f.write(script.read())
