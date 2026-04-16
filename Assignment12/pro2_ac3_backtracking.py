from collections import deque

# Input Sudoku (0 means empty)
grid = [
    [0, 0, 0, 0, 0, 6, 0, 0, 0],
    [0, 5, 9, 0, 0, 0, 0, 0, 8],
    [2, 0, 0, 0, 0, 8, 0, 0, 0],
    [0, 4, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 6, 0, 0, 3, 0, 5, 0],
    [0, 0, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 2],
]

SHOW_TRACE = True
TRACE_STEP_LIMIT = 20

variables = [(r, c) for r in range(9) for c in range(9)]


def get_neighbors(cell):
    r, c = cell
    n = set()

    # Row and column neighbors.
    for i in range(9):
        if i != c:
            n.add((r, i))
        if i != r:
            n.add((i, c))

    # 3x3 box neighbors.
    br, bc = 3 * (r // 3), 3 * (c // 3)
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if (i, j) != cell:
                n.add((i, j))

    return n


neighbors = {v: get_neighbors(v) for v in variables}


def generate_all_arcs():
    arcs = deque()
    for xi in variables:
        for xj in neighbors[xi]:
            arcs.append((xi, xj))
    return arcs


def initialize_domains(initial_grid):
    domains = {}
    for r, c in variables:
        if initial_grid[r][c] != 0:
            domains[(r, c)] = {initial_grid[r][c]}
        else:
            domains[(r, c)] = set(range(1, 10))
    return domains


def copy_domains(domains):
    return {k: set(v) for k, v in domains.items()}


def revise(domains, xi, xj):
    to_remove = set()
    if len(domains[xj]) == 1:
        only_val = next(iter(domains[xj]))
        if only_val in domains[xi]:
            to_remove.add(only_val)

    if to_remove:
        domains[xi] -= to_remove
        return True, len(to_remove), to_remove

    return False, 0, set()


def ac3(domains, show_trace=False, trace_step_limit=20):
    arcs = generate_all_arcs()
    removed_count = 0
    step = 0
    revised_arcs = 0

    if show_trace:
        print("\n===== AC-3 TRACE START =====")
        print(f"Initial queue size: {len(arcs)} arcs")
        print(f"Showing detailed logs for first {trace_step_limit} steps only.")

    while arcs:
        step += 1
        xi, xj = arcs.popleft()
        revised, removed, removed_vals = revise(domains, xi, xj)
        removed_count += removed

        if show_trace and step <= trace_step_limit:
            print(
                f"Step {step:04d} | Processing arc {xi} <- {xj} | "
                f"|D({xi})|={len(domains[xi])} |D({xj})|={len(domains[xj])}"
            )

        if len(domains[xi]) == 0:
            if show_trace:
                print(f"Domain wipeout at {xi}. Puzzle is inconsistent under AC-3.")
                print("===== AC-3 TRACE END =====")
            return False, removed_count, step, revised_arcs

        if revised:
            revised_arcs += 1
            if show_trace and step <= trace_step_limit:
                removed_vals_txt = ", ".join(str(v) for v in sorted(removed_vals))
                print(
                    f"  Revised: removed {{{removed_vals_txt}}} from {xi}. "
                    f"New domain: {sorted(domains[xi])}"
                )
            for xk in neighbors[xi]:
                if xk != xj:
                    arcs.append((xk, xi))
            if show_trace and step <= trace_step_limit:
                print(f"  Re-queued {len(neighbors[xi]) - 1} neighboring arcs due to revision.")

    if show_trace:
        print("===== AC-3 TRACE END =====")

    return True, removed_count, step, revised_arcs


def domain_sizes_grid(domains):
    return [[len(domains[(r, c)]) for c in range(9)] for r in range(9)]


def print_domain_sizes_grid(domains, title):
    print(f"\n{title}\n")
    for row in domain_sizes_grid(domains):
        print(" ".join(str(v) for v in row))


def print_singleton_grid(domains, title):
    print(f"\n{title}\n")
    for r in range(9):
        row = []
        for c in range(9):
            d = domains[(r, c)]
            row.append(str(next(iter(d))) if len(d) == 1 else ".")
        print(" ".join(row))


def is_solved(domains):
    return all(len(domains[v]) == 1 for v in variables)


def has_empty_domain(domains):
    return any(len(domains[v]) == 0 for v in variables)


def select_unassigned_mrv(domains):
    candidates = [v for v in variables if len(domains[v]) > 1]
    if not candidates:
        return None
    return min(candidates, key=lambda v: len(domains[v]))


def backtrack(domains, stats):
    if has_empty_domain(domains):
        return None
    if is_solved(domains):
        return domains

    var = select_unassigned_mrv(domains)
    if var is None:
        return domains

    for value in sorted(domains[var]):
        stats["guesses"] += 1
        new_domains = copy_domains(domains)
        new_domains[var] = {value}

        consistent, _, _, _ = ac3(new_domains, show_trace=False)
        if consistent:
            result = backtrack(new_domains, stats)
            if result is not None:
                return result

        stats["backtracks"] += 1

    return None


def print_solved_grid(domains, title):
    print(f"\n{title}\n")
    for r in range(9):
        row = [str(next(iter(domains[(r, c)]))) for c in range(9)]
        print(" ".join(row))


def main():
    domains = initialize_domains(grid)

    print_domain_sizes_grid(domains, "Initial Domain Sizes Grid")

    consistent, removed, steps, revised_arcs = ac3(
        domains, show_trace=SHOW_TRACE, trace_step_limit=TRACE_STEP_LIMIT
    )

    arc_count = len(generate_all_arcs())

    print_domain_sizes_grid(domains, "Final Domain Sizes Grid (After AC-3)")
    print_singleton_grid(domains, "Current Solved Digits Grid ('.' means unresolved)")

    print(f"\nTotal arcs generated: {arc_count}")
    print(f"Values removed by AC-3: {removed}")
    print(f"Arc-processing steps: {steps}")
    print(f"Arcs that caused revision: {revised_arcs}")
    print(f"Solved by AC-3 only? {is_solved(domains)}")
    print(f"Any domain zero after AC-3? {has_empty_domain(domains)}")

    if not consistent:
        print("\nAC-3 found inconsistency. No solution under current constraints.")
        return

    if is_solved(domains):
        print_solved_grid(domains, "Solved Sudoku Grid")
        return

    print("\nStarting backtracking search with MRV + AC-3 propagation...")
    stats = {"guesses": 0, "backtracks": 0}
    solution = backtrack(domains, stats)

    if solution is None:
        print("No complete solution found by backtracking.")
        return

    print_solved_grid(solution, "Solved Sudoku Grid (After Backtracking)")
    print(f"\nBacktracking guesses tried: {stats['guesses']}")
    print(f"Backtracks: {stats['backtracks']}")


if __name__ == "__main__":
    main()
