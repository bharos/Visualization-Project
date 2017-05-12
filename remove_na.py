import csv
import datetime


month  = {}

f1=  open('clean_data.csv','w')
wr1 = csv.writer(f1, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL,lineterminator='\n')

with open('Kaagle_Upload.csv', 'rt') as f:

	reader = csv.reader(f)
	firstRow = next(reader)
	firstRow.append('month')

	print(firstRow)
	wr1.writerow(firstRow)

	for row in reader:
		if "NA" not in row and "-1" not in row :
			try:
				my_date = datetime.datetime.strptime(row[16], "%d/%m/%Y")
				d = my_date.strftime("%d %b, %Y").split(',')
				y = d[1].strip()
				d,m = d[0].split()
				# print(m+" "+y)

				row.append(m+" "+y)
				
				wr1.writerow(row)
			except:
				# print(row[16])
				pass