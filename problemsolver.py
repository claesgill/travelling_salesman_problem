import csv
import time
import itertools as it
import numpy as np
from timer_decorator import time_it, time_it_return, time_it_simple
import matplotlib.pyplot as plt
import math

def format_data(data):
    cities_matrix = []
    for i in range(1, number_cities+1):
        cities_matrix.append(data[i][:number_cities])
    print("Data formatted!")
    return np.array(cities_matrix)

def load_data():
    with open("cities.csv", "r") as f: 
        data = np.array(list(csv.reader(f, delimiter=';')))
        print("Data loaded!")
    return data

number_cities = 24
data   = load_data()
cities = format_data(data)

def get_distance_between_two_cities(cities_matrix, start, stop):
    return float(cities_matrix[start, stop])

def get_route_distance(route):
    distance = []
    for i in range(1, len(route)):
        distance.append(get_distance_between_two_cities(cities, route[i-1], route[i]))
    distance.append(get_distance_between_two_cities(cities, route[-1], route[0]))
    return sum(distance)

def get_permutations():
    # return list(it.permutations(data[0][:number_cities], number_cities))
    permutations = [i for i in range(number_cities)]
    return list(it.permutations(permutations))

def get_number_of_permutation(sample_size):
    permutations_list = []
    numb_permutations = [i for i in range(number_cities)]
    random_start = np.random.randint(math.factorial(10))
    permutations_iterator = it.permutations(numb_permutations)
    for _ in range(random_start):
        next(permutations_iterator)
    for i in range(sample_size):
        permutations_list.append(next(permutations_iterator))
    return permutations_list

@time_it_return
def exhaustive_search():
    permutations = get_permutations()
    min_distance = 10000000
    for i in range(len(permutations)):
        new_distance = get_route_distance(permutations[i])
        if new_distance < min_distance:
            min_distance = new_distance
    return int(min_distance)

@time_it_return
def hill_climb(numb_swaps):
    permutations = get_permutations()
    
    # 1) Starte et random sted i data-sett og kalkulere rute
    # 2) Sammenligne med nabo-node til høyre/venstre og velg beste
    # 3) Fortsett frem til funnet den beste
    index = np.random.randint(len(permutations))
    random_route_dist = get_route_distance(permutations[index])
    random_route = list(permutations[index])
    # print(f"Starting route: {int(random_route_dist)} - {random_route}")
    for i in range(numb_swaps):
        city1 = np.random.randint(number_cities)
        city2 = np.random.randint(number_cities)
        new_route = random_route
        new_route[city1], new_route[city2] = new_route[city2], new_route[city1]
        new_route_dist = get_route_distance(new_route)

        if new_route_dist < random_route_dist:
            random_route_dist = new_route_dist
            random_route = new_route

    # print(f"Ending route: {int(random_route_dist)} - {random_route}")
    return int(random_route_dist)

########
## GA ##
########
def initialize_population(population_size):
    # TODO: velg random populasjon
    population = get_number_of_permutation(population_size)
    np.random.shuffle(population)
    return population[:population_size]

def evaluate_population(population):
    fitness = []
    for route in population:
        distance = get_route_distance(route)
        fitness.append(distance)
    return fitness

def get_best_route_in_population(fitness):
    return max(fitness)

def select_parents_based_on_fitness(population, fitness, num_parents):
    # TODO: Kanskje ta med noen tilfeldige som foreldre ikke bare de beste..?
    parents = []
    sorted_fitness = np.argsort(fitness)
    for i in range(num_parents):
        parents.append(population[sorted_fitness[i]])
    return parents

def order_crossover(parent1, parent2):
    random_point = np.random.randint(len(parent1))
    child1 = list(parent1[:random_point])
    child2 = list(parent2[:random_point])
    for i in range(len(parent1)):
        if parent2[i] not in child1:
            child1.append(parent2[i])
        if parent1[i] not in child2:
            child2.append(parent1[i])
    return child1, child2

def swap_mutation(persentage, child):
    if persentage >= np.random.rand():
        random_index1 = np.random.randint(len(child))
        random_index2 = np.random.randint(len(child))
        child[random_index1], child[random_index2] = child[random_index2], child[random_index1]
        return child
    return child

def get_fitness_stats(fitness):
    fitness = np.array(fitness)
    return np.mean(fitness), np.max(fitness), np.min(fitness)

def print_prosentage_done(num_generations, generations):
    percentage = (generations * 100) / num_generations
    if percentage == 100:
        print(f"{int(percentage)}%")
    else:
        print(f"{int(percentage)}%", end="\r")

def genetic_algorithm(population_size, num_generations, num_parents, num_childs, mutation_rate):
    print("Initializing the Genetic Algoritm")
    l_mean    = []
    l_maximum = []
    l_minimum = []
    generations = 0
    # Initialize population
    population = initialize_population(population_size)
    # Evaluate population
    fitness = evaluate_population(population)
    # Find best solution
    best = get_best_route_in_population(fitness)
    # While stopcondition
    while generations < num_generations:
        # Select parents
        parents = select_parents_based_on_fitness(population, fitness, num_parents)
        # Create children
        children = []
        # For parent1 and parent2 in parents
        for i in range(1, len(parents)):
            # Create children by crossover
            parent1 = parents[i-1] # TODO: kan randomize valg av foreldre
            parent2 = parents[i]
            child1, child2 = order_crossover(parent1, parent2)
            # Mutate childs
            child1 = swap_mutation(mutation_rate, child1)
            child2 = swap_mutation(mutation_rate, child2)
            children.append(child1)
            children.append(child2)
        # Evaluate childs
        fitness = evaluate_population(children)
        # Find best solutions
        best_of_gen = get_best_route_in_population(fitness)
        # Replace old population with parents and children
        population = children
        generations += 1

        mean, maximum, minimum = get_fitness_stats(fitness)
        l_mean.append(mean)
        l_maximum.append(maximum)
        l_minimum.append(minimum)

        if generations % 10 == 0:
            print_prosentage_done(num_generations, generations)

        if best_of_gen < best:
            best_gen_index = generations
            best = best_of_gen
    
    print(f"Generations: {generations} - Best: {int(best)}")
    return l_mean, l_maximum, l_minimum, [best, best_gen_index]

def get_prosentage(pop_size, percent):
    return int(pop_size * percent / 100)

if __name__ == "__main__":
    # number_cities = 11
    # exhaustive_search()
    number_of_swaps = 1000
    # hill_climb(number_of_swaps)
    number_of_generations = 1000
    population_size       = 300
    number_of_parents     = get_prosentage(population_size, 80)
    number_of_children    = get_prosentage(population_size, 20)
    mutation_rate         = 0.10
    mean, maximum, minimum, best = genetic_algorithm(population_size, number_of_generations, number_of_parents, number_of_children, mutation_rate)
    
    # Plot
    x = [i for i in range(number_of_generations)]
    fig, ax = plt.subplots()
    ax.plot(x      , mean   , label='Mean')
    ax.plot(x      , maximum, label='Max')
    ax.plot(x      , minimum, label='Min')
    ax.scatter(best[1], best[0], s=50, marker='X', c='purple', label='Best')
    ax.legend()
    plt.show()