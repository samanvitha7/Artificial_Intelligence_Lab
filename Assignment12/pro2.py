from collections import deque


# Input Sudoku
grid = [
[0,0,0,0,0,6,0,0,0],
[0,5,9,0,0,0,0,0,8],
[2,0,0,0,0,8,0,0,0],
[0,4,5,0,0,0,0,0,0],
[0,0,3,0,0,0,0,0,0],
[0,0,6,0,0,3,0,5,0],
[0,0,0,0,0,7,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,5,0,0,0,2]
]

# Toggle detailed trace output for explanation/demo.
VERBOSE = True
TRACE_STEP_LIMIT = 20

#create variables
variables = [(r,c) for r in range(9) for c in range(9)]

#domains
domains={}
for r,c in variables:
    if grid[r][c]!=0:
        domains[(r,c)]={grid[r][c]}
    else:
        domains[(r,c)]=set(range(1,10))

#neighbors
def get_neighbors(cell):
    r,c=cell
    neighbors=set()
    #row and column
    for i in range(9):
        if i!=c:
            neighbors.add((r,i))
        if i!=r:
            neighbors.add((i,c))

    #box
    br, bc = 3*(r//3), 3*(c//3)
    for i in range(br, br+3):
        for j in range(bc, bc+3):
            if (i,j) != cell:
                neighbors.add((i,j))

    return neighbors

neighbors = {v: get_neighbors(v) for v in variables}

def generate_all_arcs():
    arcs = deque()
    for xi in variables:
        for xj in neighbors[xi]:
            arcs.append((xi, xj))
    return arcs

def domain_sizes_grid():
    return [[len(domains[(r, c)]) for c in range(9)] for r in range(9)]

def print_domain_sizes_grid(title):
    print(f"\n{title}\n")
    sizes = domain_sizes_grid()
    for row in sizes:
        print(" ".join(str(v) for v in row))

def print_singleton_grid(title):
    print(f"\n{title}\n")
    for r in range(9):
        row = []
        for c in range(9):
            cell_domain = domains[(r, c)]
            if len(cell_domain) == 1:
                row.append(str(next(iter(cell_domain))))
            else:
                row.append(".")
        print(" ".join(row))

def AC_3():
    arcs = generate_all_arcs()

    removed_count = 0
    step = 0
    revised_arcs = 0

    if VERBOSE:
        print("\n===== AC-3 TRACE START =====")
        print(f"Initial queue size: {len(arcs)} arcs")
        print(f"Showing detailed logs for first {TRACE_STEP_LIMIT} steps only.")

    while arcs:
        step += 1
        xi, xj = arcs.popleft()
        revised, removed, removed_vals = revise(xi, xj)
        removed_count += removed

        if VERBOSE and step <= TRACE_STEP_LIMIT:
            print(
                f"Step {step:04d} | Processing arc {xi} <- {xj} | "
                f"|D({xi})|={len(domains[xi])} |D({xj})|={len(domains[xj])}"
            )

        if len(domains[xi]) == 0:
            if VERBOSE:
                print(f"Domain wipeout at {xi}. Puzzle is inconsistent under AC-3.")
                print("===== AC-3 TRACE END =====")
            return False, removed_count

        if revised:
            revised_arcs += 1
            if VERBOSE and step <= TRACE_STEP_LIMIT:
                removed_vals_txt = ", ".join(str(v) for v in sorted(removed_vals))
                print(
                    f"  Revised: removed {{{removed_vals_txt}}} from {xi}. "
                    f"New domain: {sorted(domains[xi])}"
                )
            for xk in neighbors[xi]:
                if xk != xj:
                    arcs.append((xk, xi))
            if VERBOSE and step <= TRACE_STEP_LIMIT:
                print(f"  Re-queued {len(neighbors[xi]) - 1} neighboring arcs due to revision.")

    if VERBOSE:
        print("===== AC-3 TRACE END =====")
        print(f"Total arc-processing steps: {step}")
        print(f"Arcs that caused revision: {revised_arcs}")

    return True, removed_count

def revise(xi, xj):
    to_remove = set()

    for x in domains[xi]:
        # Constraint is xi != xj. If xj can only be x, then x is not allowed in xi.
        if len(domains[xj]) == 1 and x in domains[xj]:
            to_remove.add(x)

    if to_remove:
        domains[xi] -= to_remove
        return True, len(to_remove), to_remove

    return False, 0, set()

print_domain_sizes_grid("Initial Domain Sizes Grid")
result, removed = AC_3()
arc_count = len(generate_all_arcs())

# Print domain sizes
print_domain_sizes_grid("Final Domain Sizes Grid (After AC-3)")
print_singleton_grid("Current Solved Digits Grid ('.' means unresolved)")

print("\nTotal arcs generated:", arc_count)
print("\nValues removed:", removed)
print("Solved?", all(len(domains[v]) == 1 for v in variables))
print("Any domain zero?", any(len(domains[v]) == 0 for v in variables))

