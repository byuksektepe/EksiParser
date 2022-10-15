import datetime
import os
import re
import sqlite3
import time
from sqlite3 import Error

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import InvalidArgumentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_headers import Headers
import pyautogui

options = Options()
header = Headers(
    # generate any browser & os headeers
    headers=False  # don`t generate misc headers
)

headers = header.generate()
headless = True

emailSelector = "//input[@id='username']"
passwordSelector = "//input[@id='password']"
loginButtonSelector = "//div[@class='actions']/button[@class='btn btn-primary btn-lg btn-block']"

searchSelector = "//form[@id='search-form']/input[@id='search-textbox']"
searchButtonSelector = "//form[@id='search-form']/button"
humanSelector = "//label[.='insanlık testi']"

loginInCheckSelector = "//nav[@id='top-navigation']//li[contains(@class, 'messages')]"
global_wait_timeout = 10


def set_driver():
    coptions = webdriver.ChromeOptions()

    coptions.add_argument("--disable-blink-features")
    coptions.add_argument("--disable-blink-features=AutomationControlled")
    coptions.add_argument("ignore-certificate-errors")
    coptions.add_argument("--no-sandbox")
    coptions.add_argument("ignore-certificate-errors")
    coptions.add_argument("--no-sandbox")
    coptions.add_argument("disable-notifications")
    coptions.add_argument("--disable-infobars")
    coptions.add_argument("--disable-blink-features")
    coptions.add_argument("--disable-blink-features=AutomationControlled")
    coptions.add_argument("user-agent=" + str(headers['User-Agent']))

    if (headless):
        coptions.add_argument("--headless")
        coptions.add_argument("--window-size=1600,900")
    else:
        coptions.add_extension("ublock.crx")

    print("System : Fake User Agent : -> " + headers['User-Agent'])
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  # complete

    chrome_driver = webdriver.Chrome(desired_capabilities=caps,
                                     service=Service(ChromeDriverManager().install()),

                                     options=coptions)
    chrome_driver.maximize_window()
    return chrome_driver


driver = set_driver()


def send_keys(selector, text):
    key_el = driver.find_element(By.XPATH, selector)
    key_el.send_keys(text)
    time.sleep(0.5)


def click(selector):
    click_el = driver.find_element(By.XPATH, selector)
    click_el.click()
    time.sleep(0.5)


def switch_parent_window():
    parent = driver.window_handles[0]
    driver.switch_to.window(parent)


def close_child_window():
    child = driver.window_handles[1]
    driver.switch_to.window(child)


def check_element_exists(selector):
    element = False
    try:
        element = WebDriverWait(driver, global_wait_timeout).until(EC.presence_of_element_located((By.XPATH, selector)))
    except:
        print("Ignored Exception")

    return element


print("Otomatik ekşi entry girme programına hoşgeldiniz\nLütfen istenilen bilgileri eksiksiz giriniz.\n")

email = pyautogui.prompt(text='Lütfen ekşi sözlük E-Posta adresinizi giriniz: ', title='Ekşi Sözlük - EPosta',
                         default='')

password = pyautogui.password(text='Lütfen ekşi sözlük şifrenizi giriniz: ', title='Ekşi Sözlük - Şifre', default='',
                              mask='*')

login_url = "https://eksisozluk.com/giris"

# Set Web Driver and Navigate to URL 9Zvt7yZicqv4.u8
driver.get(login_url)
time.sleep(1)
send_keys(emailSelector, email)
send_keys(passwordSelector, password)

if not headless:
    human_el = check_element_exists(humanSelector)

    if human_el:
        alert = pyautogui.alert(
            text="İnsanlık Testi Tespit Edildi. Testi bir insanın yapması gerekli lütfen tamam tuşuna bastıktan sonra 30 saniye içinde insanlık testini doğrulayınız.",
            title="İnsanlık Testi", button="Tamam")


        time.sleep(20)

if headless:
    human_el = check_element_exists(humanSelector)

    if human_el:
        alert = pyautogui.alert(
            text="İnsanlık Testi Tespit Edildi. Headless False yapıp tekrar çalıştırınız.",
            title="İnsanlık Testi", button="Tamam")
        driver.quit()


click(loginButtonSelector)

login_check = check_element_exists(loginInCheckSelector)
if not login_check:
    alert = pyautogui.alert(
        text="Başaramadık abi",
        title="Login Başarısız", button="Tamam")
else:
    topic_title = pyautogui.prompt(text='Hangi konu başlığında entry yazmak istiyorsunuz?',
                                   title='Ekşi Sözlük - Konu Başlığı',
                                   default='')
    send_keys(searchSelector, topic_title)
    click(searchButtonSelector)


driver.quit()
