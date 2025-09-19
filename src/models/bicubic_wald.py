"""
bicubic.py
----------
Bicubic interpolation-based super-resolution for Sentinel-2 imagery
"""

import cv2
import numpy as np
import rasterio


def bicubic_super_resolve(input_path: str, output_path: str):
    """Perform Bicubic upsampling for all bands."""
    with rasterio.open(input_path) as src:
        profile = src.profile
        bands = []

        for i in range(1, src.count + 1):
            band = src.read(i)
            # Scale factor = 2 (40m -> 20m)
            upsampled = cv2.resize(band, (src.width * 2, src.height * 2), interpolation=cv2.INTER_CUBIC)
            bands.append(upsampled)

        bands = np.stack(bands, axis=0)

        profile.update({
            'width': src.width * 2,
            'height': src.height * 2
        })

        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(bands)

    print(f"Bicubic SR output saved to: {output_path}")