from datetime import datetime
from datetime import date
import os
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path + "/testingdatawa.csv",'r') as f:
    file_read = list(csv.reader(f))

for row in file_read[1:]:
    row[0]=datetime.strptime(row[0],"%b %d, %Y").strftime("%Y-%m-%d")

with open(dir_path + "/testingdatawa.csv",'w',newline='', encoding='utf-8') as f:
    write =csv.writer(f)
    write.writerows(file_read)
