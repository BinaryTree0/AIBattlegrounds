#[water, dust, sheep, wood, wheat, clay, iron] [12, 3, 4, 5, 5]
from operator import itemgetter

def calculate_goods(resources_list):
    # drvo glina za ceste i grad, drvo i za kretanje
    return resources_list[2] * 1.5 + resources_list[3] * 2 + resources_list[4] * 1.5 + resources_list[5] * 2 + resources_list[6]
    #TODO vuna drvo zito glina


def initial_state_heuristic(): # intersections su integeri
    intersection_fitnesses = []
    for intersection in viable_intersections():
        intersection_fitnesses.append((intersection, calculate_goods(get_resources(intersection))))

    sorted_intersection_fitnesses = sorted(intersection_fitnesses, key=itemgetter(1))

    best_city = sorted_intersection_fitnesses[0]
    current_best_neighbour = 0
    current_best_value = 0

    for neighbour in best_city:
        v = intersection_fitnesses[neighbour]
        if v > current_best_value:
            current_best_value = v
            current_best_neighbour = neighbour
    r1 = get_neighbours(best_city)[0]
    r2 = get_neighbours(current_best_neighbour)[0]
    return best_city, r1, current_best_neighbour, r2 # ako smo drugi ako smo prvi uzmemo samo prvi
    #TODO cesta


def terminate_fitness(attrs):  # 0 mi 1 opponent
    myresources, mycities, myroads, opponentresources, opponentcities, opponentroads = attrs[0], attrs[1], attrs[2], attrs[3], attrs[4], attrs[5]

    my_cities_sum = 0
    for city in mycities.keys():
        my_cities_sum += 1.2 * mycities[city]

    with_value = myresources[2:]
    my_koef = 0
    my_total_resources = sum(with_value)
    my_resources_sum = 0
    for res in with_value: # bitni res
        my_resources_sum += res/400
        my_koef += (res/my_total_resources)/0.25

    my_koef = my_koef / len(with_value)

    p1 =  my_cities_sum + my_resources_sum * my_koef + myroads/2


    op_cities_sum = 0
    for city in opponentcities.keys():
        op_cities_sum += 1.2 * opponentcities[city]

    with_value = opponentresources[2:]
    opkoef = 0
    optotal_resources = sum(with_value)
    op_resources_sum = 0
    for res in with_value:  # bitni res
        op_resources_sum += res / 400
        opkoef += (res / optotal_resources) / 0.25

    opkoef = opkoef / len(with_value)

    p2 = op_cities_sum + op_resources_sum * opkoef + opponentroads / 2

    return p1 - p2
