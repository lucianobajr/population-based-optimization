import csv

class CSVWriter:
    def __init__(self, filename, size):
        self.filename = filename
        self.size = size

    def write_results(self, results):
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            if self.size == 4:
                writer.writerow(['Objective Function', 'X1', 'X2', 'X3', 'X4' ])
            else:
                writer.writerow(['Objective Function', 'X1', 'X2', 'X3', 'X4','X5', 'X6', 'X7', 'X8', 'X9', 'X10', 'X11', 'X12', 'X13' ])

            for result in results:
                objective_value = result[0]
                decision_variables = list(result[1])
                writer.writerow([objective_value] + decision_variables)