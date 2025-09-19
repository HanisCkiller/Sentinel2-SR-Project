"""
random_forest.py
----------------
Random Forest-based super-resolution for Sentinel-2 imagery
"""

import rasterio
import numpy as np
from sklearn.ensemble import RandomForestRegressor


def rf_super_resolve(input_path: str, output_path: str, n_estimators=100):
    """
    Perform Random Forest regression for SR.
    """
    with rasterio.open(input_path) as src:
        profile = src.profile
        data = src.read()

        # Prepare features and target
        h, w = data.shape[1], data.shape[2]
        features = data[:-1].reshape(data.shape[0] - 1, -1).T  # use all but last band as features
        target = data[-1].reshape(-1)  # last band as target

        # Train RF
        rf = RandomForestRegressor(n_estimators=n_estimators, n_jobs=-1)
        rf.fit(features, target)

        # Predict high-resolution band
        predicted = rf.predict(features).reshape(h, w)

        # Replace last band
        output_data = data.copy()
        output_data[-1] = predicted

        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(output_data.astype(profile['dtype']))

    print(f"Random Forest SR output saved to: {output_path}")