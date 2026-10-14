from pathlib import Path
from urllib.request import urlretrieve
import gzip
import shutil

DATA = Path("data")
DATA.mkdir(exist_ok=True)

urls = {
    "USA-road-d.NY.gr.gz": "https://www.diag.uniroma1.it/challenge9/data/USA-road-d/USA-road-d.NY.gr.gz",
    "USA-road-d.NY.co.gz": "https://www.diag.uniroma1.it/challenge9/data/USA-road-d/USA-road-d.NY.co.gz",
}

for gz_name, url in urls.items():
    gz_path = DATA / gz_name
    out_path = DATA / gz_name[:-3]
    if out_path.exists():
        print(f"Already exists: {out_path}")
        continue
    print(f"Downloading {url}")
    urlretrieve(url, gz_path)
    print(f"Extracting {gz_path}")
    with gzip.open(gz_path, "rb") as src, open(out_path, "wb") as dst:
        shutil.copyfileobj(src, dst)
    gz_path.unlink()
    print(f"Created {out_path}")

print("Dataset preparation complete.")
