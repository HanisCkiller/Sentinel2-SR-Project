"""
pca.py
------
PCA-based fusion for Sentinel-2 imagery
"""

import rasterio
import numpy as np
from sklearn.decomposition import PCA


def pca_super_resolve(input_path: str, output_path: str):
    """
    Perform PCA-based fusion on multispectral data.
    Sentinel-2 bands assumed to be ordered [B5, B6, B7, B8, B8A, B11, B12]
    """
    with rasterio.open(input_path) as src:
        profile = src.profile
        data = src.read()

        # Flatten for PCA
        h, w = data.shape[1], data.shape[2]
        reshaped = data.reshape(data.shape[0], -1).T  # shape: (pixels, bands)

        pca = PCA(n_components=data.shape[0])
        pca_result = pca.fit_transform(reshaped)

        fused = pca_result.T.reshape(data.shape)

        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(fused.astype(profile['dtype']))

    print(f"PCA fusion output saved to: {output_path}")