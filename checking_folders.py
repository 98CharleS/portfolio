import os
from datetime import datetime
import csv
import concurrent.futures


def getting_folder_mod_time(*args):  # retuning date of modification as string
    print("Updating")
    x = args[0]
    try:  # checking if it is possible to access the location of X
        y = os.stat(x).st_mtime
        mod_date = datetime.fromtimestamp(y)
        print("Updated")
        return mod_date.strftime('%d.%m.%Y')
    except KeyboardInterrupt:
        print("Program stopped manually")
    except FileNotFoundError:
        print(f"Can't find the file {x}")
    except ValueError:
        print("Missing localization")


def run_with_timeout(func, args=(), kwargs={}, timeout_duration=5):
    # use to timeout if connection to folder takes too long (checking folders located in backup server)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            result = future.result(timeout=timeout_duration)
            return result
        except concurrent.futures.TimeoutError:
            print(f"Function timed out after {timeout_duration} seconds")
            return "Timeout"


def opening():
    # opening a spreadsheet with modificated valves and a spreadsheet connected with previous one
    print("Opening spreadsheets")
    os.startfile("folders_output.csv")
    os.startfile("Synchronizacje.xlsx")


"""def writing_file(x): # previous version without timeout, left in case
    print("Accessing data")
    folders_date = [(getting_folder_mod_time(i)) for i in x]  # getting mod time
    folders_out = dict(zip(x, folders_date))  # connecting folder localization with date of mod
    print("Saving data")
    f = open("folders_output.csv", "w", newline="")
    writer = csv.writer(f, delimiter=";")  # writing file with EU csv standard
    writer.writerows(folders_out.items())
    f.close()"""
# previous version without timeout, left in case


def writing_file(x):
    print("Accessing data")
    folders_date = [(run_with_timeout(getting_folder_mod_time, args=i, timeout_duration=5)) for i in x]
    # getting mod time
    folders_out = dict(zip(x, folders_date))  # connecting folder localization with date of mod
    print("Saving data")
    f = open("folders_output.csv", "w", newline="")
    writer = csv.writer(f, delimiter=";")  # writing file with EU csv standard
    writer.writerows(folders_out.items())
    f.close()


def main(f_input):
    folders = []
    print("Opening data")
    with open(f_input) as file:  # opening a spreadsheet with folders localizations
        reader = csv.reader(file)
        for row in reader:
            folders.append(row[0])
    writing_file(folders)  # pasting dates in other file
    opening()


if __name__ == '__main__':
    main("folders_date.csv")
