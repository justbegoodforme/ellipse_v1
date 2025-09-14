import csv

class Inject:

    def __init__(self, file):
        self.file = file
        self.data = []

    def inject_csv(self):
        with open(self.file, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter = ";")
            for row in csvreader:
                self.data.append(row)
            self.data[0][0] = self.data[0][0][1:]
            self.data = self.data[:-1]