"""
prepare_data.py
--------------
Prepare Sentinel-2 data by artificial degradation:
- Downsample 20m bands to 40m
- Upsample back to 20m for SR input
保持原始波段顺序与地理信息
"""

import rasterio
from rasterio.enums import Resampling
import numpy as np


def degrade_to_40m(input_path: str, degraded_path: str):
    """Downsample Sentinel-2 image from 20m to 40m."""
    with rasterio.open(input_path) as src:
        profile = src.profile
        profile.update({
            'width': src.width // 2,
            'height': src.height // 2,
            'transform': src.transform * src.transform.scale(2, 2)
        })

        data = src.read(
            out_shape=(src.count, src.height // 2, src.width // 2),
            resampling=Resampling.average
        )

        with rasterio.open(degraded_path, 'w', **profile) as dst:
            dst.write(data)

    print(f"Degraded image saved to: {degraded_path}")


def upsample_to_20m(input_path: str, upsampled_path: str):
    """Upsample degraded 40m image back to 20m using bilinear interpolation."""
    with rasterio.open(input_path) as src:
        profile = src.profile
        profile.update({
            'width': src.width * 2,
            'height': src.height * 2,
            'transform': src.transform * src.transform.scale(0.5, 0.5)
        })

        data = src.read(
            out_shape=(src.count, src.height * 2, src.width * 2),
            resampling=Resampling.bilinear
        )

        with rasterio.open(upsampled_path, 'w', **profile) as dst:
            dst.write(data)

    print(f"Upsampled image saved to: {upsampled_path}")