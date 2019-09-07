import csv
import numpy as np
import itertools as it
import math

class Data:
    def __init__(self, number_of_cities, file_path):
        self.number_of_cities = number_of_cities
        self.file_path = file_path
    
    def load_data(self):
        with open(self.file_path, "r") as f: 
            self.data = np.array(list(csv.reader(f, delimiter=';')))
            print("\033[32mData loaded!\033[0m")
        
    def format_data(self):
        cities_matrix = []
        for i in range(1, self.number_of_cities+1):
            cities_matrix.append(self.data[i][:self.number_of_cities])
        print("\033[32mData formatted!\033[0m")
        self.cities = np.array(cities_matrix)

    def get_permutations(self):
        permutations = [i for i in range(self.number_of_cities)]
        self.permutations = list(it.permutations(permutations))

    def get_number_of_permutations(self, sample_size):
        self.permutations = []
        permutations_list = []
        numb_permutations = [i for i in range(self.number_of_cities)]
        random_start = np.random.randint(math.factorial(10))
        permutations_iterator = it.permutations(numb_permutations)
        for _ in range(random_start):
            next(permutations_iterator)
        for i in range(sample_size):
            permutations_list.append(next(permutations_iterator))
        self.permutations = permutations_list 

    def get_distance_between_two_cities(self, start, stop):
        return float(self.cities[start, stop])

    def get_route_distance(self, route):
        distance = []
        for i in range(1, len(route)):
            distance.append(self.get_distance_between_two_cities(route[i-1], route[i]))
        distance.append(self.get_distance_between_two_cities(route[-1], route[0]))
        return sum(distance)

if __name__ == "__main__":
    data = Data(24, "cities.csv")
    data.load_data()
    data.format_data()
    data.get_number_of_permutations(24)