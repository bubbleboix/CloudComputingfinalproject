#save the file as a csv format, excel is pretty wonky to deal with python
#Power BI does not offer data cleaning services.
#https://bitre.gov.au/statistics/safety/files/Fatal_Crashes_Sep_2016.csv
import csv
import urllib.request


response = urllib.request.urlopen('https://bitre.gov.au/statistics/safety/files/Fatal_Crashes_Sep_2016.csv')
html = response.read()

outfile2 = open('Input.csv','wb')
outfile2.write(html)

inputf =csv.reader(open("Input.csv","r"), delimiter=",")
crashes = open('InputClean.csv',"w")

#read csv file into array

fileLines = []
for line in inputf:
    fileLines.append(line)
lines = fileLines[1:]

fileLines[0][6]='Speed Group'
fileLines[0][0]='Quarter'

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
        lines[i][5] = 'Morning'
    elif hour >=13 and hour <= 18:
        lines[i][5] = 'Afternoon'
    elif hour >=19 and hour <=23:
        lines[i][5] = 'Night'
    else:
        lines[i][5] = 'Night'

#the Csv files also has an error with the months labourng them as numbers instead of months
Monthcol = [x[3] for x in lines]
for i,x in enumerate(Monthcol):
    if x == 'unknown':
        continue
    month = int(x)
    if month == 1:
        lines[i][3]='01.January'
    elif month == 2:
        lines[i][3]='02.February'
    elif month == 3:
        lines[i][3]='03.March'
    elif month == 4:
        lines[i][3]='04.April'
    elif month == 5:
        lines[i][3]='05.May'
    elif month == 6:
        lines[i][3]='06.June'
    elif month ==7:
        lines[i][3]='07.july'
    elif month == 8:
        lines[i][3]='08.August'
    elif month == 9:
        lines[i][3]='09.September'
    elif month == 10:
        lines[i][3]='10.October'
    elif month ==11:
        lines[i][3]='11.November'
    elif month ==12:
        lines[i][3]='12.December'

#concpet hierachry for months into quarters
for i,x in enumerate(Monthcol):
    if x =='unknown':
        continue
    month = int(x)
    if month >= 1 and month <=3:
        lines[i][0]='1st Quarter'
    elif month >=4 and month <=6:
        lines[i][0]='2nd Quarter'
    elif month >=7 and month <=9:
        lines[i][0]='3rd Quarter'
    elif month >=10 and month <=12:
        lines[i][0]='4th Quarter'

for i, x in enumerate(speedcol):
    if x == 'unknown':
        lines[i][6]='Speed E:Unknown'
        continue
    speed = int(x)
    if speed >= 80:
        lines[i][6]='Speed A:Very Fast'
    elif speed >=60 and speed <80:
        lines[i][6]='Speed B:Fast'
    elif speed >=40 and speed<60:
        lines[i][6]='Speed C:Medium'
    elif speed <40:
        lines[i][6]='Speed D:Slow'
  
    
        


#specfic the columns u want                
outputLines=['%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(r[1],r[2],r[0],r[3],r[4],r[5],r[7],r[8],r[9],r[10],r[6],r[11],r[12])for r in fileLines]
crashes.writelines(outputLines)
crashes.close()




    
    

    

