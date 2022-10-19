from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from fake_headers import Headers


class Driver:

    def __init__(self):
        self.header = Headers(headers=False)

    def set(self, headless):


        headers = self.header.generate()
        coptions = webdriver.ChromeOptions()

        coptions.add_argument("--disable-blink-features")
        coptions.add_argument("--disable-blink-features=AutomationControlled")
        coptions.add_argument("ignore-certificate-errors")
        coptions.add_argument("--no-sandbox")
        coptions.add_argument("--disable-notifications")
        coptions.add_argument("--disable-infobars")
        coptions.add_argument("--disable-blink-features")
        coptions.add_argument("--disable-blink-features=AutomationControlled")
        coptions.add_argument("user-agent=" + str(headers['User-Agent']))

        if headless:
            coptions.add_argument("--headless")
            coptions.add_argument("--window-size=1600,900")
        else:
            coptions.add_extension("../get/ublock.crx")

        print("System : Fake User Agent : -> " + headers['User-Agent'])
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"  # complete

        chrome_driver = webdriver.Chrome(desired_capabilities=caps,
                                         service=Service(ChromeDriverManager().install()),

                                         options=coptions)
        chrome_driver.maximize_window()

        return chrome_driver
