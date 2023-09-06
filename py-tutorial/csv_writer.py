
import csv

#Write a csv file
# open the file in the write mode
f = open(r'c:\work\csv\1.csv', 'w')

# create the csv writer
writer = csv.writer(f,delimiter=',',lineterminator='\r')
row = [[1, 2, 3, 4, 5],[6,7,8,9,10,123,'abcd'],[1.1,2.2,3.3,12,"&$^$"]]
# write a row to the csv file
writer.writerow(row[0])
writer.writerow(row[1])
writer.writerow(row[2])
writer.writerows(row)

# close the file
f.close()

# To read a CSV file

f = open(r'c:\work\csv\1.csv', '+r')

reader = csv.reader(f)
for row in reader:
    print(row) 
f.close()