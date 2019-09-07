from algorithms.ex import ExhaustiveSearch
from algorithms.hc import HillClimb
from algorithms.ga import GeneticAlgorithm
from algorithms.modules.helpers import get_prosentage

if __name__ == "__main__":
    # Parameters EX
    number_of_cities = 10
    ex = ExhaustiveSearch(number_of_cities)
    ex.initialize()
    ex.run()

    # Parameters HC
    number_of_cities = 10
    number_of_swaps  = 1000
    hc = HillClimb(number_of_cities, number_of_swaps)
    hc.initialize()
    hc.run()

    # Parameters GA
    number_of_cities      = 24
    number_of_generations = 500
    population_size       = 1000
    number_of_parents     = get_prosentage(population_size, 80)
    number_of_children    = get_prosentage(population_size, 20)
    mutation_rate         = 0.01
    ga = GeneticAlgorithm(number_of_cities, 
                          population_size, 
                          number_of_generations, 
                          number_of_parents, 
                          number_of_children, 
                          mutation_rate)
    ga.initialize()
    ga.run()
    ga.plot()