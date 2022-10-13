import datetime
import os
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
from webdriver_manager.chrome import ChromeDriverManager

options = Options()

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

left_results_locator = "//nav[@id='partial-index']//ul[contains(@class, 'topic-list')]//li"
content_results_locator = "//div[@id='content']//ul[contains(@class, 'topic-list')]//li"

search_button_locator = "//form[@id='search-form']/button[1]"
search_input_locator = "search-textbox"
toggle_button_locator = "//div[@id='top-bar']//a[@id='a3-toggle']"
results_button_locator = "//a[.='sonuçlar']"
accept_policy_locator = "//button[@id='onetrust-accept-btn-handler']"
topic_title_locator = "//div[@id='topic']//h1"


def set_driver():
    coptions = webdriver.ChromeOptions()
    coptions.add_argument("ignore-certificate-errors")
    coptions.add_argument("--no-sandbox")
    coptions.add_argument("disable-notifications")
    coptions.add_argument("--disable-infobars")
    coptions.add_argument("--disable-blink-features")
    coptions.add_argument("--disable-blink-features=AutomationControlled")
    coptions.add_extension("ublock.crx")

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  # complete

    chrome_driver = webdriver.Chrome(desired_capabilities=caps,
                                     service=Service(ChromeDriverManager().install()),

                                     options=coptions)
    chrome_driver.maximize_window()
    return chrome_driver


def get_topic_title():
    topic_title = driver.find_element(By.XPATH, topic_title_locator)
    return str(topic_title.text)


def switch_parent_window(driver):
    parent = driver.window_handles[0]
    driver.switch_to.window(parent)
def close_child_window(driver):
    child = driver.window_handles[1]
    driver.switch_to.window(child)


baslik = input("EkşiParser: Hangi başlığı aramak istiyorsunuz?\n")


columns = [
    "id",
    'baslik',
    'Icerik',
    'Yazar',
    'Tarih',
    'Konu',
    'Entry ID',
    'Entry URL'
]
rows = [columns]

url = "https://eksisozluk.com/basliklar/ara?SearchForm.Keywords=" + baslik + "&SearchForm.Author=&SearchForm.When.From=&SearchForm.When.To=&SearchForm.NiceOnly=false&SearchForm.SortOrder=Date"
# Set Web Driver and Navigate to URL
driver = set_driver()
driver.get(url)

time.sleep(2)

# Set Actions for element movement
actions = ActionChains(driver)
time.sleep(2)

accept_policy = driver.find_element(By.XPATH, accept_policy_locator)
accept_policy.click()

static_main_url = driver.current_url

content_results = driver.find_elements(By.XPATH, content_results_locator)
res_len = int(len(content_results))

# !! limitation Range, use "4" in test env. In release env. use "res_len" variable. !!
for i in range(1, 2):

    current_element_locator = "//div[@id='content']//ul[contains(@class, 'topic-list')]//li[" + str(i) + "]"
    current_element = driver.find_element(By.XPATH, current_element_locator)
    actions.move_to_element(current_element).perform()
    current_element.click()
    time.sleep(6)

    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    current_url = driver.current_url

    set_topic_title = get_topic_title()

    try:
        page_count = len(
            soup.find("div", {"class": "clearfix sub-title-container"}).find("div", {"class": "pager"}).find_all(
                "option"))
    except:
        page_count = 1
    # Check every page
    for j in range(1, page_count + 1):
        print("All Pages: " + str(page_count) + " Current Page: " + str(j))
        response = requests.get(current_url + "?p=" + str(j), headers=headers)

        time.sleep(2)

        soup = BeautifulSoup(response.content, "html.parser")
        entry_divs = soup.find_all("div", {"class": "content"})

        # Check every entrys
        for entry in entry_divs:
            footer = entry.findNext("footer")

            data_id = str(entry.findParent("li").attrs["data-id"])
            entry_id = "#" + data_id
            entry_url = "https://eksisozluk.com/entry/" + data_id

            author = footer.find_all("a")[0].text
            date = footer.find_all("a")[1].text

            # DATA AREA -->
            rows.append((

                baslik,
                entry.text,
                author,
                date,
                set_topic_title,
                entry_id,
                entry_url
            ))
            # <-- DATA AREA

    try:
        driver.get(static_main_url)

    except InvalidArgumentException:
        print(static_main_url)

    time.sleep(3)

df = pd.DataFrame(rows)
now_time = datetime.datetime.now()


# Write to xlsx file
# writer_b = pd.ExcelWriter('Rapor-' + str(baslik) + '-' + str(now_time.date()) + '.xlsx', engine='xlsxwriter')
# df.to_excel(writer_b,
#             sheet_name=str(now_time.date()),
#             index=False)
#
# # Save to file
# writer_b.save()

# INSERT DATA IN DATABASE
# Create a connection object

# db area -->
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        if os.path.exists(db_file):
            conn = sqlite3.connect(db_file)
        else:
            print("Database file not found!")
            # create_database(db_file)
            conn = sqlite3.connect(db_file)

    except Error as e:
        print(e)

    return conn


try:
    conn = sqlite3.connect('eksi_databasee.db')
    print("Database connection is successful!")

    c = conn.cursor()

    # verileri tabloya ekle

    c.execute(
        "CREATE TABLE IF NOT EXISTS eksi_table (id INTEGER PRIMARY KEY AUTOINCREMENT, baslik TEXT, icerik TEXT, yazar TEXT, tarih TEXT, konu TEXT, entry_id TEXT, entry_url TEXT)")
    print("Table created successfully!")
    conn.commit()


    # verileri tabloya ekle
    for i in range(1, len(rows)):
        c.execute("INSERT INTO " + "eksi_table" + " VALUES (null,?,?,?,?,?,?,?)", rows[i])

        print((baslik).replace(" ", "_") + " tablosuna veri eklendi.")
        conn.commit()
        print(rows[i], "eklendi.")

    conn.close()

except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)

finally:
    if (conn):
        conn.close()
        print("The SQLite connection is closed")

# <-- db area

# Close the connection
conn.close()

driver.quit()
