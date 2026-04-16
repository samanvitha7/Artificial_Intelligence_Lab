class State:
    def __init__(self,loc,A,B):
        self.loc=loc #A or B
        self.A=A  #C or D
        self.B=B

    # Equality/hash are needed so path-based cycle detection works in graph search.
    def __eq__(self, other):
        return isinstance(other, State) and (self.loc, self.A, self.B) == (other.loc, other.A, other.B)

    def __hash__(self):
        return hash((self.loc, self.A, self.B))

    def __repr__(self):
        return f"State(loc={self.loc}, A={self.A}, B={self.B})"

    def goal_test(state):
        return state.A=='C' and state.B=='C'
    
    def actions(state):
        return ['SUCK','LEFT','RIGHT']
    
    def results(state, action):
        outcomes = []

        if action == 'SUCK':
            if state.loc == 'A':
                if state.A == 'D':
                    # clean A, maybe clean B
                    outcomes.append(State('A', 'C', state.B))
                    outcomes.append(State('A', 'C', 'C'))
                else:
                    # on a clean square, dirt may be deposited (or no change).
                    outcomes.append(State('A', 'D', state.B))
                    outcomes.append(State('A', state.A, 'D'))
                    outcomes.append(State('A', state.A, state.B))

            elif state.loc == 'B':
                if state.B == 'D':
                    outcomes.append(State('B', state.A, 'C'))
                    outcomes.append(State('B', 'C', 'C'))
                else:
                    outcomes.append(State('B', state.A, 'D'))
                    outcomes.append(State('B', 'D', state.B))
                    outcomes.append(State('B', state.A, state.B))

        elif action == 'LEFT':
            outcomes.append(State('A', state.A, state.B))

        elif action == 'RIGHT':
            outcomes.append(State('B', state.A, state.B))

        return outcomes
    



def or_search(state, path, trace=None, depth=0):
    if trace is not None:
        trace['or_nodes'] += 1
        trace['max_depth'] = max(trace['max_depth'], depth)

    if State.goal_test(state):
        return []

    if state in path:
        if trace is not None:
            trace['cycles'] += 1
        return None

    for action in State.actions(state):
        if trace is not None:
            trace['action_trials'] += 1
        result_states = State.results(state, action)
        plan = and_search(result_states, path + [state], trace, depth + 1)
        
        if plan is not None:
            return [action, plan]

    return None


def and_search(states, path, trace=None, depth=0):
    if trace is not None:
        trace['and_nodes'] += 1
        trace['max_depth'] = max(trace['max_depth'], depth)
        trace['outcome_branches'] += len(states)

    plan = []
    
    for s in states:
        p = or_search(s, path, trace, depth)
        if p is None:
            return None
        plan.append(p)
    
    return plan


def print_plan(plan, indent=0):
    space = " " * indent
    if plan is None:
        print(space + "No conditional plan found")
        return
    if plan == []:
        print(space + "Goal reached")
        return

    action, subplans = plan
    print(space + f"Action: {action}")
    for i, sp in enumerate(subplans, start=1):
        print(space + f" Outcome {i}:")
        print_plan(sp, indent + 4)


def print_plan_detailed(state, plan, indent=0, depth=0):
    space = " " * indent
    print(space + f"[OR depth={depth}] state: {state}")

    if plan is None:
        print(space + "  No conditional plan found")
        return

    if plan == []:
        print(space + "  Goal reached")
        return

    action, subplans = plan
    outcomes = State.results(state, action)

    print(space + f"  Choose action: {action}")
    print(space + f"  [AND] outcomes: {len(outcomes)}")

    for i, next_state in enumerate(outcomes, start=1):
        print(space + f"   Outcome {i} -> {next_state}")
        subplan = subplans[i - 1] if i - 1 < len(subplans) else None
        print_plan_detailed(next_state, subplan, indent + 4, depth + 1)


if __name__ == "__main__":
    # Example start: agent at A and both tiles dirty.
    initial_state = State('A', 'D', 'D')
    trace = {
        'or_nodes': 0,
        'and_nodes': 0,
        'action_trials': 0,
        'outcome_branches': 0,
        'cycles': 0,
        'max_depth': 0,
    }
    solution = or_search(initial_state, [], trace)

    print("Initial state:", initial_state)
    print("Conditional plan from AND-OR search:")
    print_plan(solution)

    print("\nExpanded trace:")
    print_plan_detailed(initial_state, solution)

    print("\nSearch statistics:")
    print(" OR nodes visited:", trace['or_nodes'])
    print(" AND nodes visited:", trace['and_nodes'])
    print(" Action trials:", trace['action_trials'])
    print(" Outcome branches expanded:", trace['outcome_branches'])
    print(" Cycles avoided:", trace['cycles'])
    print(" Max depth reached:", trace['max_depth'])
