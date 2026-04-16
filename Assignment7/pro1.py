import random
import copy

# Heuristic function: count attacking pairs
def heuristic(state):
    conflicts = 0
    for i in range(8):
        for j in range(i+1, 8):
            # same row
            if state[i] == state[j]:
                conflicts += 1
            # same diagonal
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts


# Generate random board
def random_board():
    return [random.randint(0,7) for _ in range(8)]


# Generate neighbors
def get_neighbors(state):
    neighbors = []
    for col in range(8):
        for row in range(8):
            if row != state[col]:
                new_state = state.copy()
                new_state[col] = row
                neighbors.append(new_state)
    return neighbors


# Steepest-ascent hill climbing
def hill_climbing(initial):
    current = initial
    steps = 0
    
    while True:
        current_h = heuristic(current)
        neighbors = get_neighbors(current)
        
        best_neighbor = None
        best_h = current_h
        
        for neighbor in neighbors:
            h = heuristic(neighbor)
            if h < best_h:
                best_h = h
                best_neighbor = neighbor
        
        if best_neighbor is None:
            # no better neighbor found
            return current_h, steps, False
        
        current = best_neighbor
        steps += 1
        
        if best_h == 0:
            return best_h, steps, True


# Run 50 random boards
results = []

for i in range(50):
    board = random_board()
    initial_h = heuristic(board)
    final_h, steps, solved = hill_climbing(board)
    
    results.append((initial_h, final_h, steps, solved))

# Print results
for i, r in enumerate(results):
    print(f"Run {i+1}: Initial h={r[0]}, Final h={r[1]}, Steps={r[2]}, Solved={r[3]}")