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
from webdriver_manager.chrome import ChromeDriverManager
from fake_headers import Headers
from proxy_randomizer import RegisteredProviders
import pyautogui

options = Options()
header = Headers(
    # generate any browser & os headeers
    headers=False  # don`t generate misc headers
)

rp = RegisteredProviders()
rp.parse_providers()
headers = header.generate()

def get_proxies():
    url='https://free-proxy-list.net/'

    r=requests.get(url,headers=headers)
    page = BeautifulSoup(r.text, 'html.parser')

    proxies=[]

    for proxy in page.find_all('tr'):
        i=ip=port=0

    for data in proxy.find_all('td'):
        if i==0:
            ip=data.get_text()
        if i==1:
            port=data.get_text()
        i+=1

    if ip!=0 and port!=0:
        proxies+=[{'http':'http://'+ip+':'+port}]

    return proxies

print(get_proxies())