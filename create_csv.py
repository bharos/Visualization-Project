import csv

f1=  open('sex_of_drivers.csv','w')
f2 = open('age_of_drivers.csv','w')
f3 = open('calendar_data.csv','w')

wr1 = csv.writer(f1, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL,lineterminator='\n')

wr2 = csv.writer(f2, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL,lineterminator='\n')
wr3 = csv.writer(f3, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL,lineterminator='\n')

wr1.writerow(['State','Male','Female'])
wr2.writerow(['State','18-30','31-40','41-50'])
wr3.writerow(['State','Day','Value'])

with open('Cleansed_data.csv', 'rt') as f:
            reader = csv.reader(f)
            firstRow = next(reader)
            geo_vals= {}
            row_list = []
            print(firstRow)


            for row in reader:
                row_list.append(row[:-1])
                
                if row[20] not in geo_vals.keys():
                    geo_vals[row[20]] = {}
                    geo_vals[row[20]]["male"] = 0
                    geo_vals[row[20]]["female"] = 0
                    geo_vals[row[20]]["a1"] = 0
                    geo_vals[row[20]]["a2"] = 0
                    geo_vals[row[20]]["a3"] = 0
                    geo_vals[row[20]]["day"] = {}


                if row[2] == '1':
                    geo_vals[row[20]]["male"] += 1
                elif row[2] == '2':
                    geo_vals[row[20]]["female"] += 1
                

                if int(row[3]) >= 18 and int(row[3]) <= 30:
                    geo_vals[row[20]]['a1'] += 1
                if int(row[3]) >= 31 and int(row[3]) <= 40:
                    geo_vals[row[20]]['a2'] += 1
                if int(row[3]) >= 42 and int(row[3]) <= 50:
                    geo_vals[row[20]]['a3'] += 1


                if row[12] not in geo_vals[row[20]]["day"].keys():
                    geo_vals[row[20]]["day"][row[12]] = 0


                geo_vals[row[20]]["day"][row[12]]  += 1



i = 0
list = []
for k in geo_vals.keys():

    if i == 30:
        break
    list.append(k)
    i+=1
    wr1.writerow([k,geo_vals[k]['male'],geo_vals[k]['female']])
    wr2.writerow([k,geo_vals[k]['a1'],geo_vals[k]['a2'],geo_vals[k]['a3']])
    print(geo_vals[k]['day'].keys())
    print(geo_vals[k]['day']['2'])
    for k1 in geo_vals[k]['day'].keys():
            wr3.writerow([k,k1,geo_vals[k]['day'][k1]])


print(list)