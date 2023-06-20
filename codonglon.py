from os import read
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import numpy as np
import datetime as dt
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def read_data_from_csv(ticker):
    try:
        df = pd.read_csv(
            'company_name.csv')
    except:
        print('An exception occurred')
    else:
        return (df)


filter = read_data_from_csv('filter')
count = 0

for i in range(len(filter)):
    name_stock = filter.iloc[i]['name']
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = f'https://s.cafef.vn/Lich-su-giao-dich-{name_stock}-3.chn#data'
    driver.get(url)
    ignored_exceptions = (NoSuchElementException,
                          StaleElementReferenceException)
    next_page = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(@title,"Next to Page")]')))
    actions = ActionChains(driver)

    def scrape_page():
        tr = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_all_elements_located((By.XPATH, '//tr[contains(@id,"ContentPlaceHolder1_ctl03_rptData")]')))
        with open('data17.txt', 'a', encoding='utf-8') as f:
            for t in tr:
                f.write(f'{name_stock},'+t.get_attribute('innerText') + "\n")
    while next_page:
        try:
            next_page = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@title,"Next to Page")]')))
            scrape_page()
            driver.implicitly_wait(10)
            actions.move_to_element(next_page).click().perform()
            time.sleep(0.8)
        except StaleElementReferenceException:
            next_page = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@title,"Next to Page")]')))
            actions.move_to_element(next_page).click().perform()
        except TimeoutException:
            scrape_page()
            time.sleep(0.7)
            driver.quit()
            break
