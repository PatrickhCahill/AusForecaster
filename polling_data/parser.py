from datetime import datetime
from datetime import date
import os
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))

with open("2022wapolls.csv",'r') as f:
    file_read = list(csv.reader(f))

for row in file_read[1:]:
    try:
        row[0]=datetime.strptime(row[0],"%b %d, %Y").strftime("%Y-%m-%d")
    except:
        print("Unable to convert startDate at row: ")
        print(row)
    try:
        row[1]=datetime.strptime(row[1],"%b %d, %Y").strftime("%Y-%m-%d")
    except:
        print("Unable to convert endDate at row: ")
        print(row)
    try:
        row[2]=row[2]
    except:
        print("Unable to process pollster at row: ")
        print(row)
    try:
        row[3]=row[3]
    except:
        print("Unable to process Mode at row: "+row)
    try:
        row[4]=row[4]
    except:
        print("Unable to process Scope at row: ")
        print(row)
    try:
        row[5] = row[5].replace(",","")
    except:
        print("Unable to process sample size at row: ")
        print(row)    
    try:
        if row[6]>=1:
            row[6] = int(row[6])/100
    except:
        print("Unable to process CoalitionResult at row: ")
        print(row)     
    try:
        if row[7]>=1:
            row[7] = int(row[7])/100
    except:
        print("Unable to process LaborResult at row: ")
        print(row)
    try:
        if row[8]>=1:
            row[8] = int(row[8])/100
    except:
        print("Unable to process GreensResult at row: ")
        print(row)
    try:
        if row[9]>=1:
            row[9] = int(row[9])/100    
    except:
        print("Unable to process PHONResult at row: ")
        print(row)  
    try:
        if row[10]>=1:
            row[10] = int(row[11])/100
    except:
        print("Unable to process UNDResult at row: ") 
        print(row)        
    
with open("2022wapolls.csv",'w',newline='', encoding='utf-8') as f:
    write =csv.writer(f)
    write.writerows(file_read)
