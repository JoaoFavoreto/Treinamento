from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import string

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--start-maximized")

browser = webdriver.Chrome(options=options, service=service)


browser.get("https://orteil.dashnet.org/cookieclicker/")

time.sleep(10)

language = browser.find_element(By.ID, "langSelect-EN")
language.click()

time.sleep(10)

big_cookie = browser.find_element(By.ID, "bigCookie")
cookie_counter = browser.find_element(By.ID, "cookies")
upgrades = [browser.find_element(By.ID, "productPrice" + str(i))
            for i in range(4, -1, -1)]

while True:
    big_cookie.click()
    count = int(cookie_counter.text.split(" ")[0].replace(',', ''))
    for upgrade in upgrades:
        if upgrade.text != '':
            cost = int(upgrade.text.replace(',', ''))
            if cost <= count:
                upgrade_actions = ActionChains(browser)
                upgrade_actions.move_to_element(upgrade)
                upgrade_actions.click()
                upgrade_actions.perform()
