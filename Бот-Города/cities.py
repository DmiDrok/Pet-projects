import csv

all_cities = []
with open("all_cities.csv", "r") as file:
    reader = csv.DictReader(file)

    for line in reader:
        all_cities.append(line["city_name"])

#uses_cities = {}
#with open("data//uses_cities.csv", "r") as file:
#    reader = csv.DictReader(file)
#
#    for line in reader:
#        uses_cities[line["city_name"]] = line["chat_id"] ##В ключе айди будет храниться имя города