import csv
import time
import itertools as it
import numpy as np
from timer_decorator import time_it, time_it_return

def format_data(data):
    cities_matrix = []
    for i in range(1, number_cities+1):
        cities_matrix.append(data[i][:number_cities])
    return np.array(cities_matrix)

number_cities = 11
with open("cities.csv", "r") as f: 
    data = np.array(list(csv.reader(f, delimiter=';')))
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

def genetic_algorithm(num_cities):
    pass

if __name__ == "__main__":
    # number_cities = 11
    number_of_swaps = 1000

    # exhaustive_search()
    hill_climb(number_of_swaps)
