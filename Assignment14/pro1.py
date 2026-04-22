def forward_check(rules,facts,goal):
    #initialize inferred table
    inferred={}
    #collect all symbols

    for rule in rules:
        premise=rule[0]
        conclusion=rule[1]
        inferred[conclusion]=False

        for p in premise:
            inferred[p]=False
    for fact in facts:
        inferred[fact]=False
    
    count=[]
    for rule in rules:
        count.append(len(rule[0]))

    queue=facts[:]
    while queue:
        p=queue.pop()
        if p==goal:
            print("goal reached")
            return True
        
        if inferred[p]==False:
            inferred[p]=True

            for rule in rules:
                premise=rule[0]
                conclusion=rule[1]

                if p in premise:
                    count[rules.index(rule)]-=1
                    if count[rules.index(rule)]==0:
                        queue.append(conclusion)
    print("goal not reached")


#inputs
print("Question-A")
rules_a = [
    (['P'], 'Q'),
    (['L', 'M'], 'P'),
    (['A', 'B'], 'L')
]

facts_a = ['A', 'B', 'M']
goal_a = 'Q'
forward_check(rules_a,facts_a,goal_a)

print("\nQuestion-B")

rules_b = [
    (['A'], 'B'),
    (['B'], 'C'),
    (['C'], 'D'),
    (['D', 'E'], 'F')
]

facts_b = ['A', 'E']
goal_b = 'F'

forward_check(rules_b, facts_b, goal_b)

            






















