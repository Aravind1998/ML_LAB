import csv
hypo = [0,0,0,0]

with open('Test-data.csv') as csv_file :
    readcsv = csv.reader(csv_file,delimiter = ',')
    print(readcsv)
    data = []
    print("Examples are :")
    for row in readcsv:
        print(row)
        if row[len(row)-1].upper() == "T":
            data.append(row)
print("Positive examples are :-")
for x in data:
    print(x)

TotalExamples = len(data)
i = 0
print("Steps of Find-S algorithm are\n",hypo)
list = []
p = 0
d = len(data[p]) -1
for j in range(d):
    list.append(data[i][j])
hypo = list
i = 1

for i in range(TotalExamples):
    for k in range(d):
        if hypo[k] != data[i][k]:
            hypo[k] = '?'
        else:
            hypo[k]
print(hypo)
