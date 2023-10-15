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
        if elem('.',ys[0]) or len(ys[0]) == 1:
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
def get_2_cites_site(driver, ref):
    driver2cites = driver
    url = f'https://journals.aps.org/{ref[1]}/cited-by/10.1103/{ref[0]}'
    driver2cites.get(url)
    myElem0 = WebDriverWait(driver2cites, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'button')))
    print("Page is ready!")
    html0 = driver2cites.page_source
    try:
        xpath = "//a[@class='button']"
        button = driver2cites.find_element_by_xpath(xpath)
        button.click()
        myElem1 = WebDriverWait(driver2cites, 30).until(EC.presence_of_element_located((By.ID, 'type-ahead')))
        print("Inst Login")
        # docpapers = BeautifulSoup(html, "html.parser")
        search = driver2cites.find_element_by_xpath("//input[@class='wayfinder-form-control']")
        # search = docpapers.find('input', class_='wayfinder-form-control')
        search.click()
        search.send_keys('Sevilla')
        myElem2 = WebDriverWait(driver2cites, 30).until(EC.element_to_be_clickable((By.XPATH, "//tr[@__gwt_row='1']")))
        print("Inst Found")
        htmlus = driver2cites.page_source
        inst = driver2cites.find_element_by_xpath(
            "//tr[@__gwt_row='1']/td[@class='wayfinder-item-cell  wayfinder-item-displayname']")
        inst.click()
        myElem3 = WebDriverWait(driver2cites, 30).until(EC.presence_of_element_located((By.ID, 'identificacion')))
        print("Ident")
        name = driver2cites.find_element_by_xpath("//input[@id='edit-name']")
        passw = driver2cites.find_element_by_xpath("//input[@id='edit-pass']")
        name.click()
        name.send_keys('adovazrui')
        passw.click()
        passw.send_keys('FeynmanBongos02')
        submit = driver2cites.find_element_by_xpath("//input[@id='submit_ok']")
        submit.click()
        myElem0 = WebDriverWait(driver2cites, 10000).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='pagination']")))
    except NoSuchElementException:
        myElem0 = WebDriverWait(driver2cites, 10000).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='pagination']")))
    return driver2cites
def ref_itemNtypeNdate(item):
    datext = item.find_element(By.XPATH, ".//h6[@class='citation']").text
    date = int(datext[-4:-1] + datext[-1])
    if date >= 1990 :
        resp = ''
    else:
        try:
            approved = item.find_element(By.XPATH, ".//h6[@class='tag']/span[@class='right']")
            urleach = item.find_element(By.XPATH, ".//h5[@class='title']/a").get_attribute('href')
            for i in urleach:
                if i == 'g':
                    break
                else:
                    urleach = strdifference(i, urleach)
            urleach = strdifference('g/', urleach)
            tipo = ''
            for i in urleach:
                if i == '/':
                    break
                else:
                    tipo += i
            ref_number = reversetilslash(urleach)
            resp = [ref_number, tipo, date]
        except NoSuchElementException:
            resp = ''
    return resp
def authors_each_cite(driver,item):
    driver.execute_script("arguments[0].scrollIntoView();", item)
    authors_container = item.find_element(By.XPATH, ".//div[@class='row']/div[@class='large-12 columns']/h6[@class='authors']")
    authors = authors_container.text
    dictauthors = dict_full_and_cropped(divide_str_into_list(authors))
    try:
        date_container = item.find_element(By.XPATH,
                                           ".//div[@class='row']/div[@class='large-12 columns']/h6[@class='pub-info']")
        datext = date_container.text
        date = int(datext[-5:-1])
        dictauthors.update({"date": date})
    except NoSuchElementException:
        pass
    return dictauthors
def cites(ref,d):
    start_time = time.time()
    options = webdriver.ChromeOptions()
    options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    options.add_argument('headless')
    driver = webdriver.Firefox(executable_path=r'C:\Users\Equipo\PycharmProjects\geckodriver.exe')
    drivercites = get_2_cites_site(driver,ref)
    itemscites = drivercites.find_elements(By.XPATH, "//div[@class='citing article panel']")
    paginationc = drivercites.find_element(By.XPATH, "//ul[@class='pagination']")
    paginationcites = paginationc.find_elements_by_xpath(".//li")
    numpgs = int((paginationcites[-2]).find_element_by_xpath(".//a").text)
    l1 = list()
    if numpgs == 1:
        for i in itemscites:
            try:
                l1.append(authors_each_cite(driver, i))
            except NoSuchElementException:
                pass
    else:
        for i in itemscites:
            try:
                l1.append(authors_each_cite(driver, i))
            except NoSuchElementException:
                pass
        for i in range(2, numpgs + 1):
            urlpg = f'https://journals.aps.org/{ref[1]}/cited-by/10.1103/{ref[0]}?page={i}'
            drivercites.get(urlpg)
            myElempg = WebDriverWait(drivercites, 10000).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='citing article panel']")))
            itemscites = drivercites.find_elements(By.XPATH, "//div[@class='citing article panel']")
            for i in itemscites:
                try:
                    l1.append(authors_each_cite(driver, i))
                except NoSuchElementException:
                    pass
    driver.quit()
    drivercites.quit()
    d[ref[2]].append(l1)
    return d
def refsNdates_per_page(driverref, int):
    urlrefs = f'https://journals.aps.org/search/results?sort=relevance&clauses=%5B%7B%22field%22:%22author%22,%22value%22:%22C+S+Wu%22,%22operator%22:%22AND%22%7D%5D&page={int}'
    driverref.get(urlrefs)
    driverref.maximize_window()
    myElem2 = WebDriverWait(driverref, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='large-9 columns search-results ofc-main']")))
    srpg = driverref.find_elements(By.XPATH, "//div[@class='article panel article-result']")
    refspg = list(map(ref_itemNtypeNdate, srpg))
    return refspg
driverres = turnon()
d = dict()
for i in range(1940,1990):
    d[i] = list()
refs0 = list()
for i in range(1,7):
    refs0 += refsNdates_per_page(driverres,i)

refs = list()
for i in refs0:
    if i == '':
        continue
    else:
        refs.append(i)
driverres.quit()
#res = list(map(cites,refs))
for i in range(1,len(refs)+1):
    d = cites(refs[i-1],d)

