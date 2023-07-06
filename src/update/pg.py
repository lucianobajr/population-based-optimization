import random
import math

class GeneticProgramming:
    def __init__(self, pop_size, num_generations, tournament_size, mutation_rate, penalty_method):
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        self.penalty_method = penalty_method

    def objective_function(self, x):
        return 5 * sum(x[:4]) - 5 * sum([xi**2 for xi in x[:4]]) - sum(x[4:13])

    def evaluate(self, individual):
        if self.penalty_method == "static_penalty":
            penalty = self.calculate_static_penalty(individual)
            return self.objective_function(individual) + penalty
        elif self.penalty_method == "epsilon_constraint":
            violation = self.calculate_epsilon_constraint_method(individual)
            if violation > 0:
                return math.inf
            else:
                return self.objective_function(individual)

    def calculate_static_penalty(self, individual):
        penalty = 0

        # Constraint g1
        g1_penalty = max(0, 2 * individual[0] + 2 * individual[1] + individual[9] + individual[10] - 10)
        penalty += 1000 * g1_penalty

        # Constraint g2
        g2_penalty = max(0, 2 * individual[0] + 2 * individual[2] + individual[9] + individual[11] - 10)
        penalty += 1000 * g2_penalty

        # Constraint g3
        g3_penalty = max(0, 2 * individual[1] + 2 * individual[2] + individual[10] + individual[11] - 10)
        penalty += 1000 * g3_penalty

        # Constraint g4
        g4_penalty = max(0, -8 * individual[0] + individual[9])
        penalty += 1000 * g4_penalty

        # Constraint g5
        g5_penalty = max(0, -8 * individual[1] + individual[10])
        penalty += 1000 * g5_penalty

        # Constraint g6
        g6_penalty = max(0, -8 * individual[2] + individual[11])
        penalty += 1000 * g6_penalty

        # Constraint g7
        g7_penalty = max(0, -2 * individual[3] - individual[4] + individual[9])
        penalty += 1000 * g7_penalty

        # Constraint g8
        g8_penalty = max(0, -2 * individual[5] - individual[6] + individual[10])
        penalty += 1000 * g8_penalty

        # Constraint g9
        g9_penalty = max(0, -2 * individual[7] - individual[8] + individual[11])
        penalty += 1000 * g9_penalty

        # Add constraints for upper and lower bounds of variables
        for i in range(len(individual)):
            if i < 9:  # x1 to x9
                if individual[i] < 0 or individual[i] > 1:
                    penalty += 1000
            elif i < 12:  # x10 to x12
                if individual[i] < 0 or individual[i] > 100:
                    penalty += 1000
            else:  # x13
                if individual[i] < 0 or individual[i] > 1:
                    penalty += 1000

        return penalty
    
    def calculate_epsilon_constraint_method(self, individual):
        # Parâmetro epsilon
        epsilon = 1e-6

        # Avaliar a função objetivo
        objective_value = self.objective_function(individual)

        # Calcular as violações das restrições
        constraint_violations = []
        # Constraint g1
        constraint_violations.append(max(0, 2*individual[0] + 2*individual[1] + individual[9] + individual[10] - 10))
        # Constraint g2
        constraint_violations.append(max(0, 2*individual[0] + 2*individual[2] + individual[9] + individual[11] - 10))
        # Constraint g3
        constraint_violations.append(max(0, 2*individual[1] + 2*individual[2] + individual[10] + individual[11] - 10))
        # Constraint g4
        constraint_violations.append(max(0, -8*individual[0] + individual[9]))
        # Constraint g5
        constraint_violations.append(max(0, -8*individual[1] + individual[10]))
        # Constraint g6
        constraint_violations.append(max(0, -8*individual[2] + individual[11]))
        # Constraint g7
        constraint_violations.append(max(0, -2*individual[3] - individual[4] + individual[9]))
        # Constraint g8
        constraint_violations.append(max(0, -2*individual[5] - individual[6] + individual[10]))
        # Constraint g9
        constraint_violations.append(max(0, -2*individual[7] - individual[8] + individual[11]))

        # Calcular a violação total das restrições
        total_violation = sum(constraint_violations)

        # Aplicar a penalidade se houver violação
        if total_violation > epsilon:
            penalty = total_violation  # Penalidade linear
            return objective_value + penalty
        else:
            return objective_value
        
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
                new_population.append(child1)
                new_population.append(child2)
            population = new_population
            best_solution = min(population, key=self.evaluate)
            best_solutions.append(best_solution)
        
        return best_solutions