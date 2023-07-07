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
        return 3 * x[0] + 0.001 * x[0]**3 + 2 * x[1] + (0.002/3) * x[1]**3


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

        # Constraint g3
        g3_penalty = max(0, -individual[3] + individual[2] - 0.55)
        penalty += math.pow(g3_penalty, 2)

        # Constraint g4
        g4_penalty = max(0, individual[3] - individual[2] - 0.55)
        penalty += math.pow(g4_penalty, 2)

        # Add constraints for upper and lower bounds of variables
        for i in range(len(individual)):
            if i < 2:  # x1 and x2
                if individual[i] < 0 or individual[i] > 1200:
                    penalty += 1000

        return penalty

    def calculate_epsilon_constraint_method(self, individual):
        #  Parameter epsilon
        epsilon = 1e-6
        # Evaluate the objective function
        objective_value = self.objective_function(individual)

        # Calculate constraint violations
        constraint_violations = []
        # Constraint g1
        constraint_violations.append(max(0, -individual[1] + individual[0] - 0.55))
        
        constraint_violations.append(max(0, -individual[0] + individual[1] - 0.55))

        # Constraint h3
        constraint_violations.append(max(0, 1000 * math.sin(-individual[2] - 0.25) + 1000 * math.sin(-individual[3] - 0.25) + 894.8 - individual[0]))
        # Constraint h4
        constraint_violations.append(max(0, 1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8 - individual[1]))
        # Constraint h5
        constraint_violations.append(max(0, 1000 * math.sin(individual[3] - 0.25) + 1000 * math.sin(individual[3] - individual[2] - 0.25) + 1294.8))

        # Calculate the total violation of constraints
        total_violation = sum(constraint_violations)

        # Apply penalty if there is a violation
        if total_violation > epsilon:
            penalty = total_violation  # Linear penalty
            return objective_value + penalty
        else:
            return objective_value

    def generate_individual(self):
        individual = []
        for _ in range(4):  # Atualizado para percorrer 4 vezes
            individual.append(random.uniform(0, 1200))
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
                individual[i] = random.uniform(0, 1200)
        return individual

    def enforce_constraints(self, individual):
        # Constraint g3
        if individual[3] - individual[2] < 0.55:
            individual[3] = max(individual[3], individual[2] + 0.55)
        # Constraint g4
        if individual[2] - individual[3] < 0.55:
            individual[2] = max(individual[2], individual[3] + 0.55)

        return individual

    def run(self):
        population = self.generate_population()
        print(population)
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
                child1 = self.enforce_constraints(child1)
                child2 = self.enforce_constraints(child2)
                new_population.append(child1)
                new_population.append(child2)

            population = new_population

        if best_solution is not None:
            decision_variables = best_solution
        else:
            decision_variables = None

        return self.evaluate(best_solution), decision_variables



# Example usage
pop_size = 20
num_generations = 20
tournament_size = 2
mutation_rate = 0.1
penalty_method = "epsilon_constraint"

gp = GeneticProgramming(pop_size, num_generations, tournament_size, mutation_rate, penalty_method)
best_fitness, decision_variables = gp.run()

print("Best Fitness:", best_fitness)
print("Decision Variables:", decision_variables)