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
            penalty = self.static_penalty(individual)
        elif self.penalty_method == "epsilon_constraint":
            penalty = self.epsilon_constraint(individual)
        else:
            raise ValueError("Invalid penalty_method")

        return self.objective_function(individual) + penalty

    def static_penalty(self, individual):
        penalty = 0

        # Constraint g1
        g1 = -individual[3] + individual[2] - 0.55
        if g1 > 0:
            penalty += 1000 * g1**2

        # Constraint g2
        g2 = -individual[2] + individual[3] - 0.55
        if g2 > 0:
            penalty += 1000 * g2**2

        # Constraint h3
        h3 = 1000 * math.sin(-individual[2] - 0.25) + 1000 * math.sin(-individual[3] - 0.25) + 894.8 - individual[0]
        if abs(h3) > 0.00001:
            penalty += 1000 * h3**2

        # Constraint h4
        h4 = 1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8 - individual[1]
        if abs(h4) > 0.00001:
            penalty += 1000 * h4**2

        # Constraint h5
        h5 = 1000 * math.sin(individual[3] - 0.25) + 1000 * math.sin(individual[3] - individual[2] - 0.25) + 1294.8
        if abs(h5) > 0.00001:
            penalty += 1000 * h5**2

        return penalty

    def epsilon_constraint(self, individual):
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

        # Check if constraints are satisfied within epsilon
        if g1 <= 0 and g2 <= 0 and abs(h3) <= 0.00001 and abs(h4) <= 0.00001 and abs(h5) <= 0.00001:
            return 0
        else:
            return math.inf

    def static_penalty(self, individual):
        penalty = 0

        # Constraint g1
        if -individual[3] + individual[2] - 0.55 > 0:
            penalty += 1000 * (-individual[3] + individual[2] - 0.55) ** 2

        # Constraint g2
        if -individual[2] + individual[3] - 0.55 > 0:
            penalty += 1000 * (-individual[2] + individual[3] - 0.55) ** 2

        # Constraint h3
        h3 = 1000 * math.sin(-individual[2] - 0.25) + 1000 * math.sin(-individual[3] - 0.25) + 894.8 - individual[0]
        if h3 !=0:
            penalty += 1000 * h3 ** 2

        # Constraint h4
        h4 = 1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8 - individual[1]
        if h4 !=0:
            penalty += 1000 * h4 ** 2

        # Constraint h5
        h5 = 1000 * math.sin(individual[3] - 0.25) + 1000 * math.sin(individual[3] - individual[2] - 0.25) + 1294.8
        if h5 != 0:
            penalty += 1000 * h5 ** 2

        return penalty

    def epsilon_constraint(self, individual):
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
        if abs(h3) > 0.00001:
            individual[0] += h3
        # Constraint h4
        h4 = 1000 * math.sin(individual[2] - 0.25) + 1000 * math.sin(individual[2] - individual[3] - 0.25) + 894.8 - individual[1]
        if abs(h4) > 0.00001:
            individual[1] += h4
        # Constraint h5
        h5 = 1000 * math.sin(individual[3] - 0.25) + 1000 * math.sin(individual[3] - individual[2] - 0.25) + 1294.8
        if abs(h5) > 0.00001:
            individual[2] += h5

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
                child1 = self.enforce_constraints(child1)
                child2 = self.enforce_constraints(child2)
                new_population.append(child1)
                new_population.append(child2)

            population = new_population

        decision_variables = best_solution[:4] if best_solution is not None else None

        return self.evaluate(best_solution), decision_variables