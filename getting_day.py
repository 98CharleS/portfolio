import csv

number_of_days = []

with open("days_of_week.csv") as file:
    data = csv.DictReader(file)
    for row in data:
        number_of_days.append({"number": row["number"], "day": row["day"]})


def getting_day(day_num):
    x = number_of_days[day_num]
    print(x["day"])
