
class PriorityQueue:
    def __init__(self):
        self.queue = []
    
    def push(self, item):
        self.queue.append(item)
    
    def pop(self):
        if len(self.queue) == 0:
            raise IndexError("pop from empty queue")
        
        min_index = 0
        for i in range(1, len(self.queue)):
            if self.queue[i] < self.queue[min_index]:
                min_index = i
        
        return self.queue.pop(min_index)
    
    def __len__(self):
        return len(self.queue)


cities = [
    "Chicago", "Detroit", "Cleveland", "Indianapolis", "Columbus",
    "Pittsburgh", "Buffalo", "Syracuse", "Boston", "Portland",
    "Providence", "New York", "Philadelphia", "Baltimore"
]

h = {
    "Boston": 0,
    "Providence": 50,
    "Portland": 107,
    "New York": 215,
    "Philadelphia": 270,
    "Baltimore": 360,
    "Syracuse": 260,
    "Buffalo": 400,
    "Pittsburgh": 470,
    "Cleveland": 550,
    "Columbus": 640,
    "Detroit": 610,
    "Indianapolis": 780,
    "Chicago": 860
}

# Order: Chicago, Detroit, Cleveland, Indianapolis, Columbus, Pittsburgh, Buffalo, Syracuse, Boston, Portland, Providence, New York, Philadelphia, Baltimore
distance = [
#Ch De Cl In Co  P  Bu Sy Bo Po Pr NY Ph Ba
[0, 283, 345, 182, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     
[283, 0, 169, 0, 0, 0, 256, 0, 0, 0, 0, 0, 0, 0],     
[345, 169, 0, 0, 144, 134, 189, 0, 0, 0, 0, 0, 0, 0], 
[182, 0, 0, 0, 176, 0, 0, 0, 0, 0, 0, 0, 0, 0],      
[0, 0, 144, 176, 0, 185, 0, 0, 0, 0, 0, 0, 0, 0],     
[0, 0, 134, 0, 185, 0, 215, 0, 0, 0, 0, 0, 305, 247], 
[0, 256, 189, 0, 0, 215, 0, 150, 0, 0, 0, 0, 0, 0],   
[0, 0, 0, 0, 0, 0, 150, 0, 312, 0, 0, 254, 253, 0],  
[0, 0, 0, 0, 0, 0, 0, 312, 0, 107, 50, 215, 0, 0],   
[0, 0, 0, 0, 0, 0, 0, 0, 107, 0, 0, 0, 0, 0],         
[0, 0, 0, 0, 0, 0, 0, 0, 50, 0, 0, 181, 0, 0],       
[0, 0, 0, 0, 0, 0, 0, 254, 215, 0, 181, 0, 97, 0],   
[0, 0, 0, 0, 0, 305, 0, 253, 0, 0, 0, 97, 0, 101],    
[0, 0, 0, 0, 0, 247, 0, 0, 0, 0, 0, 0, 101, 0]        
]

# Greedy Best First Search
def greedy_best_first(start, goal):
    pq = PriorityQueue()
    pq.push((h[start], start, [start], 0))  # (heuristic, city, path, cost)
    visited = set()
    explored_order = []

    while len(pq) > 0:
        heuristic, city, path, cost = pq.pop()

        if city in visited:
            continue

        visited.add(city)
        explored_order.append(city)
        
        # Print h(n) and g(n) for current state
        print(f"Exploring: {city:15} | h(n) = {heuristic:3} | g(n) = {cost:4}")

        if city == goal:
            return path, cost, explored_order

        city_idx = cities.index(city)

        for j in range(len(distance)):
            if distance[city_idx][j] > 0:
                neighbor = cities[j]
                if neighbor not in visited:
                    pq.push((h[neighbor], neighbor, path + [neighbor], cost + distance[city_idx][j]))

    return None, float('inf'), explored_order

# A* Algorithm
def astar_search(start, goal):
    pq = PriorityQueue()
    pq.push((h[start], 0, start, [start]))  # (f=g+h, g, city, path)
    visited = set()
    explored_order = []

    while len(pq) > 0:
        f_score, g_cost, city, path = pq.pop()

        if city in visited:
            continue

        visited.add(city)
        explored_order.append(city)
        
        # Print f(n) and g(n) for current state
        h_value = h[city]
        print(f"Exploring: {city:15} | f(n) = {f_score:4} | g(n) = {g_cost:4} | h(n) = {h_value:3}")

        if city == goal:
            return path, g_cost, explored_order

        city_idx = cities.index(city)

        for j in range(len(distance)):
            if distance[city_idx][j] > 0:
                neighbor = cities[j]
                if neighbor not in visited:
                    new_g = g_cost + distance[city_idx][j]
                    f = new_g + h[neighbor]
                    pq.push((f, new_g, neighbor, path + [neighbor]))

    return None, float('inf'), explored_order

# Run searches
start = "Chicago"
goal = "Boston"

print("GREEDY BEST FIRST SEARCH")
gbfs_path, gbfs_cost, gbfs_explored = greedy_best_first(start, goal)

print("\n")
print("A* SEARCH")

astar_path, astar_cost, astar_explored = astar_search(start, goal)

print("\n")
print("RESULTS SUMMARY")
print("\nGREEDY BEST FIRST SEARCH")
print(f"Path: {' → '.join(gbfs_path)}")
print(f"Cost: {gbfs_cost}, Cities Explored: {len(gbfs_explored)}")

print("\nA* SEARCH")
print(f"Path: {' → '.join(astar_path)}")
print(f"Cost: {astar_cost}, Cities Explored: {len(astar_explored)}")

print("\nCOMPARISON")
print(f"GBFS: {len(gbfs_explored)} cities | A*: {len(astar_explored)} cities")