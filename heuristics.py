#[water, dust, sheep, wood, wheat, clay, iron] [12, 3, 4, 5, 5]
from operator import itemgetter

def calculate_goods(resources_list):
    # drvo glina za ceste i grad, drvo i za kretanje
    return resources_list[2] + resources_list[3] * 2 + resources_list[4] + resources_list[5] * 2 + resources_list[6]


def initial_state_heuristic(map): # intersections su integeri
    intersection_fitnesses = []
    for intersection in map.viable_intersections():
        intersection_fitnesses.append((intersection, calculate_goods(map.get_resources(intersection))))

    sorted_intersection_fitnesses = sorted(intersection_fitnesses, key=itemgetter(1))

    best_city = sorted_intersection_fitnesses[0]
    current_best_neighbour = 0
    current_best_value = 0

    for neighbour in best_city:
        v = intersection_fitnesses[neighbour]
        if v > current_best_value:
            current_best_value = v
            current_best_neighbour = neighbour

    return best_city, current_best_neighbour # ako smo drugi ako smo prvi uzmemo samo prvi

def terminate_fitness(map,player=0):  # 0 mi 1 opponent
    if player == 0:
        resources = map.ownResources()
        cities = map.ownCities()
        roads = map.ownRoads() # int

        cities_sum = 0
        for city in cities.keys():
            cities_sum += 1.2 * cities[city]

        with_value = resources[2:]
        koef = 0
        total_resources = sum(with_value)
        resources_sum = 0
        for res in with_value: # bitni res
            resources_sum += res/400
            koef += (res/total_resources)/0.25

        koef = koef / len(with_value)
    
        return cities_sum + resources_sum * koef + roads/2

    else:
        resources = map.opponentResources()
        cities = map.opponentCities()
        roads = map.opponentRoads()  # int

        cities_sum = 0
        for city in cities.keys():
            cities_sum += 1.2 * cities[city]

        with_value = resources[2:]
        koef = 0
        total_resources = sum(with_value)
        resources_sum = 0
        for res in with_value:  # bitni res
            resources_sum += res / 400
            koef += (res / total_resources) / 0.25

        koef = koef / len(with_value)

        return cities_sum + resources_sum * koef + roads / 2




