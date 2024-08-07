import requests
from datetime import datetime
from datetime import timedelta
import ctypes

today = datetime.today()
# time of week used to check if there's a newer deal than w week old (time to apply is usually about 2 weeks)
week = timedelta(days=7)
last_week = today - week

# converting today time to format used in eZam service
t_y = today.strftime('%Y')
t_m = today.strftime('%m')
t_d = today.strftime('%d')

# converting time a week ago to format used in eZam service
lw_y = last_week.strftime('%Y')
lw_m = last_week.strftime('%m')
lw_d = last_week.strftime('%d')

ending = t_y + "-" + t_m + "-" + t_d + "T23:59:59"
starting = lw_y + "-" + lw_m + "-" + lw_d + "T00:00:00"
# cpv is code which specific a kind of work to be made in deal
cpv = "44212200-1"

# link to access eZam API
link = ("https://ezamowienia.gov.pl/mo-board/api/v1/notice?NoticeType=ContractNotice&TenderType=1.1.1&CpvCode=" + cpv +
        "&PublicationDateFrom=" + starting + "&PublicationDateTo=" + ending + "&PageSize=100")


names_of_deals = []


def message_box(xlist):
    # showing box with a massage to user
    if not xlist:
        ctypes.windll.user32.MessageBoxW(0, "There's nothing new...", "eZam actualization")
    else:
        ctypes.windll.user32.MessageBoxW(0,
                                         "There's new deal:\n\n"+"\n".join(map(str, xlist)),
                                         "eZam actualization",
                                         )


def show_deals(data):

    def getting_deals():
        return deal["orderObject"]

    # making a list of deals then pop out info
    list_of_deals = data.json()
    for deal in list_of_deals:
        names_of_deals.append(getting_deals())
    message_box(names_of_deals)


def main():

    try:  # checking if eZam is available
        data = requests.get(link, timeout=2)
        data.raise_for_status()
        show_deals(data)
    except requests.exceptions.Timeout:
        print("Connection to eZam timeout")
    except requests.exceptions.RequestException as error:
        print(f"{error} error")


if __name__ == '__main__':
    main()
