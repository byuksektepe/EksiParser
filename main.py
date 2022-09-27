import datetime
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import InvalidArgumentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

options = Options()

headers = { 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36" }

left_results_locator = "//nav[@id='partial-index']//ul[contains(@class, 'topic-list')]//li"
content_results_locator = "//div[@id='content']//ul[contains(@class, 'topic-list')]//li"

search_button_locator = "//form[@id='search-form']/button[1]"
search_input_locator = "search-textbox"
toggle_button_locator = "//div[@id='top-bar']//a[@id='a3-toggle']"
results_button_locator = "//a[.='sonuçlar']"
accept_policy_locator = "//button[@id='onetrust-accept-btn-handler']"

def chrom_set():
    coptions = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  # complete

    chrome_driver = webdriver.Chrome(desired_capabilities=caps,service=Service(ChromeDriverManager().install()), options=coptions)
    chrome_driver.maximize_window()
    return chrome_driver


baslik = input("EkşiParser: Hangi başlığı aramak istiyorsunuz?\n")

columns = [
    'Icerik',
    'Yazar',
    'Tarih',
    'Konu',
]
rows = [columns]

url = "https://eksisozluk.com/basliklar/ara?SearchForm.Keywords="+baslik+"&SearchForm.Author=&SearchForm.When.From=&SearchForm.When.To=&SearchForm.NiceOnly=false&SearchForm.SortOrder=Date"
# Set Web Driver and Navigate to URL
driver = chrom_set()
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

for i in range(1, 3):

    current_element_locator = "//div[@id='content']//ul[contains(@class, 'topic-list')]//li[" + str(i) + "]"
    current_element = driver.find_element(By.XPATH, current_element_locator)
    actions.move_to_element(current_element).perform()
    current_element.click()
    time.sleep(4)

    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    current_url = driver.current_url

    try:
        page_count = len(
            soup.find("div", {"class": "clearfix sub-title-container"}).find("div", {"class": "pager"}).find_all(
                "option"))
    except:
        page_count = 1

    for j in range(1, page_count + 1):
        print("OK - Lütfen Bekleyin...")
        response = requests.get(current_url + "?p=" + str(j), headers=headers)

        time.sleep(2)

        soup = BeautifulSoup(response.content, "html.parser")
        entry_divs = soup.find_all("div", {"class": "content"})

        for entry in entry_divs:
            footer = entry.findNext("footer")
            author = footer.find_all("a")[0].text
            date = footer.find_all("a")[1].text
            rows.append((
                entry.text,
                author,
                date,
                baslik,
            ))
    try:
        driver.get(static_main_url)
    except InvalidArgumentException:
        print(static_main_url)
    time.sleep(3)


df = pd.DataFrame(rows)
now_time = datetime.datetime.now()
writer_b = pd.ExcelWriter('rapor-' + str(baslik) + '-' + str(now_time.date()) + '.xlsx', engine='xlsxwriter')
df.to_excel(writer_b, sheet_name=str(now_time.date()), index=False)
writer_b.save()
driver.close()
