import random

class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = None

class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate, generations):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = []

    def initialize_population(self):
        for _ in range(self.population_size):
            chromosome = [random.uniform(0, 1) for _ in range(13)]
            individual = Individual(chromosome)
            self.population.append(individual)
    
    def evaluate_fitness(self, individual):
        x = individual.chromosome
        g1 = 2 * x[0] + 2 * x[1] + x[9] + x[10] - 10
        g2 = 2 * x[0] + 2 * x[2] + x[9] + x[11] - 10
        g3 = 2 * x[1] + 2 * x[2] + x[10] + x[11] - 10
        g4 = -8 * x[0] + x[9]
        g5 = -8 * x[1] + x[10]
        g6 = -8 * x[2] + x[11]
        g7 = -2 * x[3] - x[4] + x[9]
        g8 = -2 * x[5] - x[6] + x[10]
        g9 = -2 * x[7] - x[8] + x[11]

        constraints = [g1, g2, g3, g4, g5, g6, g7, g8, g9]
        violation_penalty = sum([max(0, constraint) for constraint in constraints])

        fitness = 5 * sum(x[:4]) - 5 * sum([xi**2 for xi in x[:4]]) - sum(x[4:]) + violation_penalty

        return fitness

    def evaluate_population_fitness(self):
        for individual in self.population:
            individual.fitness = self.evaluate_fitness(individual)

    def tournament_selection(self):
        tournament_size = 2
        selected_individuals = random.sample(self.population, tournament_size)
        selected_individuals.sort(key=lambda ind: ind.fitness)
        
        return selected_individuals[0]

    def crossover(self, parent1, parent2):
        point = random.randint(0, 12)
        child_chromosome = parent1.chromosome[:point] + parent2.chromosome[point:]
        child = Individual(child_chromosome)
        
        return child
    
    def mutate(self, individual):
        for i in range(13):
            if random.random() < self.mutation_rate:
                individual.chromosome[i] = random.uniform(0, 1)
    
    def evolve(self):
        self.initialize_population()
        self.evaluate_population_fitness()

        for _ in range(self.generations):
            new_population = []

            while len(new_population) < self.population_size:
                parent1 = self.tournament_selection()
                parent2 = self.tournament_selection()

                child = self.crossover(parent1, parent2)
                self.mutate(child)

                new_population.append(child)

            self.population = new_population
            self.evaluate_population_fitness()

        self.population.sort(key=lambda ind: ind.fitness)
        best_individual = self.population[0]

        return best_individual