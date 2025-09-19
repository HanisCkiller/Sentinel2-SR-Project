# Methodology (Short)
- Artificial degradation (Wald's protocol): downsample 20m bands to 40m, then super-resolve back to 20m.
- Methods: Bicubic, Brovey, PCA (and 2 variants), Random Forest, ATPRK, DSen2.
- Metrics: PSNR, SSIM, SAM, RMSE.
- Urban application: compute RSEI and impervious indices on multi-temporal Sentinel-2 images.
