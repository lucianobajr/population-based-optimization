import random
import math
import statistics

class GeneticProgramming:
    def __init__(self, pop_size, num_generations, tournament_size, mutation_rate, penalty_method):
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        self.penalty_method = penalty_method

    def evaluate(self, individual):
        if self.penalty_method == "static_penalty":
            penalty = self.calculate_static_penalty(individual)
            return 5 * sum(individual[:4]) - 5 * sum([xi**2 for xi in individual[:4]]) - sum(individual[4:]) + penalty
        elif self.penalty_method == "epsilon_constraint":
            violation = self.calculate_constraint_violation(individual)
            if violation > 0:
                return math.inf
            else:
                return 5 * sum(individual[:4]) - 5 * sum([xi**2 for xi in individual[:4]]) - sum(individual[4:])

    def calculate_static_penalty(self, individual):
        penalty = 0
        # Constraint g1
        if 2*individual[0] + 2*individual[1] + individual[9] + individual[10] - 10 > 0:
            penalty += 1000 * (2*individual[0] + 2*individual[1] + individual[9] + individual[10] - 10)
        # Constraint g2
        if 2*individual[0] + 2*individual[2] + individual[9] + individual[11] - 10 > 0:
            penalty += 1000 * (2*individual[0] + 2*individual[2] + individual[9] + individual[11] - 10)
        # Constraint g3
        if 2*individual[1] + 2*individual[2] + individual[10] + individual[11] - 10 > 0:
            penalty += 1000 * (2*individual[1] + 2*individual[2] + individual[10] + individual[11] - 10)
        # Constraint g4
        if -8*individual[0] + individual[9] > 0:
            penalty += 1000 * (-8*individual[0] + individual[9])
        # Constraint g5
        if -8*individual[1] + individual[10] > 0:
            penalty += 1000 * (-8*individual[1] + individual[10])
        # Constraint g6
        if -8*individual[2] + individual[11] > 0:
            penalty += 1000 * (-8*individual[2] + individual[11])
        # Constraint g7
        if -2*individual[3] - individual[4] + individual[9] > 0:
            penalty += 1000 * (-2*individual[3] - individual[4] + individual[9])
        # Constraint g8
        if -2*individual[5] - individual[6] + individual[10] > 0:
            penalty += 1000 * (-2*individual[5] - individual[6] + individual[10])
        # Constraint g9
        if -2*individual[7] - individual[8] + individual[11] > 0:
            penalty += 1000 * (-2*individual[7] - individual[8] + individual[11])

        return penalty

    def calculate_constraint_violation(self, individual):
        violations = []
        # Constraint g1
        violations.append(max(0, 2*individual[0] + 2*individual[1] + individual[9] + individual[10] - 10))
        # Constraint g2
        violations.append(max(0, 2*individual[0] + 2*individual[2] + individual[9] + individual[11] - 10))
        # Constraint g3
        violations.append(max(0, 2*individual[1] + 2*individual[2] + individual[10] + individual[11] - 10))
        # Constraint g4
        violations.append(max(0, -8*individual[0] + individual[9]))
        # Constraint g5
        violations.append(max(0, -8*individual[1] + individual[10]))
        # Constraint g6
        violations.append(max(0, -8*individual[2] + individual[11]))
        # Constraint g7
        violations.append(max(0, -2*individual[3] - individual[4] + individual[9]))
        # Constraint g8
        violations.append(max(0, -2*individual[5] - individual[6] + individual[10]))
        # Constraint g9
        violations.append(max(0, -2*individual[7] - individual[8] + individual[11]))

        return sum(violations)

    def generate_individual(self):
        individual = []
        for i in range(13):
            if i < 9:
                individual.append(random.uniform(0, 1))
            elif i < 12:
                individual.append(random.uniform(0, 100))
            else:
                individual.append(random.uniform(0, 1))
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
                if i < 9:
                    individual[i] = random.uniform(0, 1)
                elif i < 12:
                    individual[i] = random.uniform(0, 100)
                else:
                    individual[i] = random.uniform(0, 1)
        return individual

    def enforce_constraints(self, individual):
        # Constraint g1
        if 2*individual[0] + 2*individual[1] + individual[9] + individual[10] - 10 > 0:
            individual[9] = max(0, 10 - (2*individual[0] + 2*individual[1] + individual[10]))
            individual[10] = max(0, 10 - (2*individual[0] + 2*individual[2] + individual[10]))
        # Constraint g2
        if 2*individual[0] + 2*individual[2] + individual[9] + individual[11] - 10 > 0:
            individual[9] = max(0, 10 - (2*individual[0] + 2*individual[2] + individual[11]))
            individual[11] = max(0, 10 - (2*individual[0] + 2*individual[2] + individual[11]))
        # Constraint g3
        if 2*individual[1] + 2*individual[2] + individual[10] + individual[11] - 10 > 0:
            individual[10] = max(0, 10 - (2*individual[1] + 2*individual[2] + individual[11]))
            individual[11] = max(0, 10 - (2*individual[1] + 2*individual[2] + individual[11]))
        # Constraint g4
        if -8*individual[0] + individual[9] > 0:
            individual[9] = max(0, 8*individual[0])
        # Constraint g5
        if -8*individual[1] + individual[10] > 0:
            individual[10] = max(0, 8*individual[1])
        # Constraint g6
        if -8*individual[2] + individual[11] > 0:
            individual[11] = max(0, 8*individual[2])
        # Constraint g7
        if -2*individual[3] - individual[4] + individual[9] > 0:
            individual[9] = max(0, -2*individual[3] - individual[4])
        # Constraint g8
        if -2*individual[5] - individual[6] + individual[10] > 0:
            individual[10] = max(0, -2*individual[5] - individual[6])
        # Constraint g9
        if -2*individual[7] - individual[8] + individual[11] > 0:
            individual[11] = max(0, -2*individual[7] - individual[8])

        return individual

    def run(self):
        population = self.generate_population()
        best_solutions = []
        for _ in range(self.num_generations):
            new_population = []
            for _ in range(self.pop_size):
                parent1 = self.selection(population)
                parent2 = self.selection(population)
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                child1 = self.enforce_constraints(child1)
                child2 = self.enforce_constraints(child2)
                new_population.extend([child1, child2])
            population = new_population
            best_solution = min(population, key=self.evaluate)
            best_solutions.append(best_solution)
        
        return best_solutions
