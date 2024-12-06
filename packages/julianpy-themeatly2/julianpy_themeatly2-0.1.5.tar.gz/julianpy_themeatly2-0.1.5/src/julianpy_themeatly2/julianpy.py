# JulianPy v1.0
# By Themeatly2 + Harsizcool
# You will need to install these packages if pip or other package managers didn't already: selenium, pyautogui
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui
import time
# import threading
# -- Commented-out threading becuase it isn't needed yet. --
import os
import platform

class Astronaut():
    def __init__(self, game):
        self.driver = webdriver.Chrome()
        self.driver.get("https://s.julianseditor.com/" + game)
        self.driver.maximize_window()
        print("Loaded game URL! Launching in 5 seconds..")
        time.sleep(7)
        # Get the screen size
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        # Move to the center of the screen and click
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()
        time.sleep(6)
        pyautogui.moveTo(1240-50, 480)
        pyautogui.click()
        print("Ready!")
    
    def die(self):
        pyautogui.moveTo(1250, 200-20)
        pyautogui.click()
        pyautogui.moveTo(1017,721)
        pyautogui.click()
        self.driver.quit()

    def clickAt(self, target_x, target_y):
        pyautogui.moveTo(target_x, target_y)
        pyautogui.click()

    def holdKey(self, key=" ", holdtime=0):
        actions = ActionChains(self.driver)
        actions.key_down(key).perform()
        time.sleep(holdtime)
        actions.key_up(key).perform()

    def sendMessage(self, message):
        actions = ActionChains(self.driver)
        actions.key_down(Keys.ENTER).perform()
        time.sleep(0.1)
        actions.key_up(Keys.ENTER).perform()
        actions.send_keys(message).perform()
        actions.key_down(Keys.ENTER).perform()
        time.sleep(0.1)
        actions.key_up(Keys.ENTER).perform()
    
def version():
    return "JulianPy v0.1"

def hasWifi():
    os_system = platform.system()

    try:
        if os_system == "Linux":
            output = os.popen("nmcli -t -f active,ssid dev wifi").read().strip()
            if not output:
                return False

            for line in output.split("\n"):
                active, ssid = line.split(":")
                if active == "yes":
                    return True
            
            return False

        elif os_system == "Windows":
            output = os.popen("netsh wlan show interfaces").read()
            if "SSID" in output:
                for line in output.splitlines():
                    if "SSID" in line and "BSSID" not in line:
                        return True
            
            return False

        elif os_system == "Darwin":  # macOS
            output = os.popen(
                "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I"
            ).read()
            if "SSID" in output:
                for line in output.splitlines():
                    if "SSID" in line and not line.startswith(" BSSID"):
                        return True
            
            return False

        else:
            return False

    except Exception:
        return False