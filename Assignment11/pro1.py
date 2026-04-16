graph = {
    "Ahmedabad": ["Gandhinagar", "Kheda", "Mehsana", "Anand"],
    "Gandhinagar": ["Ahmedabad", "Mehsana", "Sabarkantha"],
    "Mehsana": ["Ahmedabad", "Gandhinagar", "Patan", "Banaskantha"],
    "Kheda": ["Ahmedabad", "Anand", "Panchmahal"],
    "Anand": ["Ahmedabad", "Kheda", "Vadodara"],
    "Vadodara": ["Anand", "Bharuch", "Panchmahal"],
    "Bharuch": ["Vadodara", "Surat"],
    "Surat": ["Bharuch", "Navsari"],
    "Navsari": ["Surat", "Valsad"],
    "Valsad": ["Navsari"],
    "Sabarkantha": ["Gandhinagar", "Panchmahal"],
    "Patan": ["Mehsana", "Banaskantha"],
    "Banaskantha": ["Mehsana", "Patan"],
    "Panchmahal": ["Kheda", "Vadodara", "Sabarkantha"]
}

colors = ["Red", "Green", "Blue", "Yellow"]

#check if assignemnt is valid
def is_safe(node,color,assignment):
    for neighbor in graph[node]:
        if neighbor in assignment and assignment[neighbor]==color:
            return False
    return True
    
#forward checking
def forward_checking(node,color,domains):
    new_domains={v:list(domains[v]) for v in domains}

    for neighbor in graph[node]:
        if color in new_domains[neighbor]:
            new_domains[neighbor].remove(color)

            #if any neighbor has no color left that is the domain is empty
            if not new_domains[neighbor]:
                return None
    return new_domains


#backtracking algorithm
def backtrack(assignment,domains,depth=0):
    indent = "  " * depth  # For visual indentation
    
    #if all variables are assigned
    if len(assignment)==len(graph):
        print(f"{indent}✓ Solution found!")
        return assignment
    
    #select first unassigned variable
    for var in graph:
        if var not in assignment:
            break

    print(f"{indent}Step {len(assignment)+1}: Trying to assign color to '{var}'")
    print(f"{indent}Available colors for {var}: {domains[var]}")
    
    for color in domains[var]:
        if is_safe(var,color,assignment):
            print(f"{indent}  → Assigning {var} = {color}")
            assignment[var]=color
            new_domains=forward_checking(var,color,domains)
            
            if new_domains:
                print(f"{indent}  → Forward checking successful")
                result=backtrack(assignment,new_domains,depth+1)
                if result:
                    return result
                
            #backtrack
            print(f"{indent}  ✗ Backtracking: undoing {var} = {color}")
            del assignment[var]
        else:
            print(f"{indent}  ✗ {color} conflicts with neighbors")
    
    return None


def can_color_with_k_colors(k):
    trial_colors = colors[:k]
    if len(trial_colors) < k:
        trial_colors += [f"Color{i}" for i in range(len(trial_colors) + 1, k + 1)]

    def quiet_backtrack(assignment):
        if len(assignment) == len(graph):
            return True

        for var in graph:
            if var not in assignment:
                break

        for color in trial_colors:
            if is_safe(var, color, assignment):
                assignment[var] = color
                if quiet_backtrack(assignment):
                    return True
                del assignment[var]
        return False

    return quiet_backtrack({})


def find_min_colors_required():
    for k in range(1, len(graph) + 1):
        if can_color_with_k_colors(k):
            return k
    return len(graph)

def solve_map_coloring():
    print("="*60)
    print("GRAPH COLORING PROBLEM - BACKTRACKING WITH FORWARD CHECKING")
    print("="*60)
    print()
    
    domains={v: list(colors) for v in graph}
    solution=backtrack({},domains)

    print()
    print("="*60)
    if solution:
        print("SOLUTION FOUND:\n")
        for district,color in solution.items():
            print(f"  {district} -> {color}")
        min_colors = find_min_colors_required()
        print(f"\nMINIMUM COLORS REQUIRED: {min_colors}")
    else:
        print("NO SOLUTION FOUND")
    print("="*60)

solve_map_coloring()