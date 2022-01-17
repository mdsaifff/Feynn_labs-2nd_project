from bs4 import BeautifulSoup
import requests
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def make_data_row(link):
    html = BeautifulSoup(requests.get(link).text, 'lxml')
    data = []
    data.append(html.find('div', class_='projName').a.text)
    data.append(html.find('div', {'id': 'thirdFoldDisplay'}).find('div', class_='p_infoColumn').find('div', class_='p_value').a.text)
    rera = html.find('div', class_='descriptionCont').find_all('div', class_='p_infoRow')[4].find('div', class_='p_value')
    try:
        rera = rera.div.div.text
    except:
        rera = "NA"
    data.append(rera.split('(')[0])

    rate = html.find('span', class_='breakupdivider').text
    data.append(rate.replace('₹', ''))
    data.append(html.find('div', class_='descriptionCont').find_all('div', class_='p_infoRow')[6].find('div', class_='p_value').text)
    data.append(html.find('div', class_='descriptionCont').find_all('div', class_='p_infoRow')[7].find('div', class_='p_value').text)
    data.append(html.find('div', class_='descriptionCont').find_all('div', class_='p_infoRow')[8].find('div', class_='p_value').text)
    data.append(html.find('div', class_='descriptionCont').find_all('div', class_='p_infoRow')[9].find('div', class_='p_value').text)
    data.append(html.find('div', class_='seeBedRoomDimen').text)
    data.append(html.find('div', {'id': 'firstFoldDisplay'}).find_all('div', class_='p_infoColumn')[1].find('div', class_='p_value').text)
    data.append(html.find('div', {'id': 'fourthFoldDisplay'}).find_all('div', class_='p_infoColumn')[0].find('div', class_='p_value').text)
    data.append(html.find('div', class_='column col_2').find('div', class_='detailsVal').text)
    data.append(html.find('div', class_='column col_3').find('div', class_='detailsVal').text)

    ser = Service(r"C:\Users\KIIT\Downloads\chromedriver_win32\chromedriver.exe")
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    driver.get(link)

    element = driver.find_element(By.ID, "localityDetailTabId")
    desired_y = (element.size['height'] / 2) + element.location['y']
    current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script(
        'return window.pageYOffset')
    scroll_y_by = desired_y - current_y
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
    time.sleep(3)
    TEMPhtml = BeautifulSoup(driver.page_source, 'lxml')

    recomms = TEMPhtml.find('div', class_='recomLabel')
    res = ""
    sec=0
    while recomms is None:
        time.sleep(1)
        recomms = TEMPhtml.find('div', class_='recomLabel')
        sec += 1
        if sec >= 5:
            raise TimeoutError

    for s in recomms.find_all('span')[1:]:
        res = res + s.text + ','

    data.append(res)

    divs = TEMPhtml.find_all('div', class_='rateRate')

    for div in divs:
        for li in div.find_all('li'):
            data.append(str(len(li.find_all('span', class_='plus1'))))

    data.append(TEMPhtml.find('div', class_='eveRating').div.span.text)
    try:
        return list(map(lambda x: re.sub('\s+', '', x.decode('utf-8')), data))
    except:
        return list(map(lambda x: re.sub('\s+', '', x), data))
