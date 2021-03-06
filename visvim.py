#-*-coding:utf-8-*-
import  time, threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display
import platform
import waiter
from selenium.common.exceptions import TimeoutException

chromeDriverPath_mac = "libs/chromedriver-mac"
chromeDriverPath_linux = "libs/chromedriver-linux"
chromeDriverPath_win = "libs/chromedriver.exe"
MAIN_URL = "https://shop.visvim.tv"


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

    def login(self):
        print self.username
        loginItem = self.driver.find_element(By.ID, "headerLoginInfo")
        if loginItem == None:
            return
        loginItem.click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "txt001")))
        usernameItem = self.driver.find_element(By.ID, "txt001")
        usernameItem.send_keys(self.username)
        pwdItem = self.driver.find_element(By.ID, "txt002")
        pwdItem.send_keys(self.pwd)
        xpathValue = "//input[@value='ログイン']"
        sbmItem = self.driver.find_element(By.XPATH, xpathValue)
        sbmItem.click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "purchaceHistoryTab")))
        print "login success!"

    def toMainWeb(self):
        headItem = self.driver.find_element(By.ID, "headerTitle")
        headItem.click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "news1")))
        print "toMainWeb"

    def gotoItemPage(self):
        while True:
            try:
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "headerLocation")))
                newRelease = self.driver.find_element(By.CSS_SELECTOR, "div.selectItemBoxes.clearfix")
                findItems = newRelease.find_elements(By.PARTIAL_LINK_TEXT, self.itemName)
            except Exception:
                self.driver.refresh()
                continue
            # driver.execute_script("window.location.reload(true)")
            if len(findItems) != 0:
                item = findItems[0]
                break
            time.sleep(0.1)
            self.driver.refresh()
        print "find item!"
        item.click()
        print "goto item page!"
        while True:
            try:
                WebDriverWait(self.driver, 2, 0.1).until(EC.presence_of_element_located((By.ID, "detailText")))
                break
            except Exception:
                self.driver.refresh()
                continue

    def chooseItem(self):
        while True:
            try:
                colorElement = WebDriverWait(self.driver, 1, 0.1).until(waiter.find_expected_option((By.ID, "sel001"), self.color))
                colorSelect = Select(colorElement)
                colorSelect.select_by_visible_text(self.color)
                sizeElement = WebDriverWait(self.driver, 1, 0.1).until(waiter.find_expected_option((By.ID, "sel002"), self.size))
                sizeSelect = Select(sizeElement)
                sizeSelect.select_by_visible_text(self.size)
                print "color, size select OK!"
                break
            except TimeoutException:
                self.toMainWeb()
                self.gotoItemPage()

    def chooseMultiItem(self):
        colorElement = WebDriverWait(self.driver, 1, 0.1).until(
            waiter.options_more_than_one((By.ID, "sel001")))
        colorSelect = Select(colorElement)
        colorSelectLen = len(colorSelect.options)
        for i in range(1, colorSelectLen):
            colorSelect.select_by_index(i)
            sizeElement = WebDriverWait(self.driver, 1, 0.3).until(
                waiter.options_more_than_one((By.ID, "sel002")))
            sizeSelect = Select(sizeElement)
            sizeSelectLen = len(sizeSelect.options)
            for j in range(1, sizeSelectLen):
                sizeSelect.select_by_index(j)
                time.sleep(0.5)
                if self.driver.find_element(By.ID, "btn001").is_enabled():
                    return
        print "color, size select OK!"

    def buyItem(self):
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.ID, "btn001")))
        self.driver.find_element(By.ID, "btn001").click()
        checkoutBtn = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//a[@onclick='checkout()']")))
        checkoutBtn.click()
        print "goto checkout!"
        while True:
            try:
                checkoutBtn = WebDriverWait(self.driver, 2, 0.1).until(EC.presence_of_element_located((By.XPATH, "//input[@value='注文手続']")))
                break
            except Exception:
                self.driver.refresh()
                continue
        checkoutBtn.click()
        print "goto payment page"
        while True:
            try:
                payMethodItem =  WebDriverWait(self.driver, 3, 0.1).until(EC.visibility_of_element_located((By.ID, "sel201_21")))
                break
            except Exception:
                self.driver.refresh()
                continue
        payMethodItem.click()
        self.driver.find_element(By.ID, "continue_yes").click()
        continueBtn = WebDriverWait(self.driver, 3, 0.1).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='続ける']")))
        continueBtn.click()
        while True:
            try:
                finalbtn = WebDriverWait(self.driver, 2, 0.1).until(EC.presence_of_element_located((By.XPATH, "//input[@value='注文']")))
                break
            except Exception:
                self.driver.refresh()
                continue
        finalbtn.click()
        # self.driver.find_element(By.XPATH, "//input[@value='注文']").click()
        print("sucess!")

    def buyOneItem(self):
        self.driver.get(MAIN_URL)
        self.login()
        self.toMainWeb()
        self.gotoItemPage()
        self.chooseItem()
        self.buyItem()
        self.driver.quit()

    def buyMultiItem(self):
        self.driver.get(MAIN_URL)
        self.login()
        errorTime = 0
        while True:
            try:
                self.toMainWeb()
                self.gotoItemPage()
                self.chooseMultiItem()
                self.buyItem()
            except Exception:
                errorTime += 1
                if errorTime < 5:
                    continue
                else:
                    break
        self.driver.quit()


    def run(self):
        display = Display(visible=0, size=(1024, 768))
        display.start()
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("headless")
        prefs = {"profile.managed_default_content_settings.images": 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        sysstr = platform.system()
        if (sysstr == "Windows"):
            chromePath = chromeDriverPath_win
        elif (sysstr == "Linux"):
            chromePath = chromeDriverPath_linux
        else:
            chromePath = chromeDriverPath_mac

        self.driver = webdriver.Chrome(executable_path=chromePath,
                                  chrome_options=chromeOptions)  # Optional argument, if not specified will search path.
        if self.color == "*":
            self.buyMultiItem()
        else:
            self.buyOneItem()
        display.stop()
