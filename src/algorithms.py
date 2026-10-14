import heapq
import math
import time

INF = float("inf")

def reconstruct_path(parent, start, goal):
    if start == goal:
        return [start]
    if parent[goal] == -1:
        return []
    path = []
    cur = goal
    while cur != -1:
        path.append(cur)
        if cur == start:
            path.reverse()
            return path
        cur = parent[cur]
    return []

def dijkstra(graph, start, goal):
    n = len(graph)
    dist = [INF] * n
    parent = [-1] * n
    dist[start] = 0.0
    pq = [(0.0, start)]
    vertices_explored = 0
    edges_examined = 0
    t0 = time.perf_counter()

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        vertices_explored += 1
        if u == goal:
            break
        for v, w in graph[u]:
            edges_examined += 1
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))

    path = reconstruct_path(parent, start, goal)
    elapsed = time.perf_counter() - t0
    return {
        "cost": dist[goal],
        "path": path,
        "vertices_explored": vertices_explored,
        "edges_examined": edges_examined,
        "time_sec": elapsed,
    }

def haversine_m(a, b):
    if a is None or b is None:
        return 0.0
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6_371_000.0 * 2.0 * math.asin(math.sqrt(h))

def astar(graph, coords, start, goal):
    n = len(graph)
    g_score = [INF] * n
    parent = [-1] * n
    g_score[start] = 0.0

    def heuristic(node):
        return haversine_m(coords[node], coords[goal])

    pq = [(heuristic(start), 0.0, start)]
    vertices_explored = 0
    edges_examined = 0
    t0 = time.perf_counter()

    while pq:
        f, g, u = heapq.heappop(pq)
        if g != g_score[u]:
            continue
        vertices_explored += 1
        if u == goal:
            break
        for v, w in graph[u]:
            edges_examined += 1
            ng = g + w
            if ng < g_score[v]:
                g_score[v] = ng
                parent[v] = u
                heapq.heappush(pq, (ng + heuristic(v), ng, v))

    path = reconstruct_path(parent, start, goal)
    elapsed = time.perf_counter() - t0
    return {
        "cost": g_score[goal],
        "path": path,
        "vertices_explored": vertices_explored,
        "edges_examined": edges_examined,
        "time_sec": elapsed,
    }
