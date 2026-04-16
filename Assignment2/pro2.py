
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0


def get_neighbors(state):
    neighbors = []
    index = state.index(0)   
    row = index // 3
    col = index % 3

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    for move in moves:
        new_row = row + move[0]
        new_col = col + move[1]

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)

            # swap blank with adjacent tile
            new_state[index], new_state[new_index] = \
                new_state[new_index], new_state[index]

            neighbors.append(tuple(new_state))

    return neighbors

def dfs(start, goal):
    stack = Stack()
    visited = []

    stack.push(start)
    visited.append(start)

    explored_count = 0
    max_states = 100000  # Add limit to prevent infinite running

    while not stack.is_empty() and explored_count < max_states:
        current = stack.pop()
        explored_count += 1
        
        # Show progress every 10000 states
        if explored_count % 10000 == 0:
            print(f"Explored {explored_count} states...")

        if current == goal:
            print("Goal reached!")
            print("States explored:", explored_count)
            return explored_count

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.append(neighbor)
                stack.push(neighbor)

    if explored_count >= max_states:
        print(f"Stopped after exploring {explored_count} states (limit reached)")
    else:
        print("Goal not reachable")
    return explored_count


start_state = (
    7, 2, 4,
    5, 0, 6,
    8, 3, 1
)

goal_state = (
    0, 1, 2,
    3, 4, 5,
    6, 7, 8
)

dfs(start_state, goal_state)
