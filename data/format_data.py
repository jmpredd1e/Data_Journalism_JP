import json 
'''
What I have to do 
-Create a dictonary that goes through each date in Janurary 
-Inside each date is another dictonary that tells number of each bourgough
-Inside that bourgough dictonary are dictonaries for each race 
-Inside the race ditonaries is displayed, men:num, women:num, total:num
Ex
Januarary{
    01{
        Manhattahan{
            Black{
                Men:num
                Women:num
                Total:num
            }
        }
    }
}

'''
Jan = {}


f1 = open("data/NYPD_clean_arrest_data.csv","r")
lines = f1.readlines()
for i in range(1,32):
    key = f"{i:02}"
    Jan[key]= {}
for i in range(1, len(lines)): 
    #split into seperate dates
    temp = lines[i].split(",")
    temp_2 = temp[0].split("/")
    date = temp_2[1]
    if temp[1] == "M":
        borough = "Manhattan"
    elif temp[1] == "K":
        borough = "Brooklyn"
    elif temp[1] == "Q":
        borough = "Queens"
    elif temp[1] == "B":
        borough = "Bronx"
    elif temp[1] == "S":
        borough = "Staten Island"
    gender = temp[2]
    race = temp[3].strip()
    #define the borough dictonary
    if borough not in Jan[date]:
        Jan[date][borough] = {}
    if race not in Jan[date][borough]:
        Jan[date][borough][race] = {"Men": 0, "Women": 0, "Total": 0}
    #Update counting 
    if gender == "M":
        Jan[date][borough][race]["Men"] += 1
        Jan[date][borough][race]["Total"] += 1
    elif gender == "F":
        Jan[date][borough][race]["Women"] += 1
        Jan[date][borough][race]["Total"] += 1


f2 = open("data/data.json", "w")
json.dump(Jan, f2, indent = 4)

f2.close()
    
