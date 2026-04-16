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

class PriorityQueue:

    def __init__(self):
        self.items=[]  #(cost,state,path)

    def is_empty(self):
        return len(self.items)==0
    
    def push(self,item):
        self.items.append(item)

    def pop(self):
        min_index=0
        min_cost=self.items[0][0]

        for i in range(1,len(self.items)):
            if self.items[i][0]<min_cost:
                min_cost=self.items[i][0]
                min_index=i

        return self.items.pop(min_index)

def uniform_cost_search(grid, n, m, start, goal):
    frontier = PriorityQueue()
    frontier.push((0, start, [start]))  # (cost, state, path)

    visited = []

    # Allowed movements
    moves = [(0,1), (1,0), (-1,0), (0,-1)]

    while not frontier.is_empty():

        cost, current, path = frontier.pop()

        if current in visited:
            continue

        visited.append(current)

        if current == goal:
            return cost, path

        # Expand neighbors
        for dx, dy in moves:
            nx = current[0] + dx
            ny = current[1] + dy
            new_state = (nx, ny)

            if is_valid(nx, ny, n, m):
                if grid[nx][ny] != 1 and new_state not in visited:
                    new_cost = cost + 1   # Step cost = 1
                    frontier.push((new_cost, new_state, path + [new_state]))

    return None, None


grid = [
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0]
]

n = len(grid)      # rows = 5
m = len(grid[0])   # columns = 5

# Default start and goal positions
start = (0, 0)
goal = (4, 4)
cost, path = uniform_cost_search(grid, n, m, start, goal)

print("\nGrid (1 = obstacle):")
for i in range(n):
    print(grid[i])

print("\nUniform Cost Search Result:")
print("Cost:", cost)
print("Path:", path)