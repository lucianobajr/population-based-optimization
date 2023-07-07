import random
import math

class GeneticProgrammingSecond:
    def __init__(self, pop_size, num_generations, tournament_size, mutation_rate, penalty_method):
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        self.penalty_method = penalty_method

    def objective_function(self, x):
        return 3 * x[0] + 0.000001 * x[0]**3 + 2 * x[1] + (0.000002/3) * x[1]**3

    def evaluate(self, individual):
        if self.penalty_method == "static_penalty":
            penalty = self.calculate_static_penalty(individual)
            return self.objective_function(individual) + penalty
        elif self.penalty_method == "epsilon_constraint":
            objective_value = self.objective_function(individual)
            constraint_violations = self.calculate_augmented_lagrangian_method(individual)
            penalty = sum([max(0, violation)**2 for violation in constraint_violations])

            penalty_weight = 100

            return objective_value + penalty_weight * penalty
            

    def calculate_static_penalty(self, individual):
        penalty = 0

        # Constraint g1
        g1_penalty = max(0, -individual[3] + individual[2] - 0.55)
        penalty += g1_penalty**2

        # Constraint g2
        g2_penalty = max(0, -individual[2] + individual[3] - 0.55)
        penalty += g2_penalty**2

        # Constraint h3
        h3_penalty = 1000 * math.sin(-individual[2] - 0.25) + 1000 * math.sin(-individual[3] - 0.25) + 894.8 - individual[0]
        penalty += h3_penalty**2

        # Constraint h4
        h4_penalty = 1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8 - individual[1]
        penalty += h4_penalty**2

        # Constraint h5
        h5_penalty = 1000 * math.sin(individual[3] - 0.25) + 1000 * math.sin(individual[3] - individual[2] - 0.25) + 1294.8
        penalty += h5_penalty**2

        # Add constraints for upper and lower bounds of variables
        for i in range(len(individual)):
            if i < 2:  # x1, x2
                if individual[i] < 0 or individual[i] > 1200:
                    penalty += 1000
            elif i < 4:  # x3, x4
                if individual[i] < -0.55 or individual[i] > 0.55:
                    penalty += 1000

        return penalty

    def calculate_epsilon_constraint_method(self, individual):
        # Parâmetro epsilon
        epsilon = 1e-6


        constraint_violations = []
        
        objective_value = self.objective_function(individual)

        # Constraint g1
        g1 = -individual[3] + individual[2] - 0.55

        # Constraint g2
        g2 = -individual[2] + individual[3] - 0.55

        # Constraint h3
        h3 = 1000 * math.sin(-individual[2] - 0.25) + 1000 * math.sin(-individual[3] - 0.25) + 894.8 - individual[0]

        # Constraint h4
        h4 = 1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8 - individual[1]

        # Constraint h5
        h5 = 1000 * math.sin(individual[3] - 0.25) + 1000 * math.sin(individual[3] - individual[2] - 0.25) + 1294.8

        constraint_violations.append(g1)
        constraint_violations.append(g2)
        constraint_violations.append(h3)
        constraint_violations.append(h4)
        constraint_violations.append(h5)

        total_violation = sum(constraint_violations)

        # Aplicar a penalidade se houver violação
        if total_violation > epsilon:
            penalty = total_violation  # Penalidade linear
            return objective_value + penalty
        else:
            return total_violation
    
    def calculate_augmented_lagrangian_method(self, individual):
        constraint_violations = []

        # Constraint g1
        constraint_violations.append(-individual[3] + individual[2] - 0.55)

        # Constraint g2
        constraint_violations.append(-individual[2] + individual[3] - 0.55)

        # Constraint h3
        constraint_violations.append(1000 * math.sin(-individual[2] - 0.25) + 1000 * math.sin(-individual[3] - 0.25) + 894.8 - individual[0])

        # Constraint h4
        constraint_violations.append(1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8 - individual[1])

        # Constraint h5
        constraint_violations.append(1000 * math.sin(individual[3] - 0.25) + 1000 * math.sin(individual[3] - individual[2] - 0.25) + 1294.8)

        return constraint_violations

    def generate_individual(self):
        individual = []
        for i in range(4):
            if i < 2:
                individual.append(random.uniform(0, 1200))
            else:
                individual.append(random.uniform(-0.55, 0.55))
        return individual

    def generate_population(self):
        return [self.generate_individual() for _ in range(self.pop_size)]

    def selection(self, population):
        tournament = random.sample(population, self.tournament_size)
        return min(tournament, key=self.evaluate)

    def crossover(self, parent1, parent2):
        point = random.randint(0, len(parent1)-1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    def mutate(self, individual):
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                if i < 2:
                    individual[i] = random.uniform(0, 1200)
                else:
                    individual[i] = random.uniform(-0.55, 0.55)
        return individual

    def run(self):
        population = self.generate_population()
        best_fitness = math.inf
        best_solution = None

        for _ in range(self.num_generations):
            evaluated_population = [(individual, self.evaluate(individual)) for individual in population]

            for individual, fitness in evaluated_population:
                if fitness < best_fitness:
                    best_fitness = fitness
                    best_solution = individual

            # Perform selection, crossover, and mutation to generate a new population
            new_population = []
            for _ in range(self.pop_size):
                parent1 = self.selection(population)
                parent2 = self.selection(population)
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                new_population.append(child1)
                new_population.append(child2)

            population = new_population

        decision_variables = best_solution[:4] if best_solution is not None else None

        return self.evaluate(best_solution), decision_variables