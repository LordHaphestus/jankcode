import csv
name = 'Carina pi�a'

with open ('test.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(name)
