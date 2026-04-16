from collections import deque

# Graph representation
city_map = {
    'Chicago': [('Detroit', 283), ('Indianapolis', 182), ('Cleveland', 345)],
    'Detroit': [('Chicago', 283), ('Buffalo', 256), ('Cleveland', 169)],
    'Buffalo': [('Detroit', 256), ('Syracuse', 150), ('Cleveland', 189)],
    'Syracuse': [('Buffalo', 150), ('Boston', 312), ('New York', 150)],
    'Boston': [('Syracuse', 312), ('Providence', 50), ('New York', 107)],
    'Providence': [('Boston', 50), ('New York', 181)],
    'New York': [('Syracuse', 150), ('Boston', 107), ('Providence', 181), ('Philadelphia', 97)],
    'Philadelphia': [('New York', 97), ('Pittsburgh', 305), ('Baltimore', 101)],
    'Baltimore': [('Philadelphia', 101), ('Pittsburgh', 247)],
    'Pittsburgh': [('Philadelphia', 305), ('Buffalo', 189), ('Cleveland', 134), ('Columbus', 185), ('Baltimore', 247)],
    'Cleveland': [('Detroit', 169), ('Buffalo', 189), ('Pittsburgh', 134), ('Columbus', 144), ('Chicago', 345)],
    'Columbus': [('Cleveland', 144), ('Pittsburgh', 185), ('Indianapolis', 176)],
    'Indianapolis': [('Chicago', 182), ('Columbus', 176)],
}

# Counters
count_bfs = 0
count_dfs = 0
count_ab = 0


# BFS 
def run_bfs(src, dest):
    global count_bfs
    count_bfs = 0

    q = deque([(src, [src], 0)])
    seen = set()

    while q:
        current, route, dist = q.popleft()
        count_bfs += 1

        if current == dest:
            return route, dist

        if current in seen:
            continue
        seen.add(current)

        for nxt, d in city_map.get(current, []):
            if nxt not in seen:
                q.append((nxt, route + [nxt], dist + d))

    return None, float('inf')


#DFS 
def run_dfs(src, dest):
    global count_dfs
    count_dfs = 0

    def helper(node, path, cost, visited):
        global count_dfs
        count_dfs += 1

        if node == dest:
            return path, cost

        visited.add(node)
        best = (None, float('inf'))

        for nxt, d in city_map.get(node, []):
            if nxt not in visited:
                res_path, res_cost = helper(nxt, path + [nxt], cost + d, visited.copy())
                if res_path and res_cost < best[1]:
                    best = (res_path, res_cost)

        return best

    return helper(src, [src], 0, set())


#Alpha-Beta
def run_alpha_beta(src, dest):
    global count_ab
    count_ab = 0

    best_route = None
    best_val = float('inf')

    def explore(node, path, cost, alpha, beta, visited):
        nonlocal best_route, best_val
        global count_ab

        count_ab += 1

        if cost >= beta:
            return None, beta

        if node == dest:
            if cost < best_val:
                best_val = cost
                best_route = path
            return path, cost

        visited.add(node)

        neighbors = sorted(city_map.get(node, []), key=lambda x: x[1])

        for nxt, d in neighbors:
            if nxt not in visited:
                new_cost = cost + d

                if new_cost >= beta:
                    continue

                _, val = explore(nxt, path + [nxt], new_cost, alpha, beta, visited.copy())

                if val < beta:
                    beta = val

        return best_route, best_val

    explore(src, [src], 0, 0, float('inf'), set())
    return best_route, best_val


# Analysis 
def evaluate(src, dest, label):

    print(f"\n{label}: {src} → {dest}")

    # BFS
    p1, c1 = run_bfs(src, dest)
    print("BFS:")
    print(f"  Path: {' → '.join(p1) if p1 else 'Not found'}")
    print(f"  Cost: {c1} miles")
    print(f"  Nodes expanded: {count_bfs}")

    # DFS
    p2, c2 = run_dfs(src, dest)
    print("\nDFS:")
    print(f"  Path: {' → '.join(p2) if p2 else 'Not found'}")
    print(f"  Cost: {c2} miles")
    print(f"  Nodes expanded: {count_dfs}")

    # Alpha-Beta
    p3, c3 = run_alpha_beta(src, dest)
    print("\nAlpha-Beta Pruning:")
    print(f"  Path: {' → '.join(p3) if p3 else 'Not found'}")
    print(f"  Cost: {c3} miles")
    print(f"  Nodes expanded: {count_ab}")

    return count_bfs, count_dfs, count_ab



print("SCENARIO 1: SHORT ROUTES")
s1 = evaluate('Boston', 'New York', "Short route")

print("\nSCENARIO 2: MEDIUM ROUTES")
s2 = evaluate('Syracuse', 'Chicago', "Medium route")

print("\nSCENARIO 3: LONG ROUTES")
s3 = evaluate('Boston', 'Indianapolis', "Long route")


# -------- FINAL SUMMARY --------

print("\n")
print("PRUNING PATTERNS ANALYSIS")


print("{:<20} {:<10} {:<10} {:<10}".format("Scenario", "BFS", "DFS", "Alpha-Beta"))

data = [("Short", *s1), ("Medium", *s2), ("Long", *s3)]

for name, b, d, a in data:
    print("{:<20} {:<10} {:<10} {:<10}".format(name, b, d, a))


print("\n")
print("KEY INSIGHTS")

print("Short → minimal pruning (small tree)")
print("Medium → noticeable pruning")
print("Long → maximum pruning efficiency")

reductions = []
for name, b, d, a in data:
    if d > 0:
        red = ((d - a) / d) * 100
        reductions.append(red)
        print(f"{name}: {red:.1f}% reduction")

avg = sum(reductions) / len(reductions) if reductions else 0
print(f"Average reduction: {avg:.1f}%")

