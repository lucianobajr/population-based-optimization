import statistics

from pg import GeneticProgramming

# Configuration A: Penalty Estática
gp_a = GeneticProgramming(pop_size=100, num_generations=100, tournament_size=5, mutation_rate=0.1, penalty_method="static_penalty")
results_a = []
for _ in range(30):
    best_solutions_a = gp_a.run()
    results_a.append([gp_a.evaluate(solution) for solution in best_solutions_a])

# Configuration B: ɛ-constrained method
gp_b = GeneticProgramming(pop_size=100, num_generations=100, tournament_size=5, mutation_rate=0.1, penalty_method="epsilon_constraint")
results_b = []
for _ in range(30):
    best_solutions_b = gp_b.run()
    results_b.append([gp_b.evaluate(solution) for solution in best_solutions_b])

# Configuration A: Penalty Estática
table_a = []
for i, result in enumerate(results_a):
    row = [i + 1, statistics.mean(result), min(result), max(result), statistics.stdev(result)]
    table_a.append(row)

# Configuration B: ɛ-constrained method
table_b = []
for i, result in enumerate(results_b):
    row = [i + 1, statistics.mean(result), min(result), max(result), statistics.stdev(result)]
    table_b.append(row)

# Print the table
print("Configuration A: Penalty Static")
print("{:<5s} {:<10s} {:<10s} {:<10s} {:<10s}".format("Run", "Mean", "Min", "Max", "Std Dev"))
for row in table_a:
    print("{:<5d} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f}".format(*row))

print()

print("Configuration B: ɛ-constrained method")
print("{:<5s} {:<10s} {:<10s} {:<10s} {:<10s}".format("Run", "Mean", "Min", "Max", "Std Dev"))
for row in table_b:
    print("{:<5d} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f}".format(*row))