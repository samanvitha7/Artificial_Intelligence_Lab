
class Queue:
    def __init__(self):
        self.items=[]
        self.front=0

    def enqueue(self,item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            item=self.items[self.front]
            self.front+=1
            return item
        return None
        
    def is_empty(self):
        return self.front>=len(self.items)
        

def get_adjacent(state):
    adjacent=[]
    index=state.index(0) #we get the index of blank tile
    row=index//3
    col=index%3

    moves=[(-1,0),(1,0),(0,-1),(0,1)] #up,down,left,right
    for move in moves:
        new_row=row+move[0]
        new_col=col+move[1]

        if 0<=new_row<3 and 0<=new_col<3:
            new_index=new_row*3+new_col
            new_state=list(state)  
            #swap blank with adjacent tile
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            adjacent.append(tuple(new_state))  

    return adjacent


def bfs(start,goal):
    queue=Queue()
    visited=[]

    queue.enqueue(start)
    visited.append(start)

    explored_count=0
    max_states = 50000  # Add limit to prevent infinite running
    
    while not queue.is_empty() and explored_count < max_states:
        current=queue.dequeue()
        explored_count+=1
        
        # Show progress every 10000 states
        if explored_count % 10000 == 0:
            print(f"Explored {explored_count} states...")

        if current==goal:
            print("Goal reached")
            print("State explored:",explored_count)
            return explored_count
        
        for neighbour in get_adjacent(current):
            if neighbour not in visited:
                visited.append(neighbour)
                queue.enqueue(neighbour)

    if explored_count >= max_states:
        print(f"Stopped after exploring {explored_count} states (limit reached)")
    else:
        print("Goal not reached")
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

bfs(start_state,goal_state)