import urllib.parse
from selenium import webdriver
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
def remove_blank_spaces(l):
    l2 = list()
    for i in l:
        if i == '':
            continue
        else:
            l2.append(i)
    return l2
def list2str(l):
    xs = ''
    for i in l:
        xs += str(i)
    return xs
def strdifference(str1, str2):
    list1 = list(str1)
    list2 = list(str2)
    l = len(list1)
    for i in range(0,l):
        if list1[i] == list2[0]:
            list2.pop(0)
        else:
            continue
    return list2str(list2)
def reversetilslash(str):
    revstr = str[::-1]
    res = ''
    for i in revstr:
        if i == '/':
            break
        else:
            res += i
    return res[::-1]
def elem(e,l):
    n = 0
    for i in l:
        if e == i:
            n += 1
        else:
            n += 0
    return n
def remove_commas(xs):
    l = list(xs)
    l.pop(-1)
    return list2str(l)
def divide_str_into_list(xs):
    l = xs.split()
    l = remove_blank_spaces(l)
    d = {0:''}
    m = 0
    for i in l:
        if i == 'and':
            m += 1
            d[m] = ''
        elif elem(',',i) > 0:
            d[m] += remove_commas(i)
            m += 1
            d[m] = ''
        else:
            d[m] += i + ' '
    return remove_blank_spaces(list(d.values()))
def dict_full_and_cropped(l):
    l1 = list()
    l2 = list()
    d = {'full':l1, 'cropped':l2}
    for i in l:
        ys = i.split()
        if elem('.',ys[0]) or :
            l2.append(i)
        else:
            l1.append(i)
    return d
def list_concat(xs,ys):
    return xs + ys
def list_to_dict(xs):
    products = reduce(list_concat,list(map(lambda ys: list(ys.keys()), xs)))
    props = reduce(list_concat, list(map(lambda ys: list(ys.values()), xs)))
    newdict = {}
    for i,k in enumerate(products):
        newdict[k] = props[i]
    return newdict
def get_2_cites_site(driver,ref):
    url = f'https://journals.aps.org/{ref[1]}/cited-by/10.1103/{ref[0]}'
    driver.get(url)
    myElem0 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'button')))
    print("Page is ready!")
    html0 = driver.page_source
    xpath = "//a[@class='button']"
    button = driver.find_element_by_xpath(xpath)
    button.click()
    myElem1 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'type-ahead')))
    print("Inst Login")
    # docpapers = BeautifulSoup(html, "html.parser")
    search = driver.find_element_by_xpath("//input[@class='wayfinder-form-control']")
    # search = docpapers.find('input', class_='wayfinder-form-control')
    search.click()
    search.send_keys('Sevilla')
    myElem2 = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//tr[@__gwt_row='1']")))
    print("Inst Found")
    htmlus = driver.page_source
    inst = driver.find_element_by_xpath("//tr[@__gwt_row='1']/td[@class='wayfinder-item-cell  wayfinder-item-displayname']")
    inst.click()
    myElem3 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'identificacion')))
    print("Ident")
    name = driver.find_element_by_xpath("//input[@id='edit-name']")
    passw = driver.find_element_by_xpath("//input[@id='edit-pass']")
    name.click()
    name.send_keys('adovazrui')
    passw.click()
    passw.send_keys('FeynmanBongos02')
    submit = driver.find_element_by_xpath("//input[@id='submit_ok']")
    submit.click()
    myElem0 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='citing article panel']")))
    return driver
def ref_itemNtype(item):
    urleach = item.find_element(By.XPATH, "//h5[@class='title']/a").get_attribute('href')
    for i in urleach:
        if i == 'g':
            break
        else:
            urleach = strdifference(i,urleach)
    urleach = strdifference('g/', urleach)
    tipo = ''
    for i in urleach:
        if i == '/':
            break
        else:
            tipo += i
    ref_number = reversetilslash(urleach)
    return [ref_number,tipo]
def authors_each_cite(item):
    authors_container = item.find_element(By.XPATH, ".//h6[@class='authors']")
    authors = authors_container.text
    return dict_full_and_cropped(divide_str_into_list(authors))
def cites(driver,ref):
    driver = get_2_cites_site(driver,ref)
    itemscites = driver.find_elements(By.XPATH, "//div[@class='citing article panel']")
    return list(map(authors_each_cite, itemscites))

start_time = time.time()

#urlpapers = 'https://journals.aps.org/search/results?clauses=%5B%7B"field":"author","value":"C+S+Wu","operator":"AND"%7D%5D&sort=oldest&date=custom&per_page=100&start_date=1939-12-31&end_date=1996-12-31'
urlgoogle = 'https://journals.aps.org/pr/abstract/10.1103/PhysRev.105.1413'

options = webdriver.ChromeOptions()
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
options.add_argument('headless')
chrome_driver_binary = r'C:\Users\Equipo\PycharmProjects\chromedriver-win64\chromedriver.exe'

#binary = FirefoxBinary(r'C:\Users\Equipo\PycharmProjects\geckodriver.exe')
#driver = webdriver.Chrome(chrome_driver_binary, options=options)
driver = webdriver.Firefox(executable_path=r'C:\Users\Equipo\PycharmProjects\geckodriver.exe')
driver.get(urlgoogle)

#myElem0 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'large-9 columns search-results ofc-main')))

myElem0 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//section[@class='article authors open']")))
print('author found')
cookies1 = driver.find_element_by_xpath("//a[@class='app__cookie-footer__button___34uYQ']")
cookies1.click()
myElem1 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//section[@class='article authors open']")))
s1 = driver.find_element(By.LINK_TEXT,'C. S. Wu')
s1.click()
driver.maximize_window()
myElem2 = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='large-9 columns search-results ofc-main']")))
print('papers Wu')
sr = driver.find_elements(By.XPATH, "//div[@class='article panel article-result']")

