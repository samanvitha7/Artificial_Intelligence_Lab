# Graph representation
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


# Check if assignment is valid
def is_safe(node, color, assignment):
    for neighbor in graph[node]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True


# MRV: select variable with minimum remaining values
def select_unassigned_variable(assignment, domains):
    unassigned = [v for v in graph if v not in assignment]
    
    # choose variable with smallest domain
    return min(unassigned, key=lambda var: len(domains[var]))


# Forward Checking
def forward_checking(node, color, domains):
    new_domains = {v: list(domains[v]) for v in domains}

    for neighbor in graph[node]:
        if color in new_domains[neighbor]:
            new_domains[neighbor].remove(color)

            if not new_domains[neighbor]:
                return None

    return new_domains


# Backtracking
def backtrack(assignment, domains):
    if len(assignment) == len(graph):
        return assignment

    # MRV used here
    var = select_unassigned_variable(assignment, domains)

    for color in domains[var]:
        if is_safe(var, color, assignment):
            assignment[var] = color

            new_domains = forward_checking(var, color, domains)

            if new_domains:
                result = backtrack(assignment, new_domains)
                if result:
                    return result

            del assignment[var]  # backtrack

    return None


# Solve
def solve_map_coloring():
    domains = {v: list(colors) for v in graph}
    solution = backtrack({}, domains)

    if solution:
        print("Solution found:\n")
        for district, color in solution.items():
            print(district, "->", color)
    else:
        print("No solution found")


solve_map_coloring()

"""
MRV  picks districts with fewest colors left
ensuring that the most constrained variable is assigned first, which helps reduce backtracking
"""