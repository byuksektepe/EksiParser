import datetime
import os
import re
import sqlite3
import time
from sqlite3 import Error

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import InvalidArgumentException, NoSuchElementException, TimeoutException
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
import random
import scipy.interpolate as si

options = Options()
header = Headers(
    # generate any browser & os headeers
    headers=False  # don`t generate misc headers
)

headers = header.generate()

print("Otomatik ekşi entry girme programına hoşgeldiniz\nLütfen istenilen bilgileri eksiksiz giriniz.\n")
time.sleep(0.6)
print("-> Not -> Otomasyonu tarayıcı görünür vaziyette çalıştırmak, robot testine takılmanıza neden olabilir."
      " Eğer bu konuda sorun yaşıyorsanız bir sonraki sorunda 'hayır(H/h)' cevabı veriniz.")

while 1:

    headless_option = (
        input("-> ? -> Otomasyon çalışırken tarayıcıyı görmek ister misiniz? '--headless' (e/h) \n")).lower()

    if headless_option == "e":
        headless = False
        break

    elif headless_option == "h":
        headless = True
        break
    elif headless_option == "exit":
        exit()
        break
    else:
        print(
            "-> Hata -> Lütfen sadece Hayır için : (h-H) veya Evet için : (e-E) cevabı veriniz. Çıkmak için (exit) yazınız.\n")
        continue

emailSelector = "//input[@id='username']"
passwordSelector = "//input[@id='password']"
loginButtonSelector = "//div[@class='actions']/button[@class='btn btn-primary btn-lg btn-block']"

searchSelector = "//form[@id='search-form']/input[@id='search-textbox']"
searchButtonSelector = "//form[@id='search-form']/button"
humanSelector = "//label[.='insanlık testi']"

loginInCheckSelector = "//nav[@id='top-navigation']//li[contains(@class, 'messages')]"
main_titles_selector = "//ul[@id='quick-index-nav']//a[not(contains(@class, 'not-index')) and not " \
                       "(contains(@href, 'kenar')) and not(contains(@class, 'dropdown-toggle'))]"

topic_titles_selector = "//div[@id='index-section']//ul[@class='topic-list partial']//li/a"
topic_titles_selector_right = "//div[@id='topic']//h1/a"

site_footer_selector = "//footer[@id='site-footer']"

global_wait_timeout = 10
long_wait_timeout = 20
short_wait_timeout = 3


def human_like_mouse_move(action, start_element):
    points = [[6, 2], [3, 2], [0, 0], [0, 2]]
    points = np.array(points)
    x = points[:, 0]
    y = points[:, 1]

    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points) - 1, 100)

    x_tup = si.splrep(t, x, k=1)
    y_tup = si.splrep(t, y, k=1)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = si.splev(ipl_t, x_list)
    y_i = si.splev(ipl_t, y_list)

    startElement = start_element

    action.move_to_element(startElement)
    action.perform()

    c = 5  # change it for more move
    i = 0
    for mouse_x, mouse_y in zip(x_i, y_i):
        action.move_by_offset(mouse_x, mouse_y)
        action.perform()
        print("Move mouse to, %s ,%s" % (mouse_x, mouse_y))
        i += 1
        if i == c:
            break


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
action = ActionChains(driver)


def send_keys(selector, text):
    key_el = driver.find_element(By.XPATH, selector)
    key_el.send_keys(text)
    time.sleep(0.6)


def click(selector):
    click_el = driver.find_element(By.XPATH, selector)
    click_el.click()
    time.sleep(0.6)


def switch_window_by_number(num):
    w = driver.window_handles[num]
    driver.switch_to.window(w)


def random_get_main_titles(selector):
    elements = driver.find_elements(By.XPATH, selector)
    choice_element = random.choice(elements)

    el_url = str(choice_element.get_attribute("href"))
    try:
        print(f"Random Selected Main Title : From Navbar : {el_url}")
        driver.get(el_url)
        time.sleep(3)
    except:
        print("Ignored Exception")
    pass


def random_get_topic_titles(left_list_selector, right_list_selector):
    elements = None
    try:
        elements = driver.find_elements(By.XPATH, left_list_selector)
        choice_element_l = random.choice(elements)
        el_url_l = str(choice_element_l.get_attribute("href"))

        try:
            print(f"Random Selected Topic Title : From Left List: {el_url_l}")
            driver.get(el_url_l)
            time.sleep(3)

        except:
            print(f"Ignored Exception")

    except NoSuchElementException as e:
        print(f"Ignored Exception -> {random_get_topic_titles.__name__} -> {e}")

    finally:

        if not elements:

            elements_backup = driver.find_elements(By.XPATH, right_list_selector)
            choice_element_r = random.choice(elements_backup)
            el_url_r = str(choice_element_r.get_attribute("href"))

            try:
                print(
                    f"Left List Not Found, Trying Right :: \n  Random Selected Topic Title : From Right List: {el_url_r}")
                driver.get(el_url_r)
                time.sleep(3)

            except:
                print(f"Ignored Exception")


def insert_entry():
    print("lol")


def check_element_exists(selector, timeout=global_wait_timeout):
    element = False
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, selector)))

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Ignored Exception -> {check_element_exists.__name__} -> {e}")

    return element


email = pyautogui.prompt(text='Lütfen ekşi sözlük E-Posta adresinizi giriniz: ', title='Ekşi Sözlük - EPosta',
                         default='')
try:
    if email:

        password = pyautogui.password(text='Lütfen ekşi sözlük şifrenizi giriniz: ', title='Ekşi Sözlük - Şifre',
                                      default='',
                                      mask='*')
        if password:
            login_url = "https://eksisozluk.com/giris"

            # Set Web Driver and Navigate to URL 9Zvt7yZicqv4.u8
            driver.get(login_url)
            x = driver.find_element(By.XPATH, passwordSelector)
            human_like_mouse_move(action,x)
            time.sleep(1)
            send_keys(emailSelector, email)
            send_keys(passwordSelector, password)

            if not headless:
                human_el = check_element_exists(humanSelector, short_wait_timeout)

                if human_el:
                    alert = pyautogui.alert(
                        text="İnsanlık Testi Tespit Edildi. Testi bir insanın yapması gerekli lütfen tamam tuşuna "
                             "bastıktan sonra 30 saniye içinde insanlık testini doğrulayınız.",

                        title="İnsanlık Testi", button="Tamam")

                    time.sleep(20)

            if headless:
                human_el = check_element_exists(humanSelector, short_wait_timeout)

                if human_el:
                    alert = pyautogui.alert(
                        text="İnsanlık Testi Tespit Edildi. Headless False yapıp tekrar çalıştırınız.",
                        title="İnsanlık Testi", button="Tamam")
                    driver.quit()

            click(loginButtonSelector)

            login_check = check_element_exists(loginInCheckSelector, global_wait_timeout)
            if not login_check:
                alert = pyautogui.alert(
                    text="Giriş başarısız, otomasyon girişin başarıyla yapıldığını doğrulayamadı."
                         " E-Posta ve Şifreniz yanlış olabilir, Lütfen tekrar deneyiniz.",
                    title="Giriş Başarısız", button="Tamam")
            else:
                random_get_main_titles(main_titles_selector)
                time.sleep(1)
                random_get_topic_titles(topic_titles_selector, topic_titles_selector_right)
        else:
            driver.quit()
    else:
        driver.quit()
finally:
    driver.quit()
