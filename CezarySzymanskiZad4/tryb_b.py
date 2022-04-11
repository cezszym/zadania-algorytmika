import sys
from random import randint, randrange, sample, random


def generate_first_population(size):
    population = []
    for i in range(size):
        member = {
            'attractive': [],
            'immunity': []
        }
        for j in range(148):
            member['attractive'].append(randint(10, 99))
            member['immunity'].append(randint(10, 99))
        population.append(member)
    return population


def fitness(member, A, B):
    max_attractive = (46 + 58) * 99
    attractive = 0
    for gene in member['attractive'][10:56] + member['attractive'][90:149]:
        attractive += gene
    relative_attractive = attractive / max_attractive
    max_immunity = (43 + 31) * 99
    immunity = 0
    for gene in member['immunity'][45:88] + member['immunity'][101:132]:
        immunity += gene
    relative_immunity = immunity / max_immunity
    member['immunity_rate'] = relative_immunity
    return (A / (A + B)) * relative_attractive + (B / (A + B)) * relative_immunity


def roulette_selection(population, A, B):
    scores = [fitness(member, A, B) for member in population]
    scores_sum = sum(scores)
    reproduction_chances = [int(score / scores_sum * 10000)
                            for score in scores]
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


def make_pairs(members):
    pairs = []
    while len(members) >= 2:
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
        first_new_member = {
            'attractive': [],
            'immunity': []
        }
        second_new_member = {
            'attractive': [],
            'immunity': []
        }
        first_new_member['attractive'] = pair[0]['attractive'][:random_index] + \
            pair[1]['attractive'][random_index:]
        second_new_member['attractive'] = pair[0]['attractive'][:random_index] + \
            pair[1]['attractive'][random_index:]

        random_index = randrange(0, len(pair[0]))
        first_new_member['immunity'] = pair[0]['immunity'][:random_index] + \
            pair[1]['immunity'][random_index:]
        second_new_member['immunity'] = pair[0]['immunity'][:random_index] + \
            pair[1]['immunity'][random_index:]
        new_generation.append(first_new_member)
        new_generation.append(second_new_member)
    return new_generation


def eliminaion(population):
    for member in population:
        if member['immunity_rate'] >= 0.6:
            pass
        elif member['immunity_rate'] > 0.5:
            if random() < 0.05:
                population.remove(member)
        elif member['immunity_rate'] > 0.4:
            if random() < 0.1:
                population.remove(member)
        else:
            if random() < 0.15:
                population.remove(member)

    return population


def main(size, A, B):
    population = generate_first_population(size)
    print(sum([fitness(m, A, B) for m in population]) / len(population))
    num_of_generations = 1
    last_generation_with_deaths = 0
    for i in range(500):
        population_size_on_start = len(population)
        print(len(population))
        if len(population) < 4:
            print("umarły w ciagu", num_of_generations, "generacji")
            break
        next_gen = one_point_cross(roulette_selection(population, A, B))
        population = next_gen
        num_of_generations += 1
        new_score = sum([fitness(m, A, B) for m in population])
        population = eliminaion(population)
        if len(population) != population_size_on_start:
            last_generation_with_deaths = num_of_generations
        print(sum([fitness(m, A, B)
              for m in population]) / len(population))
    print("Ostatnia generacja ze śmierciami: ", last_generation_with_deaths)


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
