import time

import pyautogui
from constants.messages import *
from constants.system import *


class Key:

    def __init__(self):
        self.headless = False
        self.c_random = False

    def get_headless_from_user(self):
        while 1:

            headless_option = (pyautogui.confirm(text='-> Otomasyon çalışırken tarayıcıyı görmek ister misiniz?',
                                                 title='Tarayıcı Seçeneği',
                                                 buttons=["Hayır", "Evet", "Çık"])).lower()
            print(headless_option)
            if headless_option == "evet":
                self.headless = False
                break

            elif headless_option == "hayır":
                self.headless = True
                break

            elif headless_option == "çık":
                exit()
                break
            else:
                continue
        return self.headless

    def get_random_from_user(self):
        while 1:

            random_option = (
                pyautogui.confirm(text='-> Giriş yapmadan sadece rastgele entry bağlantısı almak ister misiniz?',
                                  title='Entry Seçeneği',
                                  buttons=["Hayır", "Evet", "Çık"])).lower()

            if random_option == "evet":
                self.c_random = True
                break

            elif random_option == "hayır":
                self.c_random = False
                break
            elif random_option == "çık":
                exit()
                break
            else:
                continue
        pyautogui.alert(text='Kullanıcıdan veri alımı başarılı, lütfen bekleyin...',
                        title='Lütfen Bekleyin', button=Messages.__OK_BUTTON__, timeout=2000)
        return self.c_random
