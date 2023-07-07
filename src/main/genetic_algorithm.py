import random
import numpy as np

class GeneticAlgorithm:
    def __init__(self, pop_size, max_generations, mutation_rate, crossover_rate, n_variables, n_inequality_constraints, epsilon, penalty_method):
        self.pop_size = pop_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.n_variables = n_variables
        self.n_inequality_constraints = n_inequality_constraints
        self.epsilon = epsilon
        self.penalty_method = penalty_method

        self.lower_bound = [0] * 9 + [0, 0, 0] + [0, 0, 0, 0, 0, 0, 0]
        self.upper_bound = [1] * 9 + [100, 100, 100] + [1]

    def objective_function(self, x):
        return 5 * sum(x[:4]) - 5 * sum([xi**2 for xi in x[:4]]) - sum(x[4:13])

    def inequality_constraints(self, x):
        constraints = np.zeros(self.n_inequality_constraints)
        
        constraints[0] = 2*x[0] + 2*x[1] + x[9] + x[10] - 10
        constraints[1] = 2*x[0] + 2*x[2] + x[9] + x[11] - 10
        constraints[2] = 2*x[1] + 2*x[2] + x[10] + x[11] - 10
        constraints[3] = -8*x[0] + x[9]
        constraints[4] = -8*x[1] + x[10]
        constraints[5] = -8*x[2] + x[11]
        constraints[6] = -2*x[3] - x[4] + x[9]
        constraints[7] = -2*x[5] - x[6] + x[10]
        constraints[8] = -2*x[7] - x[8] + x[11]

        return constraints

    def penalty_function(self, x):
        constraints = self.inequality_constraints(x)
        penalty = sum([max(0, constraint)**2 for constraint in constraints])
        return penalty
    
    def penalty_function_epsilon(self, x):
        constraints = self.inequality_constraints(x)
        penalty = sum([max(0, constraint)**2 if constraint <= 0 else (constraint / self.epsilon)**2 for constraint in constraints])
        return penalty

    def is_feasible(self, x):
        constraints = self.inequality_constraints(x)
        return all([constraint <= 0 for constraint in constraints]) and all([abs(constraint) - self.epsilon <= 0 for constraint in constraints[self.n_inequality_constraints:]])

    def initialize_population(self):
        population = []
        for _ in range(self.pop_size):
            individual = [random.uniform(self.lower_bound[i], self.upper_bound[i]) for i in range(self.n_variables)]
            population.append(individual)
        return population

    def select_parents(self, population):
        parents = []
        for _ in range(self.pop_size):
            tournament = random.sample(range(self.pop_size), 2)
            if self.penalty_method == "static":
                fitness1 = self.penalty_function(population[tournament[0]])
                fitness2 = self.penalty_function(population[tournament[1]])
            else:
                fitness1 = self.penalty_function_epsilon(population[tournament[0]])
                fitness2 = self.penalty_function_epsilon(population[tournament[1]])
            if fitness1 <= fitness2:
                parents.append(population[tournament[0]])
            else:
                parents.append(population[tournament[1]])
        return parents

    def crossover(self, parent1, parent2):
        point = random.randint(1, self.n_variables - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    def mutate(self, individual):
        for i in range(self.n_variables):
            if random.random() < self.mutation_rate:
                individual[i] = random.uniform(self.lower_bound[i], self.upper_bound[i])
        return individual

    def evaluate_population(self, population):
        fitness_values = []
        for individual in population:
            if self.is_feasible(individual):
                fitness_values.append(self.objective_function(individual))
            else:
                fitness_values.append(float('inf'))
        return fitness_values

    def genetic_algorithm(self):
        population = self.initialize_population()

        fitness_values = self.evaluate_population(population)

        best_fitness = min(fitness_values)
        best_solution = population[fitness_values.index(best_fitness)]

        for _ in range(self.max_generations):
            parents = self.select_parents(population)

            offspring = []
            while len(offspring) < self.pop_size:
                parent1, parent2 = random.sample(parents, 2)
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                offspring.append(child1)
                offspring.append(child2)

            offspring_fitness = self.evaluate_population(offspring)

            population = offspring
            fitness_values = offspring_fitness

            best_fitness = min(fitness_values)
            best_solution = population[fitness_values.index(best_fitness)]

            if best_fitness < float('inf'):
                break

        return best_solution, best_fitness