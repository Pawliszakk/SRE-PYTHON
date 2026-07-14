import csv

def test_csv_output():

    data = {"example.com": "192.168.0.1","example2.com": "192.168.0.2"}

    with open('data.csv', 'w', newline="") as f:
        columns = ["site","address"]
        writer = csv.DictWriter(f,fieldnames=columns)
        writer.writeheader()

        for row in data.items():
            writer.writerow(
                {columns[0]: row[0], columns[1]: row[1]}
            )
test_csv_output()