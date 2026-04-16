
cities = [
    "Chicago", "Detroit", "Cleveland", "Indianapolis", "Columbus",
    "Pittsburgh", "Buffalo", "Syracuse", "NewYork", "Philadelphia",
    "Baltimore", "Boston", "Providence", "Portland"
]

n = len(cities)

# graph (Adjacency Matrix)
graph = [
    [0, 283, 345, 182, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [283, 0, 169, 0, 0, 0, 256, 0, 0, 0, 0, 0, 0, 0],
    [345, 169, 0, 0, 144, 134, 189, 0, 0, 0, 0, 0, 0, 0],
    [182, 0, 0, 0, 176, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 144, 176, 0, 185, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 134, 0, 185, 0, 215, 0, 0, 305, 247, 0, 0, 0],
    [0, 256, 189, 0, 0, 215, 0, 150, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 150, 0, 254, 253, 0, 312, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 254, 0, 97, 0, 0, 181, 0],
    [0, 0, 0, 0, 0, 305, 0, 253, 97, 0, 101, 0, 0, 0],
    [0, 0, 0, 0, 0, 247, 0, 0, 0, 101, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 312, 0, 0, 0, 0, 50, 107],
    [0, 0, 0, 0, 0, 0, 0, 0, 181, 0, 0, 50, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 107, 0, 0]
]

class Node:
    def __init__(self,state,parent=None,path_cost=0):
        self.state=state  #city name
        self.parent=parent
        self.path_cost=path_cost


class PriorityQueue:
    def __init__(self, h):
        self.items = []   # list of nodes
        self.h = h        # heuristic table

    def is_empty(self):
        return len(self.items) == 0

    def push(self, node):
        self.items.append(node)

    def pop(self):
        # remove node with smallest heuristic value
        best = 0
        for i in range(1, len(self.items)):
            if self.h[self.items[i].state] < self.h[self.items[best].state]:
                best = i
        return self.items.pop(best)
    

#to find heuristic values we apply dijktras from the goal to all other nodes
def heuristic(goal):
    h={city: float('inf') for city in cities}
    h[goal]=0
    visited=set()

    #choosing next city with smallest h
    while len(visited)<n:
        current=None
        for city in cities:
            if city not in visited:
                if current is None or h[city]<h[current]:
                    current=city
        visited.add(current)
        i = cities.index(current)

        # relax edges
        for j in range(n):
            if graph[i][j] != 0:
                neighbor = cities[j]
                new_cost = h[current] + graph[i][j]
                if new_cost < h[neighbor]:
                    h[neighbor] = new_cost

    return h


def expand(node):
    children = []
    i = cities.index(node.state)
    for j in range(n):
        if graph[i][j] != 0:
            new_cost = node.path_cost + graph[i][j]
            children.append(Node(cities[j], node, new_cost))
    return children

def solution(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

def BEST_FIRST_SEARCH(start, goal, h):
    frontier = PriorityQueue(h)
    reached = {}

    start_node = Node(start)
    frontier.push(start_node)
    reached[start] = start_node

    explored = 0

    while not frontier.is_empty():
        node = frontier.pop()
        explored += 1

        if node.state == goal:
            return solution(node), node.path_cost, explored

        for child in expand(node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.push(child)

    return None, None, explored

h = heuristic("Chicago")
path, cost, explored = BEST_FIRST_SEARCH("Syracuse", "Chicago", h)

print("Heuristic Table (h*):")
print(h)
print("\nPath:", path)
print("Total Cost:", cost)
print("Nodes Explored:", explored)