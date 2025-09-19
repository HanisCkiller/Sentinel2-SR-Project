"""
run_experiments.py
------------------
Unified command-line interface for running different super-resolution methods
on Sentinel-2 imagery.

Supported methods:
- Bicubic interpolation (Python)
- Brovey fusion (Python)
- PCA-based fusion (Python)
- Random Forest regression (Python)
- ATPRK (MATLAB, with MS and PAN modes)
"""

import argparse
import os
import sys

# === Import Python-based methods ===
from src.models.bicubic import bicubic_super_resolve
from src.models.brovey import brovey_super_resolve
from src.models.pca import pca_super_resolve
from src.models.random_forest import rf_super_resolve

# === Import MATLAB-based method wrapper ===
from src.models.atprk import atprk_super_resolve


# Dictionary mapping method name to callable
METHODS = {
    "bicubic": bicubic_super_resolve,
    "brovey": brovey_super_resolve,
    "pca": pca_super_resolve,
    "rf": rf_super_resolve,
    # ATPRK handled separately since it has an extra parameter
}


def main():
    parser = argparse.ArgumentParser(description="Run Sentinel-2 super-resolution methods.")

    # Core parameters
    parser.add_argument("--method", type=str, required=True,
                        choices=["bicubic", "brovey", "pca", "rf", "atprk", "all"],
                        help="Super-resolution method to run.")
    parser.add_argument("--input", type=str, required=True, help="Path to input GeoTIFF file.")
    parser.add_argument("--output", type=str, help="Output path for single method.")
    parser.add_argument("--output_dir", type=str, default="results/",
                        help="Directory to save outputs when running multiple methods.")

    # ATPRK-specific parameter
    parser.add_argument("--atprk-mode", type=str, default="ms",
                        choices=["ms", "pan"],
                        help="ATPRK mode: 'ms' for multi-spectral or 'pan' for pan-sharpening. Default is 'ms'.")

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    # Ensure output directory exists
    if args.method == "all" or args.method == "atprk":
        os.makedirs(args.output_dir, exist_ok=True)

    # Run selected method(s)
    if args.method == "all":
        # Run all Python methods + both ATPRK modes
        for name, func in METHODS.items():
            out_path = os.path.join(args.output_dir, f"{name}_output.tif")
            print(f"\nRunning {name}...")
            func(args.input, out_path)

        # Run both ATPRK modes
        print("\nRunning ATPRK (MS mode)...")
        atprk_super_resolve("ms", args.input,
                            os.path.join(args.output_dir, "atprk_ms_output.tif"))

        print("\nRunning ATPRK (PAN mode)...")
        atprk_super_resolve("pan", args.input,
                            os.path.join(args.output_dir, "atprk_pan_output.tif"))

    elif args.method == "atprk":
        if not args.output:
            raise ValueError("Output path is required when running ATPRK alone.")
        print(f"\nRunning ATPRK in {args.atprk_mode} mode...")
        atprk_super_resolve(args.atprk_mode, args.input, args.output)

    else:
        # Run a single Python method
        if not args.output:
            raise ValueError("Output path is required when running a single method.")
        METHODS[args.method](args.input, args.output)


if __name__ == "__main__":
    main()