from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())

browser = webdriver.Chrome(service=service)

browser.get("https://orteil.dashnet.org/cookieclicker/")
browser.implicitly_wait(5)

big_cookie = browser.find_element(By.ID, "bigCookie")
cookie_counter = browser.find_element(By.ID, "cookies")
upgrades = [browser.find_element(By.ID, "productPrice" + str(i))
            for i in range(4, -1, -1)]

actions = ActionChains(browser)
actions.click(big_cookie)

for i in range(5000):
    actions.perform()
    count = int(cookie_counter.text.split(" ")[0])
    for upgrade in upgrades:
        cost = int(upgrade.text)
        if cost <= count:
            upgrade_actions = ActionChains(browser)
            upgrade_actions.move_to_element(upgrade)
            upgrade_actions.click()
            upgrade_actions.perform()
