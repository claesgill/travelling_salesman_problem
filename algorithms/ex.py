from .modules.load_data import Data
from .modules.helpers import print_prosentage_done

class ExhaustiveSearch:
    def __init__(self, num_cities):
        self.num_cities = num_cities
        self.data = None

    def initialize(self):
        self.data = Data(self.num_cities, "./data/cities.csv")
        self.data.load_data()
        self.data.format_data()
        self.data.get_permutations()

    def run(self):
        print(f"\033[35mInitializing Exhastive Search - {self.num_cities} cities\033[0m")
        min_distance = 10000000
        for i in range(len(self.data.permutations)):
            new_distance = self.data.get_route_distance(self.data.permutations[i])
            if new_distance < min_distance:
                min_distance = new_distance
            if i % 10 == 0:
                print_prosentage_done(len(self.data.permutations), i)
        print(f"\033[35mBest: {int(min_distance)}\033[0m")

if __name__ == "__main__":
    number_of_cities = 10
    ex = ExhaustiveSearch(number_of_cities)
    ex.initialize()
    ex.run()