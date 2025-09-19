"""
brovey.py
---------
Brovey transform-based fusion for Sentinel-2 imagery
"""

import rasterio
import numpy as np


def brovey_super_resolve(input_path: str, output_path: str):
    """
    Perform Brovey fusion on multispectral data.
    Sentinel-2 bands assumed to be ordered [B5, B6, B7, B8, B8A, B11, B12]
    """
    with rasterio.open(input_path) as src:
        profile = src.profile
        data = src.read()

        # Assume last band (B8) is high-resolution reference
        ref_band = data[3, :, :]  # B8

        fused_bands = []
        for i in range(data.shape[0]):
            if i == 3:
                fused_bands.append(ref_band)
            else:
                sum_rgb = np.sum(data[[0, 1, 2], :, :], axis=0) + 1e-6
                fused = (data[i] * ref_band) / sum_rgb
                fused_bands.append(fused)

        fused_bands = np.stack(fused_bands, axis=0)

        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(fused_bands.astype(profile['dtype']))

    print(f"Brovey fusion output saved to: {output_path}")