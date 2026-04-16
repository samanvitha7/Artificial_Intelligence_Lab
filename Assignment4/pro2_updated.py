import random

def is_valid(x, y, n, m):
    return 0 <= x < n and 0 <= y < m


# Randomly place obstacles in the grid
# 0 -> free cell
# 1 -> obstacle
def place_obstacles(grid, n, m, obstacle_count, start, goal):
    placed = 0

    while placed < obstacle_count:
        x = random.randint(0, n - 1)
        y = random.randint(0, m - 1)

        # Do not place obstacles on start or goal
        if (x, y) != start and (x, y) != goal and grid[x][y] == 0:
            grid[x][y] = 1
            placed += 1

# Heuristic value = shortest distance to goal
def dijkstra_heuristic(grid, n, m, goal):
    INF = 9999

    heuristic = [[INF for _ in range(m)] for _ in range(n)]
    visited = [[False for _ in range(m)] for _ in range(n)]  #visited matrix

    heuristic[goal[0]][goal[1]] = 0

    # Allowed movements (Right, Down, Up, Left)
    moves = [(0,1), (1,0), (-1,0), (0,-1)]

    for _ in range(n * m):
        min_dist = INF
        current = None

        # Finding unvisited node with minimum distance
        for i in range(n):
            for j in range(m):
                if not visited[i][j] and heuristic[i][j] < min_dist:
                    min_dist = heuristic[i][j]
                    current = (i, j)

        if current is None:
            break

        x, y = current
        visited[x][y] = True

        # Relax neighboring nodes
        for dx, dy in moves:
            nx = x + dx
            ny = y + dy

            if is_valid(nx, ny, n, m) and grid[nx][ny] != 1:
                if heuristic[nx][ny] > heuristic[x][y] + 1:
                    heuristic[nx][ny] = heuristic[x][y] + 1

    return heuristic



class PriorityQueue:
    def __init__(self, heuristic):
        self.items = []        # Stores (state, path)
        self.heuristic = heuristic

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        best_index = 0
        x, y = self.items[0][0]
        best_h = self.heuristic[x][y]

        for i in range(1, len(self.items)):
            x, y = self.items[i][0]
            if self.heuristic[x][y] < best_h:
                best_h = self.heuristic[x][y]
                best_index = i

        return self.items.pop(best_index)



def best_first_search(grid, n, m, start, goal, heuristic):
    frontier = PriorityQueue(heuristic)
    frontier.push((start, [start]))
    visited = []

    moves = [(0,1), (1,0), (-1,0), (0,-1)]

    while not frontier.is_empty():
        current, path = frontier.pop()

        # Goal test
        if current == goal:
            return path

        visited.append(current)

        # Expand neighbors
        for dx, dy in moves:
            nx = current[0] + dx
            ny = current[1] + dy
            new_state = (nx, ny)

            if is_valid(nx, ny, n, m):
                if grid[nx][ny] != 1 and new_state not in visited:
                    frontier.push((new_state, path + [new_state]))

    return None



n = int(input("Enter number of rows (n): "))
m = int(input("Enter number of columns (m): "))

grid = [[0 for _ in range(m)] for _ in range(n)]

obstacles = int(input("Enter number of obstacles: "))

sx = int(input(f"Enter start row (0-{n-1}): "))
sy = int(input(f"Enter start column (0-{m-1}): "))
gx = int(input(f"Enter goal row (0-{n-1}): "))
gy = int(input(f"Enter goal column (0-{m-1}): "))

# Validate bounds
if not (0 <= sx < n and 0 <= sy < m and 0 <= gx < n and 0 <= gy < m):
    print("Error: Coordinates out of bounds!")
    exit()

start = (sx, sy)
goal = (gx, gy)

# Place random obstacles
place_obstacles(grid, n, m, obstacles, start, goal)

# Build heuristic table using Dijkstra
heuristic = dijkstra_heuristic(grid, n, m, goal)

# Run Best-First Search
path = best_first_search(grid, n, m, start, goal, heuristic)


# OUTPUT

print("\nGrid (1 = obstacle):")
for i, row in enumerate(grid):
    print(f"Row {i}: {row}")

print("\nHeuristic Table (distance to goal):")
for i, row in enumerate(heuristic):
    print(f"Row {i}: {row}")

print("\nBest-First Search Path:")
print(path)
