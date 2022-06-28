import urllib3
import xml.etree.ElementTree as ET


def get_usd_rub_price():
    '''
        Функция запроса котировок USD_RUB на текущий день 
    '''
    URL = 'https://www.cbr.ru/scripts/XML_daily.asp'
    http = urllib3.PoolManager()
    resp = http.request('GET', URL)
    data = resp.data.decode("windows-1251")

    root = ET.fromstring(data)
    valutes = root.findall('Valute')
    for valute in valutes:
        if (valute.attrib['ID'] == 'R01235'):
            value = valute.find('Value').text
    
    return float(value.replace(',', '.'))