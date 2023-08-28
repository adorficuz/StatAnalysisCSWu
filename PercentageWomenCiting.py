import urllib.parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote
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
        if elem('.',ys[0]):
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
    url = f'https://journals.aps.org/pr/cited-by/10.1103/{ref}'
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
    myElem2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//tr[@__gwt_row='6']")))
    print("Inst Found")
    htmlus = driver.page_source
    inst = driver.find_element_by_xpath("//tr[@__gwt_row='6']")
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
    myElem4 = WebDriverWait(driver, 2)
    htmlf = driver.page_source
    return htmlf
def ref_item(item):
    urleach = 'https://journals.aps.org' + item.find('a')['href']
    general_link = 'https://journals.aps.org/pr/abstract/10.1103/'
    ref_number = strdifference(general_link, urleach)
    return ref_number
def authors_each_cite(item):
    authors_container = item.find(class_= 'authors')
    authors = authors_container.text
    return dict_full_and_cropped(divide_str_into_list(authors))
def cites(driver,ref):
    htmlcites = get_2_cites_site(driver,ref)
    doccites = BeautifulSoup(htmlcites, "html.parser")
    itemscites = doccites.find_all(class_='citing article panel')
    return list(map(authors_each_cite, itemscites))


start_time = time.time()
urlpapers = 'https://journals.aps.org/search/results?clauses=%5B%7B"field":"author","value":"C+S+Wu","operator":"AND"%7D%5D&sort=oldest&date=custom&per_page=100&start_date=1939-12-31&end_date=1996-12-31'

options = webdriver.ChromeOptions()
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
options.add_argument('headless')
chrome_driver_binary = r'C:\Users\EQUIPO\PycharmProjects\chromedriver-win64\chromedriver.exe'
driver = webdriver.Chrome(chrome_driver_binary, options=options)
driver.get(urlpapers)
myElem0 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'article panel article-result')))
html = driver.page_source
docpapers = BeautifulSoup(html, "html.parser")

div = docpapers.find_all(class_= 'article panel article-result')
#res = list(map(cites,list(map(ref_item, div))))
res = cites(driver,ref_item(div[0]))

