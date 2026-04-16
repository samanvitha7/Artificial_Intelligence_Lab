import random
import itertools

#defining cities and costs
cities = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

cost_matrix = [
    [0, 10, 15, 20, 25, 30, 35, 40],
    [12, 0, 35, 15, 20, 25, 30, 45],
    [25, 30, 0, 10, 40, 20, 15, 35],
    [18, 25, 12, 0, 15, 30, 20, 10],
    [22, 18, 28, 20, 0, 15, 25, 30],
    [35, 22, 18, 28, 12, 0, 40, 20],
    [30, 35, 22, 18, 28, 32, 0, 15],
    [40, 28, 35, 22, 18, 25, 12, 0]
]

def calculate_cost(tour):
    total_cost=0
    for i in range(len(tour)-1):
        total_cost+=cost_matrix[tour[i]][tour[i+1]]
    total_cost+=cost_matrix[tour[-1]][tour[0]]  #return to start
    return total_cost

#genrating random tour
def random_tour():
    tour=list(range(len(cities)))
    random.shuffle(tour)
    return tour

#generating neighbors by swapping two cities
def generate_neighbours(tour):
    neighbours=[]
    for i in range(len(tour)):
        for j in range(i+1,len(tour)):
            new_tour=tour[:]
            new_tour[i],new_tour[j]=new_tour[j],new_tour[i]
            neighbours.append(new_tour)
    return neighbours


def local_beam_search(k, max_iterations=100):
    print(f"Running Local Beam Search with beam width k = {k}")
    
    # Initialize k random tours
    beam = [random_tour() for _ in range(k)]
    
    print("\nInitial Beam States:")
    for i, state in enumerate(beam):
        print(f"State {i+1}: {[cities[x] for x in state]} | Cost = {calculate_cost(state)}")
    
    best_cost = float('inf')
    best_tour = None
    
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        all_neighbors = []
        
        # Generate neighbors of all beam states
        for state in beam:
            neighbors = generate_neighbours(state)
            all_neighbors.extend(neighbors)
        
        # Sort all neighbors by cost
        all_neighbors.sort(key=lambda x: calculate_cost(x))
        
        # Select best k neighbors
        beam = all_neighbors[:k]
        
        current_best_tour = beam[0]
        current_best_cost = calculate_cost(current_best_tour)
        
        print(f"\nIteration {iteration}")
        print(f"Best Cost in this iteration: {current_best_cost}")
        print("Best Path in this iteration: " + " → ".join([cities[x] for x in current_best_tour]) + " → " + cities[current_best_tour[0]])
        
        # Check convergence
        if current_best_cost < best_cost:
            best_cost = current_best_cost
            best_tour = current_best_tour
        else:
            print("No improvement. Algorithm converged.")
            break
    
    print("\nFinal Best Tour:")
    print(" → ".join([cities[x] for x in best_tour]) + " → " + cities[best_tour[0]])
    print(f"Final Cost: {best_cost}")
    print(f"Total Iterations: {iteration}")
    
    return best_cost



results = {}

for k in [3, 5, 10]:
    best_cost = local_beam_search(k)
    results[k] = best_cost

print("Comparative Analysis")


print("Comparative Analysis of Beam Width (k)")
print("{:<10} {:<25} {:<25}".format("k", "Convergence Speed", "Solution Quality / Behavior"))


analysis = {
    3: ("Fast", "May get stuck in local minimum"),
    5: ("Moderate", "Balanced exploration and solution quality"),
    10: ("Slower", "Better solution, more computation")
}

for k in [3, 5, 10]:
    print("{:<10} {:<25} {:<25}".format(
        k,
        analysis[k][0],
        analysis[k][1]
    ))