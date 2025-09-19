# Sentinel-2 Super-Resolution for Urban Remote Sensing (Beijing Case)

This repository packages a reproducible, well-documented version of my bachelor's thesis project on **super-resolution (SR) for Sentinel-2 imagery** in urban areas. It benchmarks multiple SR methods (traditional, ML, and DL) and applies the best-performing approach to **ecological indices** (e.g., RSEI) and **impervious surface** analysis over **southeastern Beijing**.

> **Highlights**
> - Methods compared: Bicubic, Brovey, PCA (+variants), Random Forest, ATPRK, **DSen2**.
> - Unified artificial degradation protocol (Wald's) for fair evaluation.
> - Quantitative metrics: **PSNR, SSIM, SAM, RMSE**.
> - Application: Multi-temporal (2017–2024) urban ecological & expansion analysis.
> - Tooling: **Python**, **TensorFlow/Keras**, **Google Earth Engine**, **MATLAB**.

> 📄 The full thesis PDF is available in `docs/Thesis_WangChuhan_Sentinel2_SR_Beijing.pdf`.

## Structure
```
.
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── docs/
│   ├── Thesis_WangChuhan_Sentinel2_SR_Beijing.pdf
│   ├── methodology.md
│   └── images/
├── src/
│   ├── preprocessing/
│   ├── models/
│   ├── evaluation/
│   └── utils/
├── data/              # (empty) instructions in docs; do NOT commit large data
├── results/           # figures/metrics (small outputs)
└── notebooks/
```
> **Note**: Do **not** commit large rasters; prefer download scripts or small samples.

## Quickstart
```bash
# 1) Create a virtual environment (optional)
python3 -m venv .venv && source .venv/bin/activate   # macOS/Linux
# Windows: python -m venv .venv && .\.venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Explore code & notebooks
#   - src/: preprocessing, models (Bicubic/ATPRK/DSen2), evaluation
#   - notebooks/: quick experiments
```

## Data
- Sentinel-2 L2A imagery (Copernicus, open access). Use scripts or links in `docs/` to download filtered tiles for the AOI (southeastern Beijing).
- Keep `data/` **out of git**.

## Reproduce (outline)
1. **Artificial degradation** (20m → 40m → SR back to 20m).
2. Run each SR method.
3. Compute metrics (PSNR/SSIM/SAM/RMSE) under a shared protocol.
4. Visualize qualitative differences for typical ROIs (urban blocks, water-street edges, airports).
5. Apply best-performing method to multi-temporal analysis (RSEI/impervious).
## Methods Implemented
This project compares several super-resolution methods for Sentinel-2 imagery:

| Method          | Language | Type           | Notes |
|----------------|----------|----------------|-------|
| Bicubic        | Python   | Interpolation  | Baseline |
| PCA             | Python   | Statistical    | |
| Brovey          | Python   | Statistical    | |
| Random Forest   | Python   | Machine Learning | |
| ATPRK           | MATLAB   | Geostatistical | |
| **DSen2**       | External (Python) | Deep Learning | See [DSen2 repo](https://github.com/lanha/DSen2) |

> **Note:**  
> DSen2 code is **not included** in this repository.  
> Please install it separately and follow their instructions.

## License
MIT — see `LICENSE`.
