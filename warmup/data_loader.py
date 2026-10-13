import csv

def load_csv() -> list:

    with open("data/labels.csv") as csv_file:
        reader = csv.DictReader(csv_file)

        data = []
        for row in reader:
            data.append(row)

        return data
        
        