import itertools  #gives permutations

letters = ('S','E','N','D','M','O','R','Y')
digits=range(10) #doamin

for permutation in itertools.permutations(digits,len(letters)):
    S,E,N,D,M,O,R,Y=permutation

    if S==0 or M==0:
        continue

    SEND=1000*S + 100*E + 10*N + D
    MORE=1000*M + 100*O + 10*R + E
    MONEY=10000*M + 1000*O + 100*N + 10*E + Y

    if SEND + MORE == MONEY:
        print("Solution found:")
        print(f"S={S}, E={E}, N={N}, D={D}")
        print(f"M={M}, O={O}, R={R}, Y={Y}")
        print(f"{SEND} + {MORE} = {MONEY}")
        break