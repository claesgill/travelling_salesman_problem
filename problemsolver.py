import csv
import time
import itertools as it
import numpy as np

def time_it(original_function):
    import time
    def wrapper(*args, **kvargs):
        t1 = time.time()
        results = original_function(*args, **kvargs)
        t2 = time.time() - t1
        print(f"{original_function.__name__}:\nLength: {results}\nTime: {t2} sec")
    return wrapper

def format_data(data):
    all_cities = []
    for i in range(len(data)-1):
        new_city = {"city": data[0][i], "index": i, "distance": [data[i+1]]}
        all_cities.append(new_city)
        # new_city["index"] = i
        # new_city["city"] = data[0][i]
        # new_city["distance"].append(data[i+1])
    #     all_cities.append({"city": data[0][i], "index": i, "distance": [data[i+1]]})
    # return all_cities
    return all_cities

with open("cities.csv", "r") as f: 
    data = list(csv.reader(f, delimiter=';'))
cities = format_data(data)

@time_it
def exhaustive_search(num_cities):
    permutations = get_permutations(num_cities)
    distances = []
    for i in range(len(permutations)):
        distances.append(distance(permutations[i]))
    return min(distances)
 
def get_city_distance(city1, city2):
    index1 = city1["index"]
    index2 = city2["index"]
    return float(city1["distance"][0][index2])

def get_city(city_name, cities):
    for i in range(len(cities)):
        if city_name == cities[i]["city"]:
            return cities[i]

def distance(permutation):
    distance = []
    for i in range(len(permutation)-1):
        city1 = get_city(permutation[i]  , cities)
        city2 = get_city(permutation[i+1], cities)
        # Distanse mellom byer
        d = get_city_distance(city1, city2)
        distance.append(d)
    # Huske å ta fra siste til første
    city1 = get_city(permutation[-1], cities)
    city2 = get_city(permutation[0] , cities)
    d = get_city_distance(city1, city2)
    distance.append(d)
    return sum(distance)

def get_permutations(num_cities):
    return list(it.permutations(data[0][:num_cities], num_cities))

@time_it
def hill_climb(num_cities):
    permutations = get_permutations(num_cities)
    # for k in range(len(permutations)):
    #     print(distance(permutations[k]))
    
    # 1) Starte et random sted i data-sett og kalkulere rute
    # 2) Sammenligne med nabo-node til høyre/venstre og velg beste
    # 3) Fortsett frem til funnet den beste
    index = np.random.randint(len(permutations))    
    while(True):
        lenght         = distance(permutations[index])
        left_neighbor  = distance(permutations[index-1])
        right_neighbor = distance(permutations[index+1])
        if left_neighbor < lenght:
            index -= 1
        elif right_neighbor < lenght:
            index += 1
        else:
            break
    return lenght

if __name__ == "__main__":
    number_cities = 10

    exhaustive_search(number_cities)
    hill_climb(number_cities)

    # t1 = time.time()
    # lenght = exhaustive_search(number_cities)
    # time_used = time.time() - t1
    # print(F"Exhaustive Search:\nLenght: {lenght}\nTime: {time_used:.3} sec")

    # t1 = time.time()
    # lenght = hill_climb(number_cities)
    # time_used = time.time() - t1
    # print(F"Hill Climbing:\nLenght: {lenght}\nTime: {time_used:.3} sec")