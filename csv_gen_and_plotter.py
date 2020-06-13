import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import datetime as dt  # use datetime to plot 'Date' by month


class Player:
    x_axis = "Rk"  # by default it graphs total games in a season vs points in a single game
    y_axis = "PTS"

    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.file_name = None

    def get_url(self):
        p_name = self.name
        p_name = p_name.split(" ")
        season = self.year

        if len(p_name[1]) < 5:
            if len(p_name) > 2:
                name = ""
                for char in p_name[1:]:
                    name = name + char
                    if len(name) == 5:
                        break
                url = "https://www.basketball-reference.com/players/" + p_name[1][0] + '/' + name + p_name[0][
                       0:2] + '01/gamelog/' + season
            else:
                url = "https://www.basketball-reference.com/players/" + p_name[1][0] + '/' + p_name[1] + p_name[0][
                       0:2] + '01/gamelog/' + season
        else:
            url = "https://www.basketball-reference.com/players/" + p_name[1][0] + '/' + p_name[1][0:5] + p_name[0][
                   0:2] + '01/gamelog/' + season
        self.file_name = p_name[0] + '_' + p_name[1] + '_' + season + 'stats.csv'
        url = url.lower()
        return url

    def write_csv(self):
        result = requests.get(self.get_url())
        if result.status_code == 200 and self.get_url() != 'https://www.basketball-reference.com/players/':
            print("Player stats retrieved successfully")
        else:
            print("Player could not be found. Maybe you typed in the name incorrectly or "
                  "you entered an invalid season")
            return False

        make_csv = input("Write to csv file? Type no if you already have the file.\t")
        if make_csv != 'y' and make_csv != 'yes':
            return False

        src = result.content

        soup = BeautifulSoup(src, 'lxml')

        header = soup.find('thead')
        new_header = header.text.replace("\n", ",")
        new_header = new_header[2:-2]
        new_header = new_header.split(",")

        tbody = soup.find('tbody')
        tr = tbody.find_all('tr')

        with open(self.file_name, 'w', newline='') as new_file:
            csv_write = csv.writer(new_file)
            csv_write.writerow(new_header)
            total_g = -1
            for stat in tr:  # list of all tr datas in tbody
                data = stat.find_all("td")
                total_g += 1
                if 'thead' in str(stat):
                    continue
                write_row = []
                for x in range(len(data)):
                    if x == 0:
                        games = tr[total_g].th.text
                        write_row.append(games)
                        stats = data[x].text
                    elif x == len(data) - 1:
                        stats = data[x].text
                    else:
                        stats = data[x].text
                    write_row.append(stats)
                csv_write.writerow(write_row)

    @classmethod
    def axes(cls):
        change_axis = input(f"Would you like to change the axes? X is currently {cls.x_axis}, "
                            f"Y is currently {cls.y_axis}\t")
        change_axis = change_axis.lower()
        if change_axis == 'y' or change_axis == 'yes':
            cls.x_axis = input("What do you want to be on the x-axis? ('Rk' or 'G' is recommended, 'Date' currently "
                               "has limited functionality)\t")
            cls.y_axis = input("What do you want to be on the y-axis? (Type in same was listed in CSV)\t")
        else:
            return False

    def graph(self):
        reader = pd.read_csv(self.file_name, encoding='latin1')
        if reader.plot.scatter(self.x_axis, self.y_axis):
            reader.plot.scatter(self.x_axis, self.y_axis, title= f"{self.name}, {str(int(self.year)-1)}-{self.year}")
            return True
        else:
            print("The x or y axis entered is not valid")
            raise TypeError("Invalid axis")


enter_name = input("Enter a players full name: ")
enter_season = input("Enter the season (If you want to see the 2019-20 season, type in 2020): ")
player = Player(enter_name, enter_season)
player.write_csv()
player.axes()
player.graph()
