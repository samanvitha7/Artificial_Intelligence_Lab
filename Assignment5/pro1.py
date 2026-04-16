
total_girls=3
total_boys=3

def is_valid(g_left,b_left):
    g_right=total_girls-g_left
    b_right=total_boys-b_left

    if g_left<0 or b_left<0:
        return False
    if g_left>total_girls or b_left>total_boys:
        return False
    
    #left side condition
    if g_left>0 and b_left>g_left:
        return False
    
    #right side condition
    if g_right>0 and b_right>g_right:
        return False
    
    return True

def get_next_state(state):
    g_left=state[0]
    b_left=state[1]
    boat=state[2]

    next_states=[]
    moves=[(1,0),(2,0),(0,1),(0,2),(1,1)]  # 1G 0B, 2G 0B, 0G 1B, 0G 2B, 1G 1B

    for move in moves:
        g_move=move[0]
        b_move=move[1]

        #if boat on left
        if boat==0:
            new_g=g_left-g_move  #we subtract because we are moving from left to right
            new_b=b_left-b_move
            new_boat=1
        else: #boat on right
            new_g=g_left+g_move  #we add because we are moving from right to left
            new_b=b_left+b_move
            new_boat=0

        if is_valid(new_g,new_b):
            next_states.append((new_g,new_b,new_boat))

    return next_states

def depth_limited_search(state,goal,limit,path,visited):
    if state==goal:
        return path
    
    if limit==0:
        return None
    
    visited.add(state)
    next_states=get_next_state(state)

    for next_s in next_states:
        if next_s not in visited:
            result=depth_limited_search(next_s,goal,limit-1,path+[next_s],visited)
            if result is not None:
                return result
            
    visited.remove(state)
    return None


def iterative_deepening_search(initial,goal):
    depth=0
    while True:
        visited=set()
        result=depth_limited_search(initial,goal,depth,[initial],visited)
        if result is not None:
            return result
        
        depth+=1


initial_state=(3,3,0)
goal_state=(0,0,1)

print("Depth Limited Search with limit = 3")
result = depth_limited_search(initial_state, goal_state, 3, [initial_state], set())

if result is None:
    print("No solution found within depth 3")
else:
    for step in result:
        print(step)


print("\nIterative Deepening Search")
solution = iterative_deepening_search(initial_state, goal_state)

print("Optimal Solution:")
for step in solution:
    print(step)