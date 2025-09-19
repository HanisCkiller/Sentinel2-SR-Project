"""
Metric utilities for PSNR, SSIM, SAM, and RMSE.
Fill in with your implementations or wrap existing libraries.
"""
from typing import Tuple
import numpy as np

def rmse(a: np.ndarray, b: np.ndarray) -> float:
    diff = (a.astype(np.float64) - b.astype(np.float64)).ravel()
    return float(np.sqrt(np.mean(diff**2)))

def psnr(a: np.ndarray, b: np.ndarray, max_val: float = None) -> float:
    if max_val is None:
        max_val = max(a.max(), b.max(), 1.0)
    mse = ((a.astype(np.float64) - b.astype(np.float64)) ** 2).mean()
    if mse == 0:
        return float("inf")
    return 20 * np.log10(max_val) - 10 * np.log10(mse)

# TODO: add SSIM, SAM or import from skimage
