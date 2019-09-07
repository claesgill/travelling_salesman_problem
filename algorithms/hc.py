import numpy as np
from .modules.load_data import Data
from .modules.helpers import print_prosentage_done
from .ex import ExhaustiveSearch

class HillClimb(ExhaustiveSearch):
    def __init__(self, num_cities, num_swaps):
        super().__init__(num_cities)
        self.num_swaps = num_swaps
        
    def run(self):
        print(f"\033[94mInitializing Hill Climb - {self.num_cities} cities\033[0m")
        index = np.random.randint(len(self.data.permutations))
        best_route_dist = self.data.get_route_distance(self.data.permutations[index])
        best_route = list(self.data.permutations[index])
        for i in range(self.num_swaps):
            city1 = np.random.randint(self.num_cities)
            city2 = np.random.randint(self.num_cities)
            new_route = best_route
            new_route[city1], new_route[city2] = new_route[city2], new_route[city1]
            new_route_dist = self.data.get_route_distance(new_route)

            if new_route_dist < best_route_dist:
                best_route_dist = new_route_dist
                best_route = new_route

            if i % 10 == 0:
                print_prosentage_done(self.num_swaps, i)
        print(f"\033[94mBest: {int(best_route_dist)}\033[0m")

if __name__ == "__main__":
    number_of_cities = 10
    number_of_swaps  = 1000

    hc = HillClimb(number_of_cities, number_of_swaps)
    hc.initialize()
    hc.run()