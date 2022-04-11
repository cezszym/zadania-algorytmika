import sys
from random import randint, randrange, sample

from async_timeout import enum


def generate_first_population(size):
    population = []
    for i in range(size):
        member = []
        for j in range(50):
            member.append(randint(10, 99))
        population.append(member)
    return population


def fitness(member):
    all_posibles = list(range(-2225, 2226))
    score = 0
    for index, gene in enumerate(member):
        if index % 2 == 0:
            score += gene
        else:
            score -= gene
    return all_posibles.index(score)


def roulette_selection(population):
    scores = [fitness(member) for member in population]
    scores_sum = sum(scores)
    reproduction_chances = [int(score / scores_sum * 1000) for score in scores]
    current_range = [0, 0]
    ranges = []
    for chance in reproduction_chances:
        current_range = [current_range[1], chance + current_range[1]]
        ranges.append(current_range)
    selected_members = []
    for i in population:
        random_num = randint(0, sum(reproduction_chances))
        match = [m for m in ranges if random_num in range(m[0], m[1] + 1)][0]
        selected_members.append(population[ranges.index(match)])
    return selected_members


def ranking_selection(population):
    population.sort(key=fitness)
    current_range = [0, 0]
    ranges = []
    selected_members = []
    sum_of_indexes = 0
    for index, memeber in enumerate(population):
        current_range = [current_range[1], index * 1000 + current_range[1]]
        sum_of_indexes += index * 1000
        ranges.append(current_range)
    for i in population:
        random_num = randint(0, sum_of_indexes)
        match = [m for m in ranges if random_num in range(m[0], m[1] + 1)][0]
        selected_members.append(population[ranges.index(match)])
    return selected_members


def turnament_selection(population):
    selected_members = []
    while len(selected_members) < len(population):
        random_members = []
        random_index1, random_index2, random_index3 = sample(
            range(0, len(population) - 1), 3)
        random_members.append(population[random_index1])
        random_members.append(population[random_index2])
        random_members.append(population[random_index3])
        random_members.sort(key=fitness)
        selected_members.append(random_members[-1])
    return selected_members


def make_pairs(members):
    pairs = []
    while len(members):
        first_random_num = randrange(0, len(members))
        first_in_pair = members.pop(first_random_num)
        second_random_num = randrange(0, len(members))
        second_in_pair = members.pop(second_random_num)
        pairs.append([first_in_pair, second_in_pair])
    return pairs


def one_point_cross(members):
    pairs = make_pairs(members)
    new_generation = []
    for pair in pairs:
        random_index = randrange(0, len(pair[0]))
        first_new_member = pair[0][:random_index] + pair[1][random_index:]
        second_new_member = pair[1][:random_index] + pair[0][random_index:]
        new_generation.append(first_new_member)
        new_generation.append(second_new_member)
    return new_generation


def two_point_cross(members):
    pairs = make_pairs(members)
    new_generation = []

    def get_two_randmon_index():
        random_indexes = sample(range(0, len(pairs[0][0])), 2)
        return min(random_indexes), max(random_indexes)
    for pair in pairs:
        start_index, end_index = get_two_randmon_index()
        while end_index - start_index > len(pairs[0][0]) / 2 or (start_index == len(pairs[0][0]) and end_index == len(pairs[0][0]) - 1):
            start_index, end_index = get_two_randmon_index()
        first_new_member = pair[0][:start_index] + \
            pair[1][start_index:end_index] + pair[0][end_index:]
        second_new_member = pair[1][:start_index] + \
            pair[0][start_index:end_index] + pair[1][end_index:]
        new_generation.append(first_new_member)
        new_generation.append(second_new_member)
    return new_generation


def gen_best_member(generation):
    generation.sort(key=fitness)
    return generation[-1]


def main(size, selection_type, cross_type):
    population = generate_first_population(size)
    selection_method = roulette_selection if selection_type == 'ruletka' else ranking_selection if selection_type == 'ranking' else turnament_selection if selection_type == 'turniej' else None
    cross_method = one_point_cross if cross_type == 'jedno' else two_point_cross if cross_type == 'dwu' else None
    print(sum([fitness(m) for m in population]))
    if selection_method and cross_method:
        for i in range(80):
            next_gen = cross_method(selection_method(population))
            population = next_gen
            new_score = sum([fitness(m) for m in population])
            print(new_score)

        print(gen_best_member(population))
    else:
        print("Złe dane wejściowe")


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2], sys.argv[3])
