from third import GeneticProgramming
from csv_writer import CSVWriter

from table import ResultsTable

# Configuration A: Penalty Estática
gp_a = GeneticProgramming(pop_size=100, num_generations=100, tournament_size=10, mutation_rate=0.1, penalty_method="static_penalty")
results_a = []

for _ in range(5):
    best_solutions_a = gp_a.run()
    results_a.append(best_solutions_a)

csv_writer = CSVWriter(filename='./out/2-results-a.csv')
csv_writer.write_results(results_a)

# Configuration B: ɛ-constrained method
gp_b = GeneticProgramming(pop_size=100, num_generations=100, tournament_size=10, mutation_rate=0.1, penalty_method="epsilon_constraint")
results_b = []
for i in range(5):
    best_solutions_b= gp_b.run()
    results_b.append(best_solutions_b)

csv_writer = CSVWriter(filename='./out/2-results-b.csv')
csv_writer.write_results(results_b)


results_table = ResultsTable(filename_a='./out/2-results-a.csv', filename_b='./out/2-results-b.csv')
results_table.create_table()