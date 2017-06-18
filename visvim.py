#-*-coding:utf-8-*-
import  time, threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

class Visvim(threading.Thread):
    driver = None
    username = ""
    pwd = ""
    itemName = ""
    size = ""
    color = ""

    def __init__(self, username, pwd, itemName, color, size):
        super(Visvim, self).__init__()
        self.username = username
        self.pwd = pwd
        self.itemName = itemName
        self.color = color
        self.size = size

    def login(self,username, pwd):
        loginItem = self.driver.find_element(By.ID, "headerLoginInfo")
        if loginItem == None:
            return
        loginItem.click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "txt001")))
        usernameItem = self.driver.find_element(By.ID, "txt001")
        usernameItem.send_keys(username)
        pwdItem = self.driver.find_element(By.ID, "txt002")
        pwdItem.send_keys(pwd)
        xpathValue = "//input[@value='ログイン']"
        sbmItem = self.driver.find_element(By.XPATH, xpathValue)
        sbmItem.click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "purchaceHistoryTab")))

    def toMainWeb(self):
        headItem = self.driver.find_element(By.ID, "headerTitle")
        headItem.click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "news1")))

    def findItem(self,itemName):
        while True:
            try:
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "headerLocation")))
                newRelease = self.driver.find_element(By.CSS_SELECTOR, "div.selectItemBoxes.clearfix")
                findItems = newRelease.find_elements(By.PARTIAL_LINK_TEXT, itemName)
            except Exception:
                self.driver.refresh()
                continue
            # driver.execute_script("window.location.reload(true)")
            if len(findItems) != 0:
                return findItems[0]
            time.sleep(0.1)
            self.driver.refresh()

    def buyItem(self, item, color, size):
        item.click()
        while True:
            try:
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "detailText")))
                break
            except Exception:
                self.driver.refresh()
                continue
        colorSelect = Select(self.driver.find_element(By.ID, "sel001"))
        colorSelect.select_by_visible_text(color)
        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.ID, "sel002")))
        sizeSelect = Select(self.driver.find_element(By.ID, "sel002"))
        sizeSelect.select_by_visible_text(size)
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.ID, "btn001")))
        self.driver.find_element(By.ID, "btn001").click()
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//a[@onclick='checkout()']")))
        checkoutBtn = self.driver.find_element(By.XPATH, "//a[@onclick='checkout()']")
        checkoutBtn.click()
        while True:
            try:
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, "//input[@value='注文手続']")))
                break
            except Exception:
                self.driver.refresh()
                continue
        checkoutBtn = self.driver.find_element(By.XPATH, "//input[@value='注文手続']")
        checkoutBtn.click()
        while True:
            try:
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "sel201_1")))
                break
            except Exception:
                self.driver.refresh()
                continue
        self.driver.find_element(By.ID, "sel201_1").click()
        self.driver.find_element(By.ID, "continue_yes").click()
        while True:
            try:
                WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='続ける']")))
                break
            except Exception:
                self.driver.refresh()
                continue
        self.driver.find_element(By.XPATH, "//input[@value='続ける']").click()
        while True:
            try:
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, "//input[@value='注文']")))
                break
            except Exception:
                self.driver.refresh()
                continue
        self.driver.find_element(By.XPATH, "//input[@value='注文']").click()

    def run(self):
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chromeOptions.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(executable_path='libs/chromedriver',
                                  chrome_options=chromeOptions)  # Optional argument, if not specified will search path.
        self.driver.get('https://shop.visvim.tv')
        self.login(self.username, self.pwd)
        self.toMainWeb()
        item = self.findItem(self.itemName)
        self.buyItem(item, self.color, self.size)
        time.sleep(2)
        self.driver.quit()