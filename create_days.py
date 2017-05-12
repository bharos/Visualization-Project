import csv
import random
f1=  open('data.tsv','w')

wr1 = csv.writer(f1, delimiter='	',quotechar='|', quoting=csv.QUOTE_MINIMAL,lineterminator='\n')

wr1.writerow(['month','day','value'])



for m in range(1,13):
	for d in range(1,32):
		val = random.randrange(0,200)

		wr1.writerow([m,d,val])

