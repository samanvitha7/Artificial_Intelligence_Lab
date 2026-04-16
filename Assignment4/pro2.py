"""
here we use manhattan distance as heuristic function.
the only movements allowed are up,dow,left and right.
this si the best choice as it doesnt consider diagonal movements and only calculates the distance based on allowed movements.
"""
def manhattan_distance(current,goal):
    return abs(current[0]-goal[0])+abs(current[1]-goal[1])

class PriorityQueue():
    def __init__(self,goal):
        self.items=[]  # items list consist of item where each item represents (state,path)
        self.goal = goal

    def is_empty(self):
        return len(self.items)==0
    
    def push(self,item):
        self.items.append(item)

    def pop(self):
        best_index=0
        best_h=manhattan_distance(self.items[0][0],self.goal)

        for i in range(1,len(self.items)):
            h=manhattan_distance(self.items[i][0],self.goal)
            if h<best_h:
                best_h=h
                best_index=i
        return self.items.pop(best_index)
    

def best_first_search(problem,start,goal):
    rows=len(problem)
    cols=len(problem[0])

    frontier=PriorityQueue(goal)
    frontier.push((start,[start]))  #path initially contains only start state
    visited=[]

    moves=[(0,1),(1,0),(-1,0),(0,-1)]  #right,down,left,up

    while not frontier.is_empty():
        current,path=frontier.pop()
        if current==goal:
            return path
        
        visited.append(current)

        for move in moves:
            new_x=current[0]+move[0]
            new_y=current[1]+move[1]

            if 0<=new_x<rows and 0<=new_y<cols:
                if problem[new_x][new_y]!=1 and (new_x,new_y) not in visited: # ignore walls/rooms and already visited states
                    new_state=(new_x,new_y)
                    new_path=path+[new_state]
                    frontier.push((new_state,new_path))

    return None  #no path found



def find_start_goal(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                start = (i, j)
            if grid[i][j] == 'G':
                goal = (i, j)
    return start, goal


problem = [
    ['S', 0, 1, 1, 1, 1],
    [0,   0, 0, 0, 0, 'G'],
    [1,   1, 1, 1, 0, 1]
]

start, goal = find_start_goal(problem)

path = best_first_search(problem, start, goal)

print("Evacuation Path:")
print(path)
