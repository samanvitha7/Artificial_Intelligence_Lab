def to_cnf(statement):
    statement = statement.replace(" ", "")

    # Case 1: implication A->B
    if "->" in statement:
        left, right = statement.split("->")
        return { "~" + left, right }

    # Case 2: OR (A v B)
    elif "v" in statement:
        return set(statement.split("v"))

    # Case 3: single literal
    else:
        return {statement}
    
def resolve(c1,c2):
    for x in c1:
        if '~' + x in c2:
            new_clause=(c1-{x}|c2-{'~' +x})
            return new_clause
        if x.startswith('~') and x[1:] in c2:
            new_clause=(c1-{x}|c2-{x[1:]})
            return new_clause
    return None

def resolution(kb,goal):
    clauses=kb + [{'~'+ goal}]

    while True:
        new_clauses=[]

        for i in range(len(clauses)):
            for j in range(i+1,len(clauses)):
                resolvent=resolve(clauses[i],clauses[j])

                if resolvent is not None:
                    if len(resolvent)==0:
                        print("goal found")
                        return True
                    
                    if resolvent not in clauses:
                        new_clauses.append(resolvent)

        if not new_clauses:
            print("goal is false")
            return False
        
        clauses.extend(new_clauses)

print("Question-A")

statements_a = [
    "P v Q",
    "P->R",
    "Q->S",
    "R->S"
]

kb_a = []
for s in statements_a:
    kb_a.append(to_cnf(s))

resolution(kb_a, "S")

print("\nQuestion-B")

statements_b = [
    "P->Q",
    "Q->R",
    "S->~R",
    "P"
]

kb_b = []
for s in statements_b:
    kb_b.append(to_cnf(s))

resolution(kb_b, "S")