
class PriorityQueue:

    def __init__(self):
        self.data=[]  #stores (node,cost,path)

    def push(self,item):
        self.data.append(item)

    def pop(self):
        if len(self.data)==0:
            return None
        min_index=0
        for i in range(len(self.data)):
            if self.data[i][1]<self.data[min_index][1]:
                min_index=i
        return self.data.pop(min_index)
    
    def is_empty(self):
        return len(self.data)==0
    

def uniform_cost_search(problem,start,goal):
    frontier=PriorityQueue()
    frontier.push((start,0,[start]))
    explored=[]
    paths_explored = 0

    while not frontier.is_empty():
        current_node,current_cost,path=frontier.pop()
        paths_explored += 1
        if current_node==goal:
            return path,current_cost, paths_explored
        explored.append(current_node)

        for neighbour,cost in problem[current_node]:
            if neighbour not in explored:
                new_cost=current_cost+cost
                new_path=path+[neighbour]
                frontier.push((neighbour,new_cost,new_path))

    return None, 0, paths_explored


problem = {
    "Syracuse": [("Buffalo", 150), ("Philadelphia", 253), ("New York", 254), ("Boston", 312)],
    "Buffalo": [("Syracuse", 150), ("Detroit", 256), ("Cleveland", 189)],
    "Detroit": [("Buffalo", 256), ("Chicago", 283)],
    "Cleveland": [("Buffalo", 189), ("Chicago", 345), ("Pittsburgh", 134)],
    "Chicago": [("Detroit", 283), ("Cleveland", 345)],
    "Philadelphia": [("Syracuse", 253), ("Pittsburgh", 305), ("New York", 97)],
    "New York": [("Syracuse", 254), ("Philadelphia", 97)],
    "Boston": [("Syracuse", 312)],
    "Pittsburgh": [("Philadelphia", 305), ("Cleveland", 134)]
}

result = uniform_cost_search(problem, "Syracuse", "Chicago")

if result[0]:
    path, cost, paths_explored = result
    print("Optimal Path:", path)
    print("Total Cost:", cost)
    print("Paths Explored:", paths_explored)
else:
    print("No path found")

