from collections import deque

variables = ["P1", "P2", "P3", "P4", "P5", "P6"]

# constraints(neighbours)
neighbors = {
    "P1": ["P2", "P3", "P6"],
    "P2": ["P1", "P3", "P4"],
    "P3": ["P1", "P2", "P5"],
    "P4": ["P2", "P6"],
    "P5": ["P3", "P6"],
    "P6": ["P1", "P4", "P5"],
}


def initial_domains():
    return {v: ["R1", "R2", "R3"] for v in variables}


# Constraint: Xi != Xj
def revise(domains, Xi, Xj):
    revised = False
    removed_values = []

    for x in domains[Xi][:]:
        # Keep x only if there is at least one supporting value in Xj.
        if not any(x != y for y in domains[Xj]):
            domains[Xi].remove(x)
            revised = True
            removed_values.append(x)

    return revised, removed_values


def AC_3(domains, trace_limit=10):
    queue = deque()

    # Add all initial arcs to the queue
    for Xi in variables:
        for Xj in neighbors[Xi]:
            queue.append((Xi, Xj))

    trace = []
    checks = 0
    limit_reached_msg = False

    while queue:
        Xi, Xj = queue.popleft()
        checks += 1

        # Stop tracing if limit is exceeded, but continue the algorithm
        if checks > trace_limit:
            if not limit_reached_msg:
                trace.append(f"...\n[Trace limit of {trace_limit} reached, continuing algorithm without printing]...\n")
                limit_reached_msg = True
            
            revised, _ = revise(domains, Xi, Xj)
            if revised:
                if len(domains[Xi]) == 0:
                    return False, trace
                for Xk in neighbors[Xi]:
                    if Xk != Xj:
                        queue.append((Xk, Xi))
            continue # Go to the next item in the queue

        # --- Detailed Tracing ---
        xi_before = domains[Xi][:]
        xj_before = domains[Xj][:]

        revised, removed_values = revise(domains, Xi, Xj)
        xi_after = domains[Xi][:]

        step_trace = f"Arc ({Xi}, {Xj}) processed from queue.\n"
        step_trace += f"  - Domain of {Xi} before revise: {xi_before}\n"
        step_trace += f"  - Domain of {Xj} (context):    {xj_before}\n"

        if revised:
            step_trace += f"  - Action: Domain of {Xi} was revised.\n"
            step_trace += f"  - Removed values: {removed_values}\n"
            step_trace += f"  - Domain of {Xi} after revise:  {xi_after}\n"

            if len(domains[Xi]) == 0:
                step_trace += f"  - Result: Domain of {Xi} is empty. Inconsistency found.\n"
                trace.append(step_trace)
                return False, trace

            # Explicitly show which arcs are being added back to the queue
            added_to_queue = []
            for Xk in neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
                    added_to_queue.append(f"({Xk}, {Xi})")
            
            if added_to_queue:
                step_trace += f"  - Consequence: Adding arcs to queue: {', '.join(added_to_queue)}\n"
        else:
            step_trace += "  - Action: No changes made to the domain of {Xi}.\n"

        trace.append(step_trace)

    return True, trace


print(" Case 1: Initial domains for all teams ")
domains_case1 = initial_domains()
result1, trace1 = AC_3(domains_case1, trace_limit=10)

print("\nAC-3 Algorithm Trace for Case 1 ")
for step_no, step in enumerate(trace1, start=1):
    print(f"Step {step_no}:")
    print(step)

print("\nFinal Result for Case 1 ")
print(f"Arc Consistent: {result1}")
print(f"Domains after AC-3: {domains_case1}")
print("\n")


print("Case 2: Pre-assign P1 = R1 and check arc consistency ")
domains_case2 = initial_domains()
domains_case2["P1"] = ["R1"]
print(f"Initial state: Domain of P1 is restricted to ['R1']\n")
result2, trace2 = AC_3(domains_case2, trace_limit=10)

print(" AC-3 Algorithm Trace for Case 2 ")
for step_no, step in enumerate(trace2, start=1):
    print(f"Step {step_no}:")
    print(step)

print("\nFinal Result for Case 2 ")
print(f"Arc Consistent: {result2}")
print(f"Domains after AC-3: {domains_case2}")


