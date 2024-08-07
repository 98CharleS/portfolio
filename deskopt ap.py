from datetime import date
from getting_day import getting_day
import os
import checking_folders
import eZam_API

today = date.today()
today_weekday = date.weekday(today)
user_name = os.environ.get("USERNAME")


def greeting_massage(day):
    print(f"Hello, {user_name}\nIt's:")
    getting_day(date.weekday(day))


def main(x):
    greeting_massage(x)
    checking_folders.main()
    eZam_API.main()


if __name__ == '__main__':
    main(today)

