import sys

from core.heuristics.first import GeneticProgrammingFirst
from core.heuristics.second import GeneticProgrammingSecond

from utils.csv_writer import CSVWriter
from utils.table import ResultsTable

def bootstrap_first():
    # Configuration A: Penalty Estática
    gp_first_a = GeneticProgrammingFirst(pop_size=100, num_generations=100, tournament_size=10, mutation_rate=0.1, penalty_method="static_penalty")
    results_first_a = []

    for _ in range(30):
        best_solutions_a = gp_first_a.run()
        results_first_a.append(best_solutions_a)

    csv_writer = CSVWriter(filename='./out/1-results-a.csv',size=13)
    csv_writer.write_results(results_first_a)

    # Configuration B: ɛ-constrained method
    gp_second_b = GeneticProgrammingFirst(pop_size=100, num_generations=100, tournament_size=10, mutation_rate=0.1, penalty_method="epsilon_constraint")
    results_first_b = []
    for _ in range(30):
        best_solutions_b= gp_second_b.run()
        results_first_b.append(best_solutions_b)

    csv_writer = CSVWriter(filename='./out/1-results-b.csv',size=13)
    csv_writer.write_results(results_first_b)

    results_table = ResultsTable(filename_a='./out/1-results-a.csv', filename_b='./out/1-results-b.csv')
    results_table.create_table()

def bootstrap_second():
    # Configuration A: Penalty Estática
    gp_first_a = GeneticProgrammingSecond(pop_size=100, num_generations=100, tournament_size=10, mutation_rate=0.1, penalty_method="static_penalty")
    results_first_a = []

    for _ in range(30):
        best_solutions_a = gp_first_a.run()
        results_first_a.append(best_solutions_a)

    csv_writer = CSVWriter(filename='./out/2-results-a.csv',size=4)
    csv_writer.write_results(results_first_a)

    # Configuration B: ɛ-constrained method
    gp_second_b = GeneticProgrammingSecond(pop_size=100, num_generations=100, tournament_size=10, mutation_rate=0.1, penalty_method="epsilon_constraint")
    results_first_b = []
    for i in range(30):
        best_solutions_b= gp_second_b.run()
        results_first_b.append(best_solutions_b)

    csv_writer = CSVWriter(filename='./out/2-results-b.csv',size=4)
    csv_writer.write_results(results_first_b)

    results_table = ResultsTable(filename_a='./out/2-results-a.csv', filename_b='./out/2-results-b.csv')
    results_table.create_table()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <problem_option>")
        print("problem_option: 'first' or 'second'")
        sys.exit(1)
    
    problem = sys.argv[1]

    if problem == "first":
        bootstrap_first()
    elif problem == "second":
        bootstrap_second()
    else:
        print("Invalid Option!")