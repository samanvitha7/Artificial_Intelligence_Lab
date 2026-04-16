def solve():
    variables = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']

    # Initial domains
    domains = {v: set(range(10)) for v in variables}

    # Constraint propagation (pre-processing)
    domains['M'] = {1}  # In SEND + MORE = MONEY, carry into a new leftmost digit forces M = 1.
    domains['O'] = {0}  # With M = 1, MONEY starts with 10..., so the ten-thousands carry implies O = 0.
    domains['S'] -= {0}

    step_counter = [0]  # mutable counter shared with nested function

    def is_valid(sol):
        if len(sol) == 8:
            S, E, N, D, M, O, R, Y = [sol[v] for v in variables]

            SEND = 1000 * S + 100 * E + 10 * N + D
            MORE = 1000 * M + 100 * O + 10 * R + E
            MONEY = 10000 * M + 1000 * O + 100 * N + 10 * E + Y

            return SEND + MORE == MONEY
        return True

    def forward_check(var, value, current_domains):
        new_domains = {v: current_domains[v].copy() for v in current_domains}

        # Remove assigned value from all other domains
        for v in new_domains:
            if v != var and value in new_domains[v]:
                new_domains[v].remove(value)
                if not new_domains[v]:
                    return None  # Domain wiped out -> failure

        return new_domains

    def format_domain_snapshot(sol, current_domains):
        # Show only unassigned variable domains in variable order.
        parts = []
        for v in variables:
            if v not in sol:
                parts.append(f"{v}:{sorted(current_domains[v])}")
        return " | ".join(parts)

    def backtrack(sol, current_domains, depth=0):
        if len(sol) == len(variables):
            if is_valid(sol):
                return sol
            return None

        # Select first unassigned variable
        var = next(v for v in variables if v not in sol)

        for value in current_domains[var]:
            if value in sol.values():
                continue

            step_counter[0] += 1
            if step_counter[0] <= 3:
                indent = "  " * depth
                print(f"{indent}Step {step_counter[0]} | Depth {depth}: trying {var} = {value}")
                print(f"{indent}Assignment: {sol}")
                print(f"{indent}Remaining domains: {format_domain_snapshot(sol, current_domains)}")

            # Assign
            sol[var] = value

            # Forward checking
            new_domains = forward_check(var, value, current_domains)
            if new_domains is not None:
                if step_counter[0] <= 3:
                    print(f"{indent}Forward check: pass")
                result = backtrack(sol, new_domains, depth + 1)
                if result:
                    return result
            else:
                if step_counter[0] <= 3:
                    print(f"{indent}Forward check: fail")

            # Backtrack
            if step_counter[0] <= 3:
                print(f"{indent}Backtracking from {var} = {value}\n")
            del sol[var]

        return None

    return backtrack({}, domains)


# Run
solution = solve()
print(solution)
if solution:
    S, E, N, D, M, O, R, Y = [solution[v] for v in ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']]
    SEND = 1000 * S + 100 * E + 10 * N + D
    MORE = 1000 * M + 100 * O + 10 * R + E
    MONEY = 10000 * M + 1000 * O + 100 * N + 10 * E + Y
    print(f"{SEND} + {MORE} = {MONEY}")
