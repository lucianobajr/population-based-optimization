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
        print("aqui: x", x)
        return 3*x[0] + 0.000001*x[0]**3 + 2*x[1] + (0.000002/3)*x[1]**3

    def evaluate(self, individual):
        if self.penalty_method == "static_penalty":
            penalty = self.calculate_static_penalty(individual)
            print("aqui2: individual", individual)
            return self.objective_function(individual) + penalty
        elif self.penalty_method == "epsilon_constraint":
            violation = self.calculate_epsilon_constraint_method(individual)
            if violation > 0:
                return math.inf
            else:
                print("aqui3")
                return self.objective_function(individual)

    def calculate_static_penalty(self, individual):
        penalty = 0
        print(individual)
        # Constraint g1
        # g1_penalty = max(0, -individual[3] + individual[2] - 0.55)
        # penalty += 2 * g1_penalty

        # # Constraint g2
        # g2_penalty = max(0, -individual[2] + individual[3] - 0.55)
        # penalty += 2 * g2_penalty

        # # Constraint h3
        # g3_penalty = max(0, 1000 * math.sin(-individual[2] - 0.25) + 1000 * math.sin(-individual[3] - 0.25) + 894.8 - individual[0])
        # penalty += 2 * g3_penalty

        # # Constraint h4
        # g4_penalty = max(0, 1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8 - individual[1])
        # penalty += 2 * g4_penalty

        # # Constraint h5
        # g5_penalty = max(0, 1000 * math.sin(individual[3] - 0.25) + 1000 * math.sin(individual[3] - individual[2] - 0.25) + 1294.8)
        # penalty += 2 * g5_penalty

        # # Add constraints for upper and lower bounds of variables
        # for i in range(len(individual)):
        #     if i < 9:  # x1 to x9
        #         if individual[i] < 0 or individual[i] > 1:
        #             penalty += 1000
        #     elif i < 12:  # x10 to x12
        #         if individual[i] < 0 or individual[i] > 100:
        #             penalty += 1000
        #     else:  # x13
        #         if individual[i] < 0 or individual[i] > 1:
        #             penalty += 1000

        return penalty
    
    def calculate_epsilon_constraint_method(self, individual):
        # Parâmetro epsilon
        epsilon = 1e-6

        # Avaliar a função objetivo
        objective_value = self.objective_function(individual)

        # Calcular as violações das restrições
        constraint_violations = []
        # Constraint g1
        constraint_violations.append(max(0, -individual[3] + individual[2] - 0.55))
        # Constraint g2
        constraint_violations.append(max(0, -individual[2] + individual[3] - 0.55))
        # Constraint h3
        constraint_violations.append(max(0, 1000 * math.sin(-individual[2] - 0.25) + 1000 * math.sin(-individual[3] - 0.25) + 894.8 - individual[0]))
        # Constraint h4
        constraint_violations.append(max(0, 1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8 - individual[1]))
        # Constraint h5
        constraint_violations.append(max(0, 1000 * math.sin(individual[3] - 0.25) + 1000 * math.sin(individual[3] - individual[2] - 0.25) + 1294.8))

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
        for i in range(4):
            if i < 2:
                individual.append(random.uniform(0, 1200))
            else:
                individual.append(random.uniform(-0.55, 0.55))

        return individual
    
    def generate_population(self):
        print("aqui4")
        return [self.generate_individual() for _ in range(self.pop_size)]

    def selection(self, population):
        tournament_size = min(self.tournament_size, len(population))
        tournament = random.sample(population, tournament_size)
        print("aqui5")
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

    def enforce_constraints(self, individual):
        # Constraint g1
        if -individual[3] + individual[2] - 0.55 > 0:
            individual[3] = individual[2] - 0.55
        # Constraint g2
        if -individual[2] + individual[3] - 0.55 > 0:
            individual[2] = individual[3] - 0.55
    
        # Constraint h3
        constraint_h3 = 1000 * math.sin(-individual[2] - 0.25) + 1000 * math.sin(-individual[3] - 0.25) + 894.8 - individual[0]
        if abs(constraint_h3) != 0:
            individual[0] = 1000 * math.sin(-individual[2] - 0.25) + 1000 * math.sin(-individual[3] - 0.25) + 894.8

        # Constraint h4
        constraint_h4 = 1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8 - individual[1]
        if abs(constraint_h4) != 0:
            individual[1] = 1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8

        # Constraint h5
        constraint_h5 = 1000 * math.sin(individual[3] - 0.25) + 1000 * math.sin(individual[3] - individual[2] - 0.25) + 1294.8
        if abs(constraint_h5) != 0:
            individual[2] = math.sin((constraint_h5 - 1000 * math.sin(individual[3] - 0.25)) / 1000) - 0.25
            individual[3] = math.sin((constraint_h5 - 1000 * math.sin(individual[3] - individual[2] - 0.25)) / 1000) - 0.25

    
        return individual

    def run(self):
        population = self.generate_population()
        best_fitness = math.inf
        best_solution = None

        for _ in range(self.num_generations):
            print("population", population)
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
                child1 = self.enforce_constraints(child1)
                child2 = self.enforce_constraints(child2)
                new_population.append(child1)
                new_population.append(child2)

            population = new_population

        decision_variables = best_solution[:4] if best_solution is not None else None

        return self.evaluate(best_solution), decision_variables