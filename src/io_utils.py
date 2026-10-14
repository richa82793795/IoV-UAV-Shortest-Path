from pathlib import Path

def read_dimacs_graph(gr_file, co_file):
    gr_file = Path(gr_file)
    co_file = Path(co_file)

    n = None
    m = None
    with gr_file.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("p"):
                parts = line.split()
                n = int(parts[2])
                m = int(parts[3])
                break

    if n is None:
        raise ValueError("DIMACS problem line was not found.")

    graph = [[] for _ in range(n + 1)]
    with gr_file.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("a"):
                parts = line.split()
                u, v, w = int(parts[1]), int(parts[2]), float(parts[3])
                graph[u].append((v, w))

    coords = [None] * (n + 1)
    with co_file.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("v"):
                parts = line.split()
                node = int(parts[1])
                lon = int(parts[2]) / 1_000_000.0
                lat = int(parts[3]) / 1_000_000.0
                coords[node] = (lat, lon)

    return graph, coords, n, m
