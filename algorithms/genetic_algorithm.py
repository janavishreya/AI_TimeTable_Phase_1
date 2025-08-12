import random

def run_genetic_algorithm(input_data, population_size=10, generations=100):
    """Runs a genetic algorithm to generate an initial timetable."""
    population = [generate_random_timetable(input_data) for _ in range(population_size)]
    
    for _ in range(generations):
        population = sorted(population, key=lambda x: fitness(x, input_data), reverse=True)
        new_population = population[:2]  # Select top 2 parents
        
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:5], 2)
            child = crossover(parent1, parent2)
            mutate(child, input_data)
            new_population.append(child)

        population = new_population

    return max(population, key=lambda x: fitness(x, input_data))

def generate_random_timetable(input_data):
    """Creates a random timetable based on input constraints."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timetable = {day: [] for day in days}

    for _ in range(input_data["total_periods"]):
        for day in days:
            subject = random.choice(input_data["subjects"])
            timetable[day].append(subject)

    return timetable

def fitness(timetable, input_data):
    """Evaluates the timetable based on constraints (e.g., subject distribution)."""
    score = 0
    for day in timetable:
        if len(set(timetable[day])) == len(timetable[day]):  # Unique subjects per day
            score += 1
    return score

def crossover(parent1, parent2):
    """Performs crossover between two parent timetables."""
    child = {}
    for day in parent1:
        child[day] = parent1[day][:len(parent1[day])//2] + parent2[day][len(parent2[day])//2:]
    return child

def mutate(timetable, input_data):
    """Mutates the timetable by swapping subjects in a random period."""
    day = random.choice(list(timetable.keys()))
    if len(timetable[day]) > 1:
        i, j = random.sample(range(len(timetable[day])), 2)
        timetable[day][i], timetable[day][j] = timetable[day][j], timetable[day][i]
