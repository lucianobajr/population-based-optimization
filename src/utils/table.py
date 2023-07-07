import pandas as pd

class ResultsTable:
    def __init__(self, filename_a, filename_b):
        self.filename_a = filename_a
        self.filename_b = filename_b

    def create_table(self):
        # Ler os dados dos arquivos CSV
        data_a = pd.read_csv(self.filename_a)
        data_b = pd.read_csv(self.filename_b)

        min_a, max_a, mean_a, std_a = data_a['Objective Function'].min(), data_a['Objective Function'].max(), data_a['Objective Function'].mean(), data_a['Objective Function'].std()
        min_b, max_b, mean_b, std_b = data_b['Objective Function'].min(), data_b['Objective Function'].max(), data_b['Objective Function'].mean(), data_b['Objective Function'].std()

        # Obter o valor mínimo da função objetivo
        min_obj_value_a = data_a['Objective Function'].min()
        min_obj_value_b = data_b['Objective Function'].min()

        # Filtrar os dados para a linha com o valor mínimo da função objetivo
        filtered_data_a = data_a[data_a['Objective Function'] == min_obj_value_a]
        filtered_data_b = data_b[data_b['Objective Function'] == min_obj_value_b]
        
        # Calcular estatísticas para as variáveis de decisão
        decision_variables_a = filtered_data_a.iloc[0, 1:]
        decision_variables_b = filtered_data_b.iloc[0, 1:]

        # Criar a tabela
        table_data = {
            'Nome do Algoritmo': ['Static Penalty', 'Epsilon Constraint'],
            'Mínimo': [min_a, min_b],
            'Máximo': [max_a, max_b],
            'Média': [mean_a, mean_b],
            'Desvio Padrão': [std_a, std_b]
        }
        for i in range(1, 5):
            table_data[f'X{i}'] = [decision_variables_a[i-1], decision_variables_b[i-1]]

        table = pd.DataFrame(table_data)

        # Criar a tabela
        table_data = {
            'Nome do Algoritmo': ['Static Penalty', 'Epsilon Constraint'],
            'Mínimo': [min_a, min_b],
            'Máximo': [max_a, max_b],
            'Média': [mean_a, mean_b],
            'Desvio Padrão': [std_a, std_b]
        }

        for i in range(1, 5):
            table_data[f'X{i}'] = [decision_variables_a[i-1], decision_variables_b[i-1]]

        table = pd.DataFrame(table_data)

        # Imprimir a tabela
        print(table)
        return table