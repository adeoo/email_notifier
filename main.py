from utils import *
import pywintypes
from win10toast import ToastNotifier
import os
import time

email_list = ["moussaadel97@gmail.com"]


def main():
    time.sleep(60)

    # unila
    news = scrape_unila_news()
    latest_news = news[0]

    # pti
    editais = scrape_pti_editais()
    latest_edital = editais[0]

    unila_update, pti_update = check_updates(latest_news[0], latest_edital[0])
    write_to_json(latest_news[0], latest_edital[0])

    if unila_update:
        email_alert("Unila News", str(latest_news), email_list)

    if pti_update:
        email_alert("PTI Editais", str(latest_edital), email_list)


if __name__ == "__main__":
    main()
