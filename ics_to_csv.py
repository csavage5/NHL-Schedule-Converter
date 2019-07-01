#Python 3.7.1

import csv
import string
import vobject
import io
import os
from datetime import datetime, timezone
import dateutil


def separateTeams(strTeams):
    home = ""
    away = ""
    word = ""
    selected = 0
    bracket = False
    order = ""
    #print(strTeams)

    for char in strTeams:        
        #print(word)
        if char != " " and bracket == False:
            #add current character to current word
            if char == '(':
                bracket = True
            else: 
                word += char


        elif char == " " :
            #check if found word is "at"
            if word == 'vs.' or word == 'at':
                #swap writing to away team
                #at: swap home and away
                selected = 1
                order = word
            
            # if found word wasn't 'at', then is part of home / away team name
            else :
                if selected == 0:
                    home += " " + word
                    
                elif selected == 1:
                    away += " " + word
                    
            word = ""

    if word != "":
        away += word
            
        #print( (home, away))
    
    if order == 'at':
        temp = home
        home = away
        away = temp

    return (home, away)
        
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

fileLoc = input(".ics file (input):")
fIn = open(fileLoc).read()

# if os.path.isfile('out.csv'):
# 	os.remove("out.csv")
	
# fOut = open("out.csv", "w")

#time = input("Timezone? (i.e. PST) ")

output = fileLoc[::-1].split('/', 1)[1][::-1]
print(output)

with open(output + '/out.csv', 'w') as fOut: 

    csv_writer = csv.writer(fOut)
    csv_writer.writerow(['Home Team', 'Away Team', 'Date', 'Start Time'])


    for cal in vobject.readComponents(fIn):
        
        #vobject.change_tz()

        for component in cal.components():
            
            #if component.name == "VEVENT" :
                
            #Separate home + away team
            teams = separateTeams(component.summary.value)
            
            #convert date
            date = component.dtstart.value
            strDate = date.strftime("%Y/%m/%d")

            #convert time from UTC to PT
            date.replace(tzinfo=timezone.utc).astimezone(tz=None)
            strTime = utc_to_local(date).strftime("%I:00 %p")

            #write to CSV
            csv_writer.writerow([teams[0], teams[1], strDate, strTime])
            fOut.flush()
            
fOut.close()