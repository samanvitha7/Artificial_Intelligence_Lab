from itertools import permutations

# PriorityQueue implementation using a list
class PriorityQueue:
    def __init__(self):
        self.queue = []
    
    def push(self, item):
        self.queue.append(item)
    
    def pop(self):
        if len(self.queue) == 0:
            raise IndexError("pop from empty queue")
        
        # Find the index of the minimum element
        min_index = 0
        for i in range(1, len(self.queue)):
            if self.queue[i] < self.queue[min_index]:
                min_index = i
        
        # Remove and return the minimum element
        return self.queue.pop(min_index)
    
    def __len__(self):
        return len(self.queue)

"""
MAZE SOLVER WITH A* ALGORITHM
==============================
Maze: 5x5 matrix
  0 = empty tile (walkable)
  1 = wall (obstacle)
  2 = start position
  3 = reward (goal)

Goal: Visit ALL rewards using A* algorithm

Heuristic: h(n) = Manhattan Distance
  h(n) = |current_row - goal_row| + |current_col - goal_col|
  Justification: Never overestimates, admissible for A*

Evaluation Cost: g(n) = steps taken  
  g(n) = number of moves (each = 1 unit)
  Justification: Equal cost per move in grid
"""

maze = [
    [2,0,0,0,1],    # Row 0
    [0,1,0,0,3],    # Row 1
    [0,3,0,1,1],    # Row 2
    [0,1,0,0,1],    # Row 3
    [3,0,0,0,3]     # Row 4
]

ROWS = 5
COLS = 5

start = None
rewards = []

for r in range(ROWS):
    for c in range(COLS):
        if maze[r][c] == 2:
            start = (r, c)
        if maze[r][c] == 3:
            rewards.append((r, c))

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(r, c):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    result = []
    
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] != 1:
            result.append((nr, nc))
    
    return result

def a_star(start_pos, goal_pos, segment_info="", print_exploration=False):
   
    pq = PriorityQueue()
    pq.push((heuristic(start_pos, goal_pos), 0, start_pos))
    g_cost = {start_pos: 0}
    parent = {}
    visited = set()
    visited_order = []

    while len(pq) > 0:
        f_cost, g, current = pq.pop()  #get node with lowest f_cost

        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)
        
        # Print h(n) and g(n) for current state (only if requested)
        if print_exploration:
            h_value = heuristic(current, goal_pos)
            print(f"{segment_info}Exploring: {str(current):8} | f(n) = {f_cost:3} | g(n) = {g:3} | h(n) = {h_value:3}")

        if current == goal_pos:
            path = []
            node = current
            while node in parent:
                path.append(node)
                node = parent[node]
            path.append(start_pos)
            path.reverse()
            return path, visited_order

        for neighbor in get_neighbors(*current):
            if neighbor not in visited:
                new_g = g_cost[current] + 1

                if neighbor not in g_cost or new_g < g_cost[neighbor]:  #either we didnt visit neighbor before or we found a cheaper path
                    g_cost[neighbor] = new_g
                    f = new_g + heuristic(neighbor, goal_pos)
                    pq.push((f, new_g, neighbor))
                    parent[neighbor] = current     #keep track of path as we dont have a separate path variable in the priority queue

    return None, visited_order

def find_optimal_tour():
    """Find optimal order to visit all rewards"""
    best_path = []
    best_visited = []
    min_cost = float('inf')
    best_order = None

    for reward_order in permutations(rewards):
        total_path = [start]
        total_visited = []
        current = start
        total_cost = 0

        for reward in reward_order:
            path, visited = a_star(current, reward)
            if path is None:
                total_cost = float('inf')
                break

            total_path.extend(path[1:])
            total_visited.extend(visited)
            total_cost += len(path) - 1
            current = reward

        if total_cost < min_cost:
            min_cost = total_cost
            best_path = total_path
            best_visited = total_visited
            best_order = reward_order

    return best_path, best_visited, min_cost, best_order

def find_and_display_optimal_tour():
    """Find and display the optimal tour with detailed A* exploration"""
    print("="*60)
    print("FINDING OPTIMAL TOUR ORDER...")
    print("="*60)
    
    # Find optimal order quietly first
    best_path, best_visited, min_cost, best_order = find_optimal_tour()
    
    print(f"\nOptimal order found: {start} → {' → '.join([str(r) for r in best_order])}")
    print(f"Total cost: {min_cost}\n")
    
    print("DETAILED A* EXPLORATION FOR OPTIMAL TOUR:")

    
    # Now run A* again with printing for the best order
    current = start
    segment_num = 1
    
    for reward in best_order:
        print(f"\n--- Segment {segment_num}: {current} → {reward} ---")
        path, visited = a_star(current, reward, segment_info=f"  ", print_exploration=True)
        current = reward
        segment_num += 1
    
    return best_path, best_visited, min_cost

print("Start: {0}, Rewards: {1}\n".format(start, rewards))

path, visited, cost = find_and_display_optimal_tour()

if path:
    print("\n")
    print("FINAL RESULTS:")
    print("Path: {0}".format(' → '.join([str(p) for p in path])))
    print("Cost: {0}\n".format(cost))
    
    print("Maze (S=start, R=reward, #=wall, *=path):")
    display = [row[:] for row in maze]
    
    for pos in path:
        r, c = pos
        if display[r][c] == 0:
            display[r][c] = '*'
    
    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            if (r, c) == start:
                row_str += "S "
            elif (r, c) in rewards:
                row_str += "R "
            elif display[r][c] == '*':
                row_str += "* "
            elif display[r][c] == 1:
                row_str += "# "
            else:
                row_str += ". "
        print(row_str)
else:
    print("No path found")