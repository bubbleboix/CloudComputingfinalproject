#save the file as a csv format, excel is pretty wonky to deal with python
#Power BI does not offer data cleaning services.
#https://bitre.gov.au/statistics/safety/files/Fatal_Crashes_Sep_2016.csv
import csv
import urllib.request
from os import path

response = urllib.request.urlopen('https://bitre.gov.au/statistics/safety/files/Fatal_Crashes_Sep_2016.csv')
html = response.read()
outfile2 = open('testing2.csv','wb')
outfile2.write(html)

filename= path.expanduser('Desktop')+'crashes.csv'
inputf =csv.reader(open("testing2.csv","r"), delimiter=",")
crashes = open(filename,"w")

#read csv file into array
fileLines = []
for line in inputf:
    fileLines.append(line)
lines = fileLines[1:]

#replacing blank cells with unknown,never delete due to the other attributes might sway the analysze.     
for i, line in enumerate(lines):
    for j, cell in enumerate(line):
        if cell == " ":
            lines[i][j] = 'unknown'

            
#replacing weird speed limits with upperbound of 110km and amount lower then 40
speedcol = [x[-1] for x in lines]
for i, x in enumerate(speedcol):
    if x == 'unknown':
        continue
    speed = int(x)
    if speed > 110:
        lines[i][-1] ='110'
    elif speed < 40:
        lines[i][-1] ='40'

#Do a simple concept hierachary to grow time of the day to morning,noon and night
for i, x in enumerate(lines):
    if x[5] == 'unknown':
        continue
    hour = int(x[5])
    if  hour >= 4 and hour <= 12:
        lines[i][5] = 'morning'
    elif hour >=13 and hour <= 18:
        lines[i][5] = 'afternoon'
    elif hour >=19 and hour <=23:
        lines[i][5] = 'night'
    else:
        lines[i][5] = 'night'

#the Csv files also has an error with the months labourng them as numbers instead of months
Monthcol = [x[3] for x in lines]
for i,x in enumerate(Monthcol):
    if x == 'unknown':
        continue
    month = int(x)
    if month == 1:
        lines[i][3]='Jan'
    elif month == 2:
        lines[i][3]='Feb'
    elif month == 3:
        lines[i][3]='March'
    elif month == 4:
        lines[i][3]= 'April'
    elif month == 5:
        lines[i][3]= 'May'
    elif month == 6:
        lines[i][3]='June'
    elif month ==7:
        lines[i][3]='july'
    elif month == 8:
        lines[i][3]= 'August'
    elif month == 9:
        lines[i][3]= 'Sep'
    elif month == 10:
        lines[i][3]='Oct'
    elif month ==11:
        lines[i][3]='Nov'
    elif month ==12:
        lines[i][3]='Dec'

#specfic the columns u want                
outputLines=['%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(r[1],r[2],r[3],r[4],r[5],r[7],r[8],r[9],r[10],r[11],r[12])for r in fileLines]
crashes.writelines(outputLines)
crashes.close()




    
    

    

