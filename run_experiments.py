from pathlib import Path
import csv
import sys

sys.path.insert(0, str(Path(__file__).parent))
from src.io_utils import read_dimacs_graph
from src.graph_utils import graph_stats, connected_subset, make_local_graph, choose_queries
from src.algorithms import dijkstra, astar

DATA = Path("data")
RESULTS = Path("results")
RESULTS.mkdir(exist_ok=True)
GR = DATA / "USA-road-d.NY.gr"
CO = DATA / "USA-road-d.NY.co"
SIZES = [1000, 5000, 10000, 25000, 50000]

if not GR.exists() or not CO.exists():
    raise FileNotFoundError("Put USA-road-d.NY.gr and USA-road-d.NY.co inside data/.")

print("Loading New York DIMACS road network...")
graph, coords, n, m = read_dimacs_graph(GR, CO)
print(f"Loaded vertices={n}, edges={m}")

all_stats = []
query_rows = []
avg_rows = []
path_lines = []

for size in SIZES:
    print(f"Preparing {size}-vertex graph...")
    selected = connected_subset(graph, size, start=1)
    local_graph, local_coords, original_ids = make_local_graph(graph, coords, selected)
    V, E, avg_degree, max_degree = graph_stats(local_graph, range(len(local_graph)))

    all_stats.append({
        "Graph Size": V,
        "Edges": E,
        "Average Out-Degree": avg_degree,
        "Maximum Out-Degree": max_degree,
    })

    queries = choose_queries(local_graph, count=5, seed=100 + size)
    per_algorithm = {"Dijkstra": [], "A*": []}

    for qid, (s, t) in enumerate(queries, start=1):
        d = dijkstra(local_graph, s, t)
        a = astar(local_graph, local_coords, s, t)

        if d["path"] and a["path"] and abs(d["cost"] - a["cost"]) > 1e-6:
            raise AssertionError("Dijkstra and A* returned different costs.")

        for algorithm, result in [("Dijkstra", d), ("A*", a)]:
            query_rows.append({
                "Graph Size": size,
                "Query": qid,
                "Algorithm": algorithm,
                "Source": original_ids[s],
                "Destination": original_ids[t],
                "Shortest-Path Cost": result["cost"],
                "Vertices Explored": result["vertices_explored"],
                "Edges Examined": result["edges_examined"],
                "Execution Time (s)": result["time_sec"],
            })
            per_algorithm[algorithm].append(result)

        path_lines.append(f"Graph Size {size}, Query {qid}")
        path_lines.append(f"Original Source: {original_ids[s]}")
        path_lines.append(f"Original Destination: {original_ids[t]}")
        path_lines.append(f"Dijkstra cost: {d['cost']}")
        path_lines.append("Path: " + " -> ".join(map(str, [original_ids[x] for x in d["path"]])))
        path_lines.append("")

    for algorithm, rows in per_algorithm.items():
        valid = [r for r in rows if r["cost"] != float("inf")]
        avg_rows.append({
            "Graph Size": size,
            "Algorithm": algorithm,
            "Shortest-Path Cost": sum(r["cost"] for r in valid) / len(valid),
            "Vertices Explored": sum(r["vertices_explored"] for r in valid) / len(valid),
            "Edges Examined": sum(r["edges_examined"] for r in valid) / len(valid),
            "Execution Time (s)": sum(r["time_sec"] for r in valid) / len(valid),
        })

def write_csv(path, rows):
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

write_csv(RESULTS / "graph_stats.csv", all_stats)
write_csv(RESULTS / "query_results.csv", query_rows)
write_csv(RESULTS / "average_results.csv", avg_rows)
(RESULTS / "paths.txt").write_text("\n".join(path_lines), encoding="utf-8")
print("Done. Results are in results/.")
