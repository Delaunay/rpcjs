import requests
import html5lib
from xml.etree.ElementTree import Element
from bs4 import BeautifulSoup


PRE = '{http://www.w3.org/1999/xhtml}'

button_object = 'https://www.w3schools.com/jsref/dom_obj_button.asp'

r = requests.get(button_object)


def read_page(content):
    soup = BeautifulSoup(content, 'html5lib')
    tables = soup.body.find_all('table')

    headers = None
    data = []

    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            if headers is None:
                headers = [h.text for h in row.find_all('th')]

            else:
                cols = row.find_all('td')
                columns = {}
                for k, col in zip(headers, cols):
                    columns[k] = col.text
                data.append(columns)

    print(data)


read_page(r.content)
