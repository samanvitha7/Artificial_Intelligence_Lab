def backward_check(goal,facts,kb_rules):
    if goal in facts:
        return True
    
    for rule in kb_rules:
        premise=rule[0]
        conclusion=rule[1]

        if conclusion==goal:
            all_premises=True
            for p in premise:
                if not backward_check(p,facts,kb_rules):
                    all_premises=False
                    break
            if all_premises:
                return True
            
    return False

print("Question-A")

rules_a = [
    (['P'], 'Q'),
    (['R'], 'Q'),
    (['A'], 'P'),
    (['B'], 'R')
]

facts_a = ['A', 'B']
goal_a = 'Q'

if backward_check(goal_a, facts_a, rules_a):
    print("Goal reached")
else:
    print("Goal not reached")

print("\nQuestion-B")

rules_b = [
    (['A'], 'B'),
    (['B', 'C'], 'D'),
    (['E'], 'C')
]

facts_b = ['A', 'E']
goal_b = 'D'

if backward_check(goal_b, facts_b, rules_b):
    print("Goal reached")
else:
    print("Goal not reached")
