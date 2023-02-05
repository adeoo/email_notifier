import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import json
import urllib.request
import os


def connected(host='http://google.com'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False


# sends email
def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)

    # Gmail API key
    user = os.environ.get('EMAIL_ADDRESS')
    password = os.environ.get('EMAIL_PASSWORD')

    msg['from'] = user
    msg['subject'] = subject
    msg['to'] = to

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()


# Scrapes unila news webpage, returns news list with news[i] = [date_text, title_text, description_text, link]
def scrape_unila_news():
    news_list = []
    r = requests.get("https://portal.unila.edu.br/noticias")
    html_text = r.text
    soup = BeautifulSoup(html_text, "lxml")

    for article in soup.find_all('article', class_='tileItem'):
        title = article.find('a', class_='summary url')
        title_text = title.text
        description_text = article.find('span', class_="description").text
        date_text = article.find('span', class_="summary-view-icon").text.lstrip().rstrip()
        link = title['href']

        noticia = [date_text, title_text, description_text, link]
        news_list.append(noticia)
    return news_list


# Scrapes PTI editais webpage, returns editales list with editales[i] =  [title_text, description_text]
def scrape_pti_editais():
    editais_list = []
    r = requests.get("https://www.pti.org.br/editais-bolsas/")
    html_text = r.text
    soup = BeautifulSoup(html_text, "lxml")

    for article in soup.find_all('div', class_='elementor-toggle-item'):
        title = article.find('a', class_='elementor-toggle-title')
        title_text = title.text
        description_text = article.find('p').text

        edital = [title_text, description_text]
        editais_list.append(edital)
    return editais_list


def write_to_json(unila, pti):
    dictionary = {
        "unila": str(unila),
        "pti": str(pti)
    }

    # Serializing json
    json_object = json.dumps(dictionary, indent=4)

    # Writing to sample.json
    with open("latest.json", "w") as outfile:
        outfile.write(json_object)


def check_updates(new_unila, new_pti):
    with open('latest.json', 'r') as openfile:
        # Reading from json file
        latest_json = json.load(openfile)

        if latest_json['unila'] != new_unila:
            unila_update = True
        else:
            unila_update = False

        if latest_json['pti'] != new_pti:
            pti_update = True
        else:
            pti_update = False

        return unila_update, pti_update
