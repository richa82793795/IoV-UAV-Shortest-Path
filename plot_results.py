from pathlib import Path
import csv
import matplotlib.pyplot as plt

RESULTS = Path("results")
with (RESULTS / "average_results.csv").open("r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

for metric, filename, ylabel in [
    ("Execution Time (s)", "execution_time.png", "Average Execution Time (seconds)"),
    ("Vertices Explored", "vertices_explored.png", "Average Vertices Explored"),
    ("Edges Examined", "edges_examined.png", "Average Edges Examined"),
]:
    plt.figure()
    for algorithm in ["Dijkstra", "A*"]:
        data = [r for r in rows if r["Algorithm"] == algorithm]
        data.sort(key=lambda x: int(x["Graph Size"]))
        x = [int(r["Graph Size"]) for r in data]
        y = [float(r[metric]) for r in data]
        plt.plot(x, y, marker="o", label=algorithm)
    plt.xlabel("Graph Size (vertices)")
    plt.ylabel(ylabel)
    plt.title(f"{ylabel} vs Graph Size")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(RESULTS / filename, dpi=200)
    plt.close()

print("Plots created in results/.")
