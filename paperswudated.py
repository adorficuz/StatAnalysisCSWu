import urllib.parse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote
from selenium.webdriver.firefox.service import Service
import sys
sys.path.append(r'c:\users\equipo\appdata\local\programs\python\python311\lib\site-packages')
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import requests
import re
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import time
from functools import reduce
import json
from urllib.request import Request, urlopen
import functools
def turnon():
    start_time = time.time()

    # urlpapers = 'https://journals.aps.org/search/results?clauses=%5B%7B"field":"author","value":"C+S+Wu","operator":"AND"%7D%5D&sort=oldest&date=custom&per_page=100&start_date=1939-12-31&end_date=1996-12-31'
    urlgoogle = 'https://journals.aps.org/pr/abstract/10.1103/PhysRev.105.1413'

    options = webdriver.ChromeOptions()
    options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    options.add_argument('headless')
    chrome_driver_binary = r'C:\Users\Equipo\PycharmProjects\chromedriver-win64\chromedriver.exe'

    # binary = FirefoxBinary(r'C:\Users\Equipo\PycharmProjects\geckodriver.exe')
    # driver = webdriver.Chrome(chrome_driver_binary, options=options)
    driver = webdriver.Firefox(executable_path=r'C:\Users\Equipo\PycharmProjects\geckodriver.exe')
    driver.get(urlgoogle)

    # myElem0 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'large-9 columns search-results ofc-main')))

    myElem0 = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//section[@class='article authors open']")))
    print('author found')
    cookies1 = driver.find_element_by_xpath("//a[@class='app__cookie-footer__button___34uYQ']")
    cookies1.click()
    myElem1 = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//section[@class='article authors open']")))
    s1 = driver.find_element(By.LINK_TEXT, 'C. S. Wu')
    s1.click()
    driver.maximize_window()
    myElem2 = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='large-9 columns search-results ofc-main']")))
    print('papers Wu')
    return driver

def papers_per_page(driverref,ent,dict):
    urlrefs = f'https://journals.aps.org/search/results?sort=relevance&clauses=%5B%7B%22field%22:%22author%22,%22value%22:%22C+S+Wu%22,%22operator%22:%22AND%22%7D%5D&page={ent}'
    driverref.get(urlrefs)
    driverref.maximize_window()
    myElem2 = WebDriverWait(driverref, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='large-9 columns search-results ofc-main']")))
    srpg = driverref.find_elements(By.XPATH, "//div[@class='article panel article-result']//div[@class='row']//div[@class='large-9 columns']//h6[@class='citation']")
    for i in srpg:
        idate = int(i.text[-4:-1] + i.text[-1])
        if idate >= 1990:
            continue
        else:
            dict[idate] += 1
    return dict

driverres = turnon()
refs0 = list()
paperdates = dict()
for i in range(1940,1990):
    paperdates[i] = 0
for i in range(1,7):
    paperdates = papers_per_page(driverres,i,paperdates)
