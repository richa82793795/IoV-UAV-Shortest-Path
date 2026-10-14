# Shortest-Path Planning in a Large-Scale IoV/UAV Mobility Network

## Dataset
**9th DIMACS Implementation Challenge – New York Road Network (USA-road-d.NY)**

Required files:
- `data/USA-road-d.NY.gr`
- `data/USA-road-d.NY.co`

Official source:
https://www.diag.uniroma1.it/challenge9/download.shtml

## Run
```powershell
python -m pip install -r requirements.txt
python download_dataset.py
python run_experiments.py
python plot_results.py
```

If you download the two files manually, put them inside `data/` and skip `download_dataset.py`.

## Output
- `results/graph_stats.csv`
- `results/query_results.csv`
- `results/average_results.csv`
- `results/paths.txt`
- three PNG plots

The numerical results must be generated from the real dataset; no experimental values are fabricated.
