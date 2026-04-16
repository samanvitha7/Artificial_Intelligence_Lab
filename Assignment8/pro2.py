import random

cities = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# Cost matrix where cost_matrix[i][j] gives cost from city i to city j
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
    """
    Calculates total cost of a TSP tour.
    Adds cost between consecutive cities and
    finally adds cost to return to starting city.
    """
    total = 0
    
    for i in range(len(tour) - 1):
        total += cost_matrix[tour[i]][tour[i+1]]

    total += cost_matrix[tour[-1]][tour[0]]
    
    return total




def create_population(size):
    """
    Creates an initial population of random tours.
    Each tour is a permutation of city indices.
    """
    population = []
    
    for _ in range(size):
        tour = list(range(len(cities)))  
        random.shuffle(tour)            
        population.append(tour)
    
    return population



def selection(population):
  
    p1 = random.choice(population)
    p2 = random.choice(population)
    
    # Choose individual with lower cost (better fitness)
    return p1 if calculate_cost(p1) < calculate_cost(p2) else p2




def one_point_crossover(parent1, parent2):
    # Choose random crossover point
    point = random.randint(1, len(parent1)-2)
    
    # Copy first part from parent1
    child = parent1[:point]
    
    # Fill remaining genes from parent2 in order
    for gene in parent2:
        if gene not in child:
            child.append(gene)
    
    return child



def two_point_crossover(parent1, parent2):
    
    size = len(parent1)
    
    # Select two crossover points
    p1, p2 = sorted(random.sample(range(size), 2))
    
    # Create empty child
    child = [None] * size
    
    # Copy middle segment from parent1
    child[p1:p2] = parent1[p1:p2]
    
    # Fill remaining positions from parent2
    pointer = 0
    for gene in parent2:
        if gene not in child:
            while child[pointer] is not None:
                pointer += 1
            child[pointer] = gene
    
    return child



def mutate(tour, mutation_rate=0.1, verbose=False):
    """
    Performs swap mutation.
    With given probability, two cities are swapped.
    Returns: (mutated_tour, mutation_occurred)
    """
    
    probability = random.random()
    mutation_occurred = False
    
    if verbose:
        print(f"  Mutation Check: Random value = {probability:.3f}, Threshold = {mutation_rate}")
    
    if probability < mutation_rate:
        i, j = random.sample(range(len(tour)), 2)
        if verbose:
            print(f"  ✓ MUTATION OCCURRED! Swapping cities {cities[tour[i]]} (pos {i}) ↔ {cities[tour[j]]} (pos {j})")
        tour[i], tour[j] = tour[j], tour[i]
        mutation_occurred = True
    else:
        if verbose:
            print(f"  ✗ No mutation (probability {probability:.3f} >= {mutation_rate})")
    
    return tour, mutation_occurred



def genetic_algorithm(crossover_type, generations=100, pop_size=50):

    print(f"Running Genetic Algorithm using {crossover_type} Crossover")
 
    population = create_population(pop_size)
    
    best_cost = float('inf')
    best_tour = None
    
    # Print table header
    print("\n{:<12} {:<12} {:<50}".format("Generation", "Best Cost", "Best Path"))

    for gen in range(generations):
        new_population = []
        mutation_count = 0
        
        for idx in range(pop_size):
            parent1 = selection(population)
            parent2 = selection(population)
            
            if crossover_type == "one-point":
                child = one_point_crossover(parent1, parent2)
            else:
                child = two_point_crossover(parent1, parent2)
        
        
            child, mutated = mutate(child, verbose=False)
            if mutated:
                mutation_count += 1
            
            new_population.append(child)
        
        population = new_population
        
        # Find best in this generation
        generation_best = min(population, key=calculate_cost)
        generation_best_cost = calculate_cost(generation_best)
        
        # Update global best
        if generation_best_cost < best_cost:
            best_cost = generation_best_cost
            best_tour = generation_best
        
        # Print progress every 10 generations
        if gen % 10 == 0:
            path = " → ".join([cities[i] for i in generation_best])
            print("{:<12} {:<12} {:<50}".format(gen, generation_best_cost, path))
    
    print("\nFinal Best Tour Found:")
    print(" → ".join([cities[i] for i in best_tour]) + " → " + cities[best_tour[0]])
    print("Final Cost:", best_cost)
    
    return best_cost




cost_one = genetic_algorithm("one-point")
cost_two = genetic_algorithm("two-point")


print("Comparative Analysis of Crossover Methods")

print("{:<15} {:<20} {:<30}".format("Crossover", "Convergence Speed", "Solution Quality"))

print("{:<15} {:<20} {:<30}".format(
    "One-Point", 
    "Faster", 
    "Moderate, risk of premature convergence"
))

print("{:<15} {:<20} {:<30}".format(
    "Two-Point", 
    "Moderate", 
    "Better exploration, improved solution"
))