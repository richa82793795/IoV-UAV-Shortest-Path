from collections import deque
import random

def graph_stats(graph, active_nodes=None):
    if active_nodes is None:
        active_nodes = range(1, len(graph))
    active = set(active_nodes)
    vertices = len(active)
    edges = 0
    max_out = 0
    for u in active:
        count = 0
        for v, _ in graph[u]:
            if v in active:
                edges += 1
                count += 1
        max_out = max(max_out, count)
    avg_out = edges / vertices if vertices else 0.0
    return vertices, edges, avg_out, max_out

def connected_subset(graph, size, start=1):
    if size >= len(graph) - 1:
        return list(range(1, len(graph)))
    visited = {start}
    q = deque([start])
    while q and len(visited) < size:
        u = q.popleft()
        for v, _ in graph[u]:
            if v not in visited:
                visited.add(v)
                q.append(v)
                if len(visited) >= size:
                    break
    if len(visited) < size:
        for candidate in range(1, len(graph)):
            if candidate not in visited:
                visited.add(candidate)
                q.append(candidate)
                while q and len(visited) < size:
                    u = q.popleft()
                    for v, _ in graph[u]:
                        if v not in visited:
                            visited.add(v)
                            q.append(v)
                            if len(visited) >= size:
                                break
            if len(visited) >= size:
                break
    return list(visited)[:size]

def make_local_graph(graph, coords, original_nodes):
    original_nodes = list(original_nodes)
    index = {old: i for i, old in enumerate(original_nodes)}
    local_graph = [[] for _ in original_nodes]
    local_coords = [None] * len(original_nodes)
    for old_u, new_u in index.items():
        local_coords[new_u] = coords[old_u]
        for old_v, w in graph[old_u]:
            if old_v in index:
                local_graph[new_u].append((index[old_v], w))
    return local_graph, local_coords, original_nodes

def reachable(graph, source, target):
    q = deque([source])
    seen = {source}
    while q:
        u = q.popleft()
        if u == target:
            return True
        for v, _ in graph[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return False

def choose_queries(graph, count=5, seed=42):
    n = len(graph)
    rng = random.Random(seed)
    queries = []
    for _ in range(300):
        if len(queries) >= count:
            break
        s = rng.randrange(n)
        t = rng.randrange(n)
        if s != t and reachable(graph, s, t):
            if (s, t) not in queries:
                queries.append((s, t))
    if len(queries) < count:
        q = deque([0])
        seen = {0}
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v, _ in graph[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        for t in order[::-1]:
            if len(queries) >= count:
                break
            if t != 0 and (0, t) not in queries:
                queries.append((0, t))
    if len(queries) < count:
        raise RuntimeError("Could not find enough reachable source-destination pairs.")
    return queries[:count]
