import csv

with open("data/labels.csv") as csv_file:
    reader = csv.DictReader(csv_file)

    data = []
    for row in reader:
        data.append(row)

    total_entries = len(data)

    refuse_sum = 0
    empty_sum = 0
    caption_sum = 0

    for row in data:
        if row["action"] == "refuse":
            refuse_sum += 1
        elif row["action"] == "empty":
            empty_sum += 1
        elif row["action"] == "caption":
            caption_sum += 1
        else:
            raise ValueError(f"filename: {row["filename"]} has wrong action type {row["action"]}")

    print(total_entries == refuse_sum + empty_sum + caption_sum)

    print("refuse: ", refuse_sum)
    print("empty: ", empty_sum)
    print("caption: ", caption_sum)
    
    
    
    