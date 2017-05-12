import csv


f1=  open('clean_data2.csv','w')
month = {}
wr1 = csv.writer(f1, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL,lineterminator='\n')

wr1.writerow(['date','price'])

with open('clean_data.csv', 'rt') as f:

	reader = csv.reader(f)
	firstRow = next(reader)

	for row in reader:
		if row[25] not in month:
			month[row[25]] = 0

		month[row[25]] += 1



for m in month.keys():
	wr1.writerow([m,month[m]])