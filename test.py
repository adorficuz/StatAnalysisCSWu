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
start_time = time.time()
ref = input()
url = f'https://journals.aps.org/pr/cited-by/10.1103/{ref}'
options = webdriver.ChromeOptions()
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
options.add_argument('headless')
chrome_driver_binary = r'C:\Users\EQUIPO\PycharmProjects\chromedriver-win64\chromedriver.exe'
driver = webdriver.Chrome(chrome_driver_binary, options=options)
driver.get(url)
myElem0 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'button')))
print("Page is ready!")
html0 = driver.page_source
xpath = "//a[@class='button']"
button = driver.find_element_by_xpath(xpath)
button.click()
myElem1 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'type-ahead')))
print("Inst Login")
#docpapers = BeautifulSoup(html, "html.parser")
search = driver.find_element_by_xpath("//input[@class='wayfinder-form-control']")
#search = docpapers.find('input', class_='wayfinder-form-control')
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
myElem4 = WebDriverWait(driver, 3)
htmlf = driver.page_source