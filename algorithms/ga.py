import math
import numpy as np
import matplotlib.pyplot as plt
from .modules.load_data import Data
from .modules.helpers import print_prosentage_done, get_prosentage

class GeneticAlgorithm:
    def __init__(self, num_cities, pop_size, num_gens, num_parents, num_childs, mut_rate):
        self.num_cities  = num_cities
        self.pop_size    = pop_size
        self.num_gens    = num_gens
        self.num_parents = num_parents
        self.num_childs  = num_childs
        self.mut_rate    = mut_rate
        self.population  = []
        self.fitness     = []
        self.best           = None
        self.best_gen_index = None
        self.cities         = None

    def _evaluate_population(self, population):
        fitness = []
        for route in population:
            distance = self.data.get_route_distance(route)
            fitness.append(distance)
        return fitness

    def _get_best_route_in_population(self):
        return min(self.fitness)
    
    def _select_parents_based_on_fitness(self, population, fitness):
        parents = []
        sorted_fitness = np.argsort(fitness)
        for i in range(len(population)):
            parents.append(population[sorted_fitness[i]])
        return parents
    
    def _order_crossover(self, parent1, parent2):
        start = np.random.randint(len(parent1)-1)
        end   = np.random.randint(len(parent1)-1)
        if end > start:
            start, end = end, start
        child = [None for _ in range(len(parent1))]
        child[start:end] = parent1[start:end]
        rest = list(parent2).copy()
        for p1 in parent1[start:end]:
            if p1 in rest:
                    rest.remove(p1)
        rest_iter = iter(rest)
        for i in range(len(child)):
            if child[i] == None:
                child[i] = next(rest_iter)
        return child

    def _swap_mutation(self, persentage, child):
        if persentage >= np.random.rand():
            random_index1 = np.random.randint(len(child))
            random_index2 = np.random.randint(len(child))
            child[random_index1], child[random_index2] = child[random_index2], child[random_index1]
            return child
        return child

    def _get_fitness_stats(self):
        fitness = np.array(self.fitness)
        return np.mean(fitness), np.max(fitness), np.min(fitness)

    def initialize(self):
        self.data = Data(self.num_cities, "./data/cities.csv")
        self.data.load_data()
        self.data.format_data()
        # Initialize population
        self.data.get_number_of_permutations(self.pop_size)
        # TODO: Maybe need to shuffle data?
        self.population = self.data.permutations
        self.cities = self.data.cities
        # Evaluate population
        self.fitness = self._evaluate_population(self.population)
        # Find best route
        self.best = self._get_best_route_in_population()

    def run(self):
        print(f"\033[93mInitializing the Genetic Algoritm - {self.num_cities} cities")
        self.l_mean    = []
        self.l_maximum = []
        self.l_minimum = []
        generations = 0
        while generations < self.num_gens:
            # Select parents
            parents = self._select_parents_based_on_fitness(self.population, self.fitness)
            # Clear lists
            children = []
            # For parent1 and parent2 in parents
            for i in range(1, len(parents)):
                # Chose parents randomly
                parent1 = parents[np.random.randint(len(parents))]
                parent2 = parents[np.random.randint(len(parents))]
                child = self._order_crossover(parent1, parent2)
                # Mutate childs
                child = self._swap_mutation(self.mut_rate, child)
                children.append(child)
            children.append(child)
            # Evaluate childs
            self.fitness = self._evaluate_population(children)
            # Find best solutions
            best_of_gen = self._get_best_route_in_population()
            # Find best children
            best_children = self._select_parents_based_on_fitness(children, self.fitness)
            # Replace old population with parents and children
            self.population = parents[:self.num_parents] + best_children[:self.num_childs]

            mean, maximum, minimum = self._get_fitness_stats()
            self.l_mean.append(mean)
            self.l_maximum.append(maximum)
            self.l_minimum.append(minimum)

            if generations % 10 == 0:
                print_prosentage_done(self.num_gens, generations)

            if best_of_gen < self.best:
                self.best_gen_index = generations
                self.best = best_of_gen

            generations += 1
        print(f"Generations: {generations} - Best: {int(self.best)}\033[0m")
    
    def plot(self):
        x = [i for i in range(self.num_gens)]
        fig, ax = plt.subplots()
        ax.plot(x, self.l_mean   , label='Mean')
        ax.plot(x, self.l_maximum, label='Max')
        ax.plot(x, self.l_minimum, label='Min')
        ax.scatter(self.best_gen_index, self.best, s=50, marker='X', c='purple', label='Best')
        ax.legend()
        plt.show()

if __name__ == "__main__":
    # Parameters
    number_of_cities      = 24
    number_of_generations = 500
    population_size       = 1000
    number_of_parents     = get_prosentage(population_size, 80)
    number_of_children    = get_prosentage(population_size, 20)
    mutation_rate         = 0.01

    ga = GeneticAlgorithm(number_of_cities, population_size, number_of_generations, number_of_parents, number_of_children, mutation_rate)
    ga.initialize()
    ga.run()
    ga.plot()