"""
atprk.py
--------
Wrapper to run ATPRK methods (MSsharpen or PANsharpen) via MATLAB from Python.

Requirements:
- MATLAB must be installed locally
- MATLAB command must be accessible in the system PATH
"""

import os
import subprocess
import sys


def atprk_super_resolve(mode: str, input_path: str, output_path: str, matlab_path="matlab"):
    """
    Run ATPRK method in MATLAB.

    Parameters
    ----------
    mode : str
        'ms' for ATPRK_MSsharpen or 'pan' for ATPRK_PANsharpen
    input_path : str
        Path to input degraded image
    output_path : str
        Path to save output SR image
    matlab_path : str
        Directory where atprk_main.m is located
    """
    if mode not in ["ms", "pan"]:
        raise ValueError("mode must be either 'ms' or 'pan'")

    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    matlab_path = os.path.abspath(matlab_path)

    matlab_cmd = f"""
    try
        addpath('{matlab_path}');
        atprk_main('{mode}', '{input_path}', '{output_path}');
        exit;
    catch ME
        disp(getReport(ME));
        exit(1);
    end
    """

    
    command = [
    "/Applications/MATLAB_R2025b.app/bin/matlab", 
    "-nodisplay",
    "-nosplash",
    "-r",
    matlab_cmd
]

    print(f"Running ATPRK ({mode}) in MATLAB...")

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error running ATPRK:")
        print(result.stderr)
        sys.exit(1)

    print(result.stdout)
    print(f"ATPRK ({mode}) SR output saved to: {output_path}")