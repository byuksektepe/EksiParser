import datetime
import os
import re
import sqlite3
import time
from sqlite3 import Error

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver.chrome_driver import Driver
from utils.navigate_methods import Navigate
from utils.key_methods import Key

from constants.selectors import *
from constants.system import *
from constants.messages import *

import pyautogui
import random

# -> SE442 # SE442 # SE442 # SE442 # SE442 ->

print(Messages.__WELCOME__)
time.sleep(0.6)
print(Messages.__WELCOME_WARNING__)

headless = Key().get_headless_from_user()  # C768 - MUST BE FIRST CALL(1)
c_random = Key().get_random_from_user()  # C768 - MUST BE SECOND CALL(2)

# Set Driver and Action
driver = Driver().set(headless)
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


def disable_before_unload():
    driver.execute_script("$(window).off('beforeunload');")


def random_get_main_titles(selector):
    elements = driver.find_elements(By.XPATH, selector)
    choice_element = random.choice(elements)

    el_url = str(choice_element.get_attribute("href"))
    try:
        print(f"{Messages.__SELECT_MAIN_TITLE__}{el_url}")
        driver.get(el_url)
        time.sleep(3)
    except:
        print("Ignored Exception")
    pass


def random_get_topic_titles(left_list_selector, right_list_selector):
    elements = None
    try:
        elements = driver.find_elements(By.XPATH, left_list_selector)

        try:
            choice_element_l = random.choice(elements)
            el_url_l = str(choice_element_l.get_attribute("href"))

            print(f"{Messages.__LEFT_SELECT_ENTRY_TITLE__}{el_url_l}")
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
                    f"{Messages.__RIGHT_SELECT_ENTRY_TITLE__}{el_url_r}")
                driver.get(el_url_r)
                time.sleep(3)

            except:
                print(f"Ignored Exception")
    pass


def scroll_to_bottom():
    x = driver.find_element(By.XPATH, Selectors.SITE_FOOTER_SELECTOR)
    action.move_to_element(x)
    pass


def accept_cookies():
    accept_policy = check_element_exists(Selectors.ACCEPT_COOKIES_SELECTOR, Global.__SHORT_WAIT_TIMEOUT__)
    if accept_policy:
        accept_policy.click()
    pass


def enter_entry(text):
    time.sleep(1)
    send_keys(Selectors.ENTRY_INPUT_SELECTOR, text)
    pass


def get_entry_title():
    x = None
    try:
        x = WebDriverWait(driver, Global.__DEFAULT_WAIT_TIMEOUT__) \
            .until(EC.presence_of_element_located((By.XPATH, Selectors.ENTRY_INPUT_SELECTOR)))
    except:
        pyautogui.alert(text=Messages.__ENTRY_FAIL__,
                        title=Messages.__ERROR_TITLE__,
                        button=Messages.__OK_BUTTON__,
                        timeout=Global.__DEFAULT_ERROR_TIMEOUT__)
        driver.quit()
        exit()
    finally:
        return x.get_attribute("placeholder")
    pass


def check_element_exists(selector, timeout=Global.__DEFAULT_WAIT_TIMEOUT__):
    element = False
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, selector)))

    except (NoSuchElementException, TimeoutException) as e:
        print(f"System Ignored Exception -> {check_element_exists.__name__} "
              f"-> NoSuchElementException or TimeoutException")

    return element


if c_random:

    driver.get(Global.__MAIN_URL__)
    time.sleep(1)
    random_get_main_titles(Selectors.MAIN_TITLES_SELECTOR)
    time.sleep(1)
    random_get_topic_titles(Selectors.TOPIC_TITLES_SELECTOR_LEFT, Selectors.TOPIC_TITLES_SELECTOR_RIGHT)

    driver.quit()
else:

    email = pyautogui.prompt(text=Messages.__EMAIL__,
                             title=Messages.__EMAIL_TITLE__,
                             default=Global.__DEFAULT_EMAIL__)
    try:
        if email:

            password = pyautogui.password(text=Messages.__PASSWORD__,
                                          title=Messages.__PASSWORD_TITLE__,
                                          default=Global.__DEFAULT_PASSWORD__,
                                          mask=Global.__DEFAULT_PASSWORD_MASK__)
            if password:
                pyautogui.alert(text='Kullanıcıdan veri alımı başarılı, lütfen bekleyin...',
                                title='Lütfen Bekleyin', button=Messages.__OK_BUTTON__, timeout=1000)

                # Set Web Driver and Navigate to URL
                driver.get(Global.__LOGIN_URL__)
                x = driver.find_element(By.XPATH, Selectors.PASSWORD_SELECTOR)

                # Robot Kontrolünü Kandırmak için insana benzer mouse haraketi
                Navigate().human_like_mouse_move(action, x)

                time.sleep(1)
                send_keys(Selectors.EMAIL_SELECTOR, email)
                send_keys(Selectors.PASSWORD_SELECTOR, password)

                if not headless:
                    human_el = check_element_exists(Selectors.ROBOT_TEST_SELECTOR, Global.__SHORT_WAIT_TIMEOUT__)

                    if human_el:
                        alert = pyautogui.alert(
                            text=Messages.__ROBOT_TEST__,
                            title=Messages.__ROBOT_TEST_TITLE__,
                            button=Messages.__OK_BUTTON__)

                        time.sleep(25)

                if headless:
                    human_el = check_element_exists(Selectors.ROBOT_TEST_SELECTOR, Global.__SHORT_WAIT_TIMEOUT__)

                    if human_el:
                        alert = pyautogui.alert(
                            text=Messages.__ROBOT_TEST_HEADLESS__,
                            title=Messages.__ROBOT_TEST_TITLE__,
                            button=Messages.__OK_BUTTON__)
                        driver.quit()
                        exit()

                click(Selectors.LOGIN_BUTTON_SELECTOR)

                login_check = check_element_exists(Selectors.LOGIN_CHECK_SELECTOR, Global.__DEFAULT_WAIT_TIMEOUT__)
                if not login_check:
                    alert = pyautogui.alert(
                        text=Messages.__LOGIN_FAIL__,
                        title=Messages.__LOGIN_FAIL_TITLE__, button=Messages.__OK_BUTTON__)
                else:

                    for entry in Global.__SAMPLE_ENTRY_LIST__:
                        random_get_main_titles(Selectors.MAIN_TITLES_SELECTOR)
                        time.sleep(1)
                        random_get_topic_titles(Selectors.TOPIC_TITLES_SELECTOR_LEFT,
                                                Selectors.TOPIC_TITLES_SELECTOR_RIGHT)
                        k = get_entry_title()

                        enter_entry(entry)
                        time.sleep(1)
                        accept_cookies()
                        time.sleep(1)
                        scroll_to_bottom()
                        print(f"Entry -> {entry},to inserted Topic Title -> {k}")

                        disable_before_unload()
            else:
                driver.quit()
        else:
            driver.quit()
    finally:
        driver.quit()
