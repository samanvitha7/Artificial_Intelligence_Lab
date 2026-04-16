def solve():
    variables = ['S','E','N','D','M','O','R','Y']
    
    # Initial domains
    domains = {v: set(range(10)) for v in variables}
    
    # Constraint propagation (pre-processing)
    domains['M'] = {1}
    domains['O'] = {0}
    domains['S'] -= {0}
    
    solution = {}
    
    def is_valid(sol):
        if len(sol) == 8:
            S,E,N,D,M,O,R,Y = [sol[v] for v in variables]
            
            SEND = 1000*S + 100*E + 10*N + D
            MORE = 1000*M + 100*O + 10*R + E
            MONEY = 10000*M + 1000*O + 100*N + 10*E + Y
            
            return SEND + MORE == MONEY
        return True
    
    def forward_check(var, value, domains):
        new_domains = {v: domains[v].copy() for v in domains}
        
        # Remove assigned value from other domains
        for v in new_domains:
            if v != var and value in new_domains[v]:
                new_domains[v].remove(value)
                if not new_domains[v]:
                    return None  # Domain wiped → fail
        
        return new_domains
    
    def backtrack(sol, domains):
        if len(sol) == len(variables):
            if is_valid(sol):
                return sol
            return None
        
        # Select unassigned variable (simple order)
        var = next(v for v in variables if v not in sol)
        
        for value in domains[var]:
            if value in sol.values():
                continue
            
            # Assign
            sol[var] = value
            
            # Forward checking
            new_domains = forward_check(var, value, domains)
            if new_domains is not None:
                result = backtrack(sol, new_domains)
                if result:
                    return result
            
            # Backtrack
            del sol[var]
        
        return None
    
    return backtrack({}, domains)


# Run
solution = solve()
print(solution)
if solution:
    S,E,N,D,M,O,R,Y = [solution[v] for v in ['S','E','N','D','M','O','R','Y']]
    SEND = 1000*S + 100*E + 10*N + D
    MORE = 1000*M + 100*O + 10*R + E
    MONEY = 10000*M + 1000*O + 100*N + 10*E + Y
    print(f"{SEND} + {MORE} = {MONEY}")