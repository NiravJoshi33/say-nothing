import csv

def load_csv(path) -> list:

    with open(path) as csv_file:
        reader = csv.DictReader(csv_file)

        data = []
        for row in reader:
            data.append(row)

        return data
        
        