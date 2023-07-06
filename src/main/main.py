import numpy as np
from genetic_algorithm import GeneticAlgorithm

# Configurações do algoritmo genético
configurations = [
    {"name": "Configuração A", "penalty_method": "static"},
    {"name": "Configuração B", "penalty_method": "epsilon"}
]

# Dicionário para armazenar os resultados
results = {
    "Configuração A": {"fitness_values": [], "solutions": []},
    "Configuração B": {"fitness_values": [], "solutions": []}
}

# Executar o algoritmo 30 vezes para cada configuração
for config in configurations:
    for _ in range(30):
        # Criar uma instância do algoritmo genético com a configuração atual
        ga = GeneticAlgorithm(
            pop_size=100,
            max_generations=100,
            mutation_rate=0.1,
            crossover_rate=0.8,
            n_variables=13,
            n_inequality_constraints=9,
            epsilon=0.0001,
            penalty_method=config["penalty_method"]
        )

        # Executar o algoritmo genético
        best_solution, best_fitness = ga.genetic_algorithm()

        # Armazenar os resultados
        results[config["name"]]["fitness_values"].append(best_fitness)
        results[config["name"]]["solutions"].append(best_solution)

# Calcular estatísticas
statistics = {}
for config_name, result in results.items():
    fitness_values = result["fitness_values"]
    statistics[config_name] = {
        "Minimum": np.min(fitness_values),
        "Maximum": np.max(fitness_values),
        "Mean": np.mean(fitness_values),
        "Standard Deviation": np.std(fitness_values)
    }

# Imprimir resultados
print("Resultados:")
for config_name, stats in statistics.items():
    print(f"\n{config_name}:")
    for stat_name, value in stats.items():
        print(f"{stat_name}: {value}")