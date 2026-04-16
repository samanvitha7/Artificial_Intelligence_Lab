# graph
graph = {
    "Chicago": {
        "Detroit": 283,
        "Cleveland": 345,
        "Indianapolis": 182
    },
    "Detroit": {
        "Chicago": 283,
        "Cleveland": 169,
        "Buffalo": 256
    },
    "Cleveland": {
        "Chicago": 345,
        "Detroit": 169,
        "Columbus": 144,
        "Pittsburgh": 134
    },
    "Indianapolis": {
        "Chicago": 182,
        "Columbus": 176
    },
    "Columbus": {
        "Indianapolis": 176,
        "Cleveland": 144,
        "Pittsburgh": 185
    },
    "Pittsburgh": {
        "Cleveland": 134,
        "Columbus": 185,
        "Buffalo": 215,
        "Syracuse": 253,
        "Philadelphia": 305,
        "Baltimore": 247
    },
    "Buffalo": {
        "Detroit": 256,
        "Pittsburgh": 215,
        "Syracuse": 150
    },
    "Syracuse": {
        "Buffalo": 150,
        "New York": 254,
        "Pittsburgh": 253,
        "Boston": 312
    },
    "New York": {
        "Syracuse": 254,
        "Boston": 215,
        "Providence": 181,
        "Philadelphia": 97
    },
    "Philadelphia": {
        "New York": 97,
        "Pittsburgh": 305,
        "Baltimore": 101
    },
    "Baltimore": {
        "Philadelphia": 101,
        "Pittsburgh": 247
    },
    "Boston": {
        "Syracuse": 312,
        "New York": 215,
        "Providence": 50,
        "Portland": 107
    },
    "Providence": {
        "Boston": 50,
        "New York": 181
    },
    "Portland": {
        "Boston": 107
    }
}

# queue functions
def enqueue(queue, item):
    queue.append(item)

def dequeue(queue):
    item = queue[0]
    del queue[0]
    return item

def is_empty(queue):
    return len(queue) == 0

# bfs
def bfs_all_paths(graph, start, goal):
    queue = []
    enqueue(queue, (start, [start], 0))  # (current city, path, cost)

    paths = []
    exploratory_cost = 0

    while not is_empty(queue):
        current, path, cost = dequeue(queue)

        if current == goal:
            paths.append((path, cost))
            continue

        for neighbor in graph[current]:
            if neighbor not in path:  # avoid cycles
                step_cost = graph[current][neighbor]
                exploratory_cost+=step_cost
                enqueue(
                    queue,
                    (neighbor, path + [neighbor], cost + step_cost)
                )

    return paths,exploratory_cost

# dfs
def dfs_all_paths(graph, current, goal, path, cost, paths, exploration):
    if current == goal:
        paths.append((path, cost))
        return

    for neighbor in graph[current]:
        if neighbor not in path:  # avoid cycles
            step_cost = graph[current][neighbor]
            exploration[0]+=step_cost
            dfs_all_paths(
                graph,
                neighbor,
                goal,
                path + [neighbor],
                cost + step_cost,
                paths,
                exploration
            )


start = "Syracuse"
goal = "Chicago"

# BFS
bfs_paths, bfs_exploration_cost = bfs_all_paths(graph, start, goal)
print("BFS Paths:")
for p, c in bfs_paths:
    print("Path:", p, "Cost:", c)
print("BFS Exploratory Cost:",bfs_exploration_cost)

# DFS
dfs_paths = []
dfs_exploration_cost = [0]
dfs_all_paths(graph, start, goal, [start], 0, dfs_paths, dfs_exploration_cost)

print("\nDFS Paths:")
for p, c in dfs_paths:
    print("Path:", p, "Cost:", c)
print("DFS Exploratory Cost:", dfs_exploration_cost[0])