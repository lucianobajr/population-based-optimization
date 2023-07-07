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
        return 3 * x[0] + 0.000001 * x[0]**3 + 2 * x[1] + (0.000002/3) * x[1]**3

    def evaluate(self, individual):
        if self.penalty_method == "static_penalty":
            penalty = self.calculate_static_penalty(individual)
            return self.objective_function(individual) + penalty
        elif self.penalty_method == "epsilon_constraint":
            violation = self.calculate_epsilon_constraint_method(individual)
            if violation < 0:
                return math.inf
            else:
                return self.objective_function(individual)

    def calculate_static_penalty(self, individual):
        penalty = 0

        # Constraint g1
        g1_penalty = max(0, -individual[3] + individual[2] - 0.55)
        penalty += math.pow(g1_penalty, 2)

        # Constraint g2
        g2_penalty = max(0, -individual[2] + individual[3] - 0.55)
        penalty += math.pow(g2_penalty, 2)

        # Constraint h3
        h3_penalty = 1000 * math.sin(-individual[2] - 0.25) + 1000 * math.sin(-individual[3] - 0.25) + 894.8 - individual[0]
        penalty += math.pow(h3_penalty, 2)

        # Constraint h4
        h4_penalty = 1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8 - individual[1]
        penalty += math.pow(h4_penalty, 2)

        # Constraint h5
        h5_penalty = 1000 * math.sin(individual[3] - 0.25) + 1000 * math.sin(individual[3] - individual[2] - 0.25) + 1294.8
        penalty += math.pow(h5_penalty, 2)

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
        # Parameter epsilon
        epsilon = 1e-6

        # Evaluate the objective function
        objective_value = self.objective_function(individual)

        # Calculate constraint violations
        constraint_violations = []
        # Constraint g1
        constraint_violations.append(max(0, -individual[3] + individual[2] - 0.55))
        # Constraint g2
        constraint_violations.append(max(0, -individual[2] + individual[3] - 0.55))
        # Constraint h3
        constraint_violations.append(1000 * math.sin(-individual[2] - 0.25) + 1000 * math.sin(-individual[3] - 0.25) + 894.8 - individual[0])
        # Constraint h4
        constraint_violations.append(1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8 - individual[1])
        # Constraint h5
        constraint_violations.append(1000 * math.sin(individual[3] - 0.25) + 1000 * math.sin(individual[3] - individual[2] - 0.25) + 1294.8)

        # Calculate the total constraint violation
        total_violation = sum(constraint_violations)

        # Apply penalty if there is a violation
        if total_violation > epsilon:
            penalty = total_violation  # Linear penalty
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

    def enforce_constraints(self, individual):
        # Constraint g1
        if -individual[3] + individual[2] - 0.55 > 0:
            individual[2] = individual[3] - 0.55
        # Constraint g2
        if -individual[2] + individual[3] - 0.55 > 0:
            individual[3] = individual[2] - 0.55
        # Constraint h3
        h3 = 1000 * math.sin(-individual[2] - 0.25) + 1000 * math.sin(-individual[3] - 0.25) + 894.8 - individual[0]
        if abs(h3) > 1e-6:
            individual[0] += h3
        # Constraint h4
        h4 = 1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8 - individual[1]
        if abs(h4) > 1e-6:
            individual[1] += h4
        # Constraint h5
        h5 = 1000 * math.sin(individual[3] - 0.25) + 1000 * math.sin(individual[3] - individual[2] - 0.25) + 1294.8
        if abs(h5) > 1e-6:
            individual[2] += h5

        return individual


    def run(self):
        population = self.generate_population()
        for _ in range(num_generations):
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

        return self.evaluate(best_solution)

# Example usage
pop_size = 100
num_generations = 150
tournament_size = 5
mutation_rate = 0.1
penalty_method = "epsilon_constraint"

gp = GeneticProgramming(pop_size, num_generations, tournament_size, mutation_rate, penalty_method)
best_fitness = gp.run()

print("Best Fitness:", best_fitness)