# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 14:27:45 2020

@author: rowss
"""
import requests
from bs4 import BeautifulSoup
import csv

p_name = input("Enter a players full name: ")
p_name = p_name.split(" ")
season = input("Enter the season (If you want to see the 2019-20 season, type in 2020): ")
#stat = input("Enter the stat you want to see plotted over the course of the " + str(int(season)-1)+ '-'+ season + " season (PTS, REB, AST): ")

if(len(p_name[1])<5):
    if(len(p_name)>2):
        name = ""
        for char in p_name[1:]:
            name = name + char
            if len(name)== 5:
                break
        url = "https://www.basketball-reference.com/players/" + p_name[1][0]+ '/' + name + p_name[0][0:2] + '01/gamelog/'+season
    else:
        url = "https://www.basketball-reference.com/players/" + p_name[1][0]+ '/' + p_name[1] + p_name[0][0:2] + '01/gamelog/'+season
else:
    url = "https://www.basketball-reference.com/players/" + p_name[1][0]+ '/' + p_name[1][0:5] + p_name[0][0:2] + '01/gamelog/'+season

url = url.lower()

result = requests.get(url)

if(result.status_code==200):
    print("Retrieved Successfully")
else:
    print("Not retrieved")

make_csv = input("Write to csv file? ")
if make_csv == "y" or make_csv == "yes":
    file_name = p_name[0]+ '_' + p_name[1] + '_' + season +'stats.csv'
    
src = result.content



soup = BeautifulSoup(src, 'lxml')
head = soup.find('thead')

header = soup.find('thead')
new_header = header.text.replace("\n", ",")
new_header = new_header[2:-2]
new_header = new_header.split(",")


tbody = soup.find('tbody') 
tr = tbody.find_all('tr')

with open(file_name, 'w', newline ='') as new_file:
    csv_write = csv.writer(new_file)
    csv_write.writerow(new_header)
    total_g = -1
    for stat in tr: #list of all tr datas in tbody
        data = stat.find_all("td") 
        total_g +=1
        if 'thead' in str(stat):
            continue
        write_row = []
        for x in range(len(data)):
            if x == 0:
                games = tr[total_g].th.text
                write_row.append(games)
                stats = data[x].text
            elif x == len(data)-1:
                stats = data[x].text
            else:
                stats = data[x].text
            write_row.append(stats)
        csv_write.writerow(write_row)
