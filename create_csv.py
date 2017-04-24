import csv

f1=  open('sex_of_drivers.csv','w')
f2 = open('age_of_drivers.csv','w')
wr1 = csv.writer(f1, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL,lineterminator='\n')

wr2 = csv.writer(f2, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL,lineterminator='\n')
wr1.writerow(['State','Male','Female'])
wr2.writerow(['State','18-30','31-40','41-50'])


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




for k in geo_vals.keys():
    wr1.writerow([k,geo_vals[k]['male'],geo_vals[k]['female']])
    wr2.writerow([k,geo_vals[k]['a1'],geo_vals[k]['a2'],geo_vals[k]['a3']])