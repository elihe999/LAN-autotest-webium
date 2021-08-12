# -*- coding: utf-8 -*-
import json
import os
import re
import sys
import time
import traceback
from collections import deque
# import win32gui, win32con
# import pyautogui as pg

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from PySide2.QtCore import QByteArray, QFile, QIODevice, QObject, QTextStream, QThread, QTimer, Signal, Slot
from PySide2.QtWidgets import QAction, QApplication, QCheckBox, QLabel, \
                               QLineEdit, QMenu, QPushButton, QRadioButton, \
                               QSpinBox, QTextEdit, QWidget
from scapy.all import *
from selenium import webdriver
from selenium.common import exceptions
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
import tracemalloc

configfile = "config.ini"

class SpiderThread():
    def __init__(self):
        self.ip = ""
        self.username = ""
        self.web_passwd = ""
        self.mac = ""
        self.version = ""
        self.factorPasswd = "admin"
        # message list
        self.messageList = deque()
        self.status = [False,0,0,'ip','mac']
        # setup service
        self.chromedriver_path = r"chromedriver.exe"
        c_service = Service(self.chromedriver_path)
        c_service.command_line_args()
        c_service.start()
        self.webServer = c_service
        self.driver = None
        self.browser_path = ""
        # for each model
        self.product_model = ""
        # flow control
        self.currentloop = 0
        self.totalloop = 0
        self.sleepTime = 0
        self.ready = False
        self.actionType = ""
        self.coredumpStop = True
        self.headlessFlag = False
        # function type
        self.provType = "HTTP"
        self.taskList = ("reboot", "provision", "reset")
        self.modelList = ("GRP260X", "GXP21XX")
        self.provList = {}
        self.versionCount = 0
        self.prov_dir = ""
        self.ssl_config = False
        self.firmware_bin = "grp2600fw.bin"
        # 
        self.service_args = []
        self.chrome_options = None
        self.clean_cache = False
        self.pcap_name = ""

        self.model = None

    def setup_chrome(self):
        time.sleep(1)
        global configfile
        self.service_args.append('--load-images=no')
        self.service_args.append('--disk-cache=yes')
        self.service_args.append('--ignore-ssl-errors=true')
        # webdriver option
        self.chrome_options = Options()
        if os.path.exists(os.path.abspath(configfile) ):
            f = open(os.path.abspath(configfile) , "r")
            line = f.readline()
            while line:
                option = line.split("=")
                print(line)
                if option[0] == "initpasswd":
                    if option[1].strip('"') != "":
                        password = option[1].strip()
                        self.factorPasswd = password.strip('"')
                        if self.factorPasswd == "":
                            self.factorPasswd = "admin"
                    pass
                line = f.readline()
            f.close()

        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        if self.headlessFlag:
            self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--disable-plugins')
        if self.browser_path != "":
            self.chrome_options.binary_location = self.browser_path

        if self.driver != None:
            try:
                self.__del__()
            except BaseException as e:
                print("setup err: " + repr(e))
                self.debuglog(traceback.format_exc())
                pass
        try:
            self.driver = webdriver.Chrome(chrome_options=self.chrome_options, service_args=self.service_args,
                                            executable_path=self.chromedriver_path)
        except BaseException as e:
            print("setup err: " + repr(e))
            self.debuglog(traceback.format_exc())
            self.quit()
        # time wait
        self.longwait = WebDriverWait(self.driver, 60)
        self.middlewait = WebDriverWait(self.driver, 40)
        self.shortwait = WebDriverWait(self.driver, 25)
        self.wait = WebDriverWait(self.driver, 8)
        self.ready = True

    """
    networking function
    """
    def search_lan_mac(self):
        conf.route.resync()
        conf.route.route('0.0.0.0')[0]
        # show_interfaces()
        addr = ""
        iface = get_working_if()
        if self.pcap_name != "" and self.pcap_name != "Default":
            iface = self.pcap_name
        addr = self.ip.split('.')
       
        lan = addr[0] + "." + addr[1] + "." + addr[2] + ".0/24"
        print(lan)
        ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=lan), iface=iface, timeout=5, verbose=False)
        for snd, rcv in ans:
            cur_mac = rcv.sprintf("%Ether.src%")
            cur_ip  = rcv.sprintf("%ARP.psrc%")
            print(cur_ip)
            if cur_ip.strip() == self.ip.strip():
                self.debuglog("mac" + cur_mac)
                self.status[3] = cur_ip.strip()
                self.status[4] = cur_mac.strip()
                self.mac = cur_mac
                return True
        return False

    def search_ip(self):
        conf.route.resync()
        conf.route.route('0.0.0.0')[0]
        # show_interfaces()
        iface = get_working_if()
        addr = ""
        if self.pcap_name != "" and self.pcap_name != "Default":
            iface = self.pcap_name
        addr = self.ip.split('.')
        lan = addr[0] + "." + addr[1] + "." + addr[2] + ".0/24"
        print(lan)
        ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=lan), iface=iface, timeout=5, verbose=False)
        self.debuglog("Searching new ip")
        find_flag = False
        for snd, rcv in ans:
            cur_mac = rcv.sprintf("%Ether.src%")
            cur_ip  = rcv.sprintf("%ARP.psrc%")
            if cur_mac.strip() == self.mac.strip():
                find_flag = True
                if self.ip.strip() != cur_ip.strip():
                    self.ip = cur_ip.strip()
                    self.status[3] = cur_ip.strip()
                    self.debuglog( "New Ip: " + cur_ip )
                return 0
        if find_flag:
            return 0
        else:
            self.debuglog("Can not find device' ip", "error")
            return -1

    """
    support function
    """
    def move_n_click(self, elem):
        try:
            action = ActionChains(self.driver)
            action.move_to_element(elem).perform()
            self.my_waiting(1)
            try:
                elem.click()
            except BaseException as e:
                action.click()
        except BaseException as e:
            print("move_n_click: " + repr(e))
            print(traceback.format_exc())
            pass

    def findElement(self, by, value):
        if (by == "id"):
            element = self.driver.find_element_by_id(value)
            return element
        elif (by == "name"):
            element = self.driver.find_element_by_name(value)
            return element
        elif (by == "xpath"):
            element = self.driver.find_element_by_xpath(value)
            return element
        elif (by == "classname"):
            element = self.driver.find_element_by_class_name(value)
            return element
        elif (by == "css"):
            element = self.driver.find_element_by_css_selector(value)
            return element
        elif (by == "link_text"):
            element = self.driver.find_element_by_link_text(value)
            return element
        else:
            print("No function")
            return None

    def findElements(self, by, value):
        try:
            if (by == "xpath"):
                element = self.driver.find_elements_by_xpath(value)
                return element
            elif (by == "classname"):
                element = self.driver.find_elements_by_class_name(value)
                return element
            elif (by == "css"):
                element = self.driver.find_elements_by_css_selector(value)
                return element
            elif (by == "link_text"):
                element = self.driver.find_elements_by_link_text(value)
                return element
            elif (by == "tag"):
                element = self.driver.find_elements_by_tag_name(value)
                return element
            else:
                print("No function")
                return None
        except NoSuchElementException as e:
            return None

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def my_get_page(self, path=""):
        if self.ssl_config:
            self.driver.get('https://' + self.ip + path)
        else:
            self.driver.get('http://' + self.ip + path)

    def my_waiting(self, count):
        if count > 4:
            self.debuglog("waiting ：{}".format(str(count)))
        for i in range(count):
            time.sleep(1)
            if count > 4:
                self.status[2] = count - i
            if self.status[0] == False:
                self.status[2] = 0
                break
        self.status[2] = 0

    def my_requests(self, atype="get"):
        if self.ssl_config:
            if atype == "get":
                r = requests.get("https://" + self.ip, verify = False)
        else:
            if atype == "get":
                r = requests.get("http://" + self.ip, verify = False)
        return r

    """
    action function
    """
    def open_browser(self):
        try:
            self.driver.get( "http://" + self.ip )
        except BaseException as e:
            print(repr(e))
            print(traceback.format_exc())

        try:
            self.debuglog( "Opening browser" + self.ip )
            self.driver.get( "http://" + self.ip )
            self.driver.implicitly_wait(10)
            if self.product_model == "GRP260X":
                lang_btn = self.driver.find_element_by_xpath('//*[@id="localeSelect"]/span')
                if lang_btn.get_attribute('innerHTML') != "English":
                    self.move_n_click(lang_btn)
                    lang_list = self.driver.find_elements_by_xpath('//*[@id="localeSelect"]/div/div/div/ul/li')
                    for eachli in lang_list:
                        if eachli.get_attribute('innerHTML') == "English":
                            self.move_n_click(eachli)
                            break
            else:
                try:
                    self.wait.until(lambda browser: self.driver.find_elements_by_xpath('//div[@id="page-layout"]/div[@class="layoutContainer"]'))
                except:
                    self.shortwait.until(lambda browser: self.driver.find_elements_by_xpath('//*[@id="control-pad"]//div/select[@class="gwt-ListBox"]'))
                    lang_btn = self.driver.find_element_by_xpath('//*[@id="control-pad"]//div/select[@class="gwt-ListBox"]')
                    Select(lang_btn).select_by_visible_text('English')

        except BaseException as e:
            print( "get: s " + repr(e) )
            print(traceback.format_exc())
            return -1

        print(self.driver.current_url)
        if self.driver.current_url.find("http://") != -1:
            pass
        elif self.driver.current_url.find("https://") != -1:
            self.ssl_config = True
        r = requests.get("https://" + self.ip, verify = False)
        if r.status_code == 200:
            return 0
        return -1

    def login_phone(self, mode="Normal"):
        """
        -1 stop
        -2 fail
        """
        login_fail_count = 0

        self.driver.refresh()
        self.driver.implicitly_wait(5)
        self.debuglog( "Waiting for browser response" )
        if self.product_model == "GRP260X":
            self.debuglog( "Ant Design UI login" )
            for __retry in range(0,3):
                if self.status[0] == False:
                    return -1
                if __retry > 0:
                    self.search_ip()
                    print("loginrefresh")
                    self.driver.refresh()
                    self.debuglog("login failed, retry","error")
                    self.my_get_page("/")
                    self.driver.implicitly_wait(5)
                try:
                    self.shortwait.until(lambda browser: self.driver.find_elements_by_xpath("/html/body//section/form"))
                except BaseException as e:
                    try:
                        self.wait.until(lambda browser: self.driver.find_elements_by_xpath("//section[@class='ant-layout']"))
                        return 0
                    except BaseException as e:
                        if repr(e).find("TimeoutException") != -1:
                            self.debuglog( "Can not found form " + repr(e) )
                            login_fail_count += 1
                else:
                    for __loop in range(0,4):
                        if self.status[0] == False:
                            return -1
                        if __loop > 0:
                            self.driver.refresh()
                            self.driver.implicitly_wait(5)
                        try:
                            user_input = self.driver.find_element_by_id("username")
                            pass_input = self.driver.find_element_by_id("password")
                            login_antbtn = self.driver.find_elements_by_xpath('//button[@class="ant-btn login-submit"]')
                        except BaseException as e:
                            try:
                                self.wait.until( lambda browser: self.driver.find_elements_by_xpath("//section[@class='ant-layout']"))
                                return 0
                            except BaseException as t:
                                print("double:" + repr(t))
                                login_fail_count += 1
                        else:
                            if user_input.is_displayed() == False or pass_input.is_displayed() == False or login_antbtn[0].is_displayed() == False:
                                print("Item is not displayed")
                            else:
                                try:
                                    user_input.clear()
                                    pass_input.clear()
                                    self.my_waiting(2)
                                    user_input.send_keys(self.username)
                                    if mode == "reset" or __loop > 2:
                                        self.debuglog("Reset - " + str(self.factorPasswd))
                                        pass_input.send_keys(self.factorPasswd)
                                    else:
                                        pass_input.send_keys(self.web_passwd)
                                    try:
                                        for __ in range(1):
                                            for bttn in login_antbtn:
                                                bttn.click()
                                    except BaseException as e:
                                        print(repr(e))
                                        print(traceback.format_exc())
                                    self.my_waiting(3)
                                except BaseException as e:
                                    print( repr(e) )
                                    print(traceback.format_exc())
                                    continue

                                try:
                                    # searching warning tip
                                    self.wait.until( lambda browser: self.driver.find_elements_by_xpath('//div[@class="err-tips"]/span/span') )
                                except BaseException as e:
                                    self.my_waiting(2)
                                    try:
                                        self.wait.until( lambda browser: self.driver.find_elements_by_xpath('//input[@id="newAdmPwd"]') )
                                        input_new = self.findElement("xpath", '//input[@id="newAdmPwd"]')
                                        input_con = self.findElement("xpath", '//input[@id="newAdmPwdConfirm"]')
                                        input_new.send_keys(self.web_passwd)
                                        input_con.send_keys(self.web_passwd)
                                        self.findElement('xpath', '//button[@class="ant-btn login-submit"]').click()
                                    except BaseException as e:
                                        pass
                                    self.my_waiting(3)
                                    temp = "http://" + self.ip + "/login"
                                    temp1 = "https://" + self.ip + "/login"
                                    self.debuglog("login:" + self.driver.current_url)
                                    if self.driver.current_url == temp or self.driver.current_url == temp1:
                                        self.driver.refresh()
                                    else:
                                        return 0
                                else:
                                    span_list = self.driver.find_elements_by_xpath('//div[@class="err-tips"]/span/span')
                                    for span in span_list:
                                        content = span.get_attribute("innerHTML")
                                        if content.find("Invalid username/password combination entered!") != -1:
                                            continue
                                        elif content.find("Provision") != -1:
                                            self.my_waiting(25)
                                            continue
                                        elif content.find("Too many consecutive failed login attempts.") != -1:
                                            self.my_waiting(360)
                                            continue
            return -2
        elif self.product_model == "GXP21XX":
            self.debuglog( "Classic UI Style Login" )
            for __retry in range(0,3):
                locator = (By.ID, "login-box")
                if self.status[0] == False:
                    return -1
                self.search_ip()
                if __retry > 0:
                    self.driver.refresh()
                    print("loginrefresh")
                if __retry > 1:
                    self.my_get_page("/")
                    self.driver.implicitly_wait(3)
                try:
                    self.wait.until( EC.presence_of_element_located(locator) )
                except BaseException as e:
                    try:
                        self.driver.find_elements_by_id("topBanner")
                        self.driver.find_elements_by_id("main-container")
                        # self.wait.until( lambda browser: self.driver.find_elements_by_id("topBanner"))
                        # self.wait.until( lambda browser: self.driver.find_elements_by_id("main-container"))
                        return 0
                    except BaseException as e:
                        print( "wait pad" + repr(e) )
                        print(traceback.format_exc())
                        self.debuglog("Not login: " + repr(e))
                        login_fail_count += 1
                        continue
                else:
                    print("Find main body")
                    try:
                        try:
                            # login auto
                            if self.findElement("id", "logo-pad") != None and self.findElement("id", "mid-container") != None:
                                return 0
                        except BaseException as e:
                            pass

                        for __loginCount in range(0,5):
                            if self.status[0] == False:
                                return -1
                            try:
                                self.debuglog("login")
                                try:
                                    user_input = self.findElement("classname", "gwt-TextBox")
                                    pass_input = self.findElement("classname", "gwt-PasswordTextBox")
                                    login_button = self.findElement("classname", "gwt-Button")
                                    user_result = user_input.is_displayed()
                                    pass_result = pass_input.is_displayed()
                                    result = login_button.is_displayed()
                                    if result == False or pass_result == False or user_result == False:
                                        continue
                                    user_input.clear()
                                    pass_input.clear()
                                    user_input.send_keys(self.username)
                                    if mode != "reset" and __loginCount > 2:
                                        pass_input.send_keys(self.factorPasswd)
                                    elif mode == "reset":
                                        if __loginCount > 2:
                                            pass_input.send_keys(self.web_passwd)
                                            self.debuglog("Reset Failed", "error")
                                        else:
                                            pass_input.send_keys(self.factorPasswd)
                                    else:
                                        pass_input.send_keys(self.web_passwd)
                                except BaseException as e:
                                    self.my_get_page("/")
                                    self.driver.implicitly_wait(5)
                                    self.driver.refresh()
                                    self.debuglog("Enter passwd err:" + repr(e))
                                    print(traceback.format_exc())
                                    continue

                                self.my_waiting(1)
                                try:
                                    login_button.click()
                                    print("test click function")
                                    self.wait.until_not(lambda browser: self.driver.find_elements_by_xpath("//*[@class='left message']/p"))
                                except BaseException as e:
                                    print("Find popout")
                                    popout_alert = self.driver.find_element_by_xpath("//*[@class='left message']/p")
                                    warning_msg = popout_alert.get_attribute("innerHTML")
                                    print(warning_msg)
                                    if warning_msg.find("Provision") != -1:
                                        self.debuglog(warning_msg)
                                        self.my_waiting(50)
                                    elif warning_msg.find("Locked out for") != -1:
                                        self.my_waiting(299)
                                    else:
                                        self.debuglog(warning_msg)
                                        self.my_waiting(10)
                                    self.search_ip()
                                    self.driver.refresh()
                                    continue

                                try:
                                    if self.driver.get_current_url().find("status_account") != -1:
                                        login_fail_count = 0
                                except:
                                    pass

                                for _ in range(0,2):
                                    try:
                                        r = self.my_requests()
                                        if r.status_code != 200:
                                            print(r.status_code)
                                            self.my_waiting(5)
                                            self.search_ip()
                                            self.driver.refresh()
                                        else:
                                            try:
                                                self.shortwait.until_not(lambda browser: self.driver.find_elements_by_class_name("//*[@class='left message']/p"))
                                                break
                                            except BaseException as e:
                                                self.my_waiting(5)
                                                self.driver.refresh()
                                    except BaseException as e:
                                        self.my_waiting(4)
                                # click popout
                                try:
                                    popout_alert = self.driver.find_element_by_xpath("//*[@class='left message']/p")
                                    print("click pop out")
                                    if len(popout_alert) == 0:
                                        break
                                    print(popout_alert.get_attribute("textContent"))
                                    if popout_alert.get_attribute("textContent").find("Provision") != -1 or popout_alert.get_attribute("textContent").find("Upgrade") != -1:
                                        self.my_waiting(30)
                                        self.search_ip()
                                        self.driver.refresh()
                                        continue
                                    if len(popout_alert) > 0:
                                        visib_btn = self.driver.find_elements_by_xpath('//div[@class="popupContent"]//span[@class="closebtn"]')
                                        try:
                                            for btn in visib_btn:
                                                self.move_n_click(btn)
                                                self.my_waiting(1)
                                        except BaseException as e:
                                            pass
                                    else:
                                        break
                                except BaseException as e:
                                    pass
                            except BaseException as e:
                                print("loginfail"+repr(e))
                                if repr(e).find("NoSuchElementException") != -1:
                                    self.search_ip()
                                    self.driver.refresh()

                            print("Checking device reset status")
                            try:
                                self.my_waiting(3)
                                print(self.driver.current_url)
                                self.wait.until(lambda browser: self.driver.find_elements_by_class_name("popupContent"))
                                try:
                                    class_group = self.driver.find_elements_by_xpath("//div[@class='popupContent']")
                                    for xpath_ele in class_group:
                                        if xpath_ele.find_element_by_xpath('//div[@class="heading"]/div[@class="gwt-HTML"]').get_attribute('textContent') == "Admin Password":
                                            try:
                                                self.debuglog("Update password", "info")
                                                try:
                                                    i = 0
                                                    for item in self.driver.find_elements_by_class_name('gwt-PasswordTextBox'):
                                                        try:
                                                            if i == 0:
                                                                # item.send_keys(self.factorPasswd)
                                                                pass
                                                            else:
                                                                self.move_n_click(item)
                                                                item.send_keys(self.web_passwd)
                                                        except BaseException as e:
                                                            print("reset " + repr(e))
                                                            pass
                                                        finally:
                                                            i = i + 1
                                                except BaseException as e:
                                                    print("Update password" + repr(e))

                                                try:
                                                    button_list = self.driver.find_elements_by_class_name("gwt-Button")
                                                    for btn in button_list:
                                                        if btn.get_attribute("innerHTML") == "Save" and btn.is_displayed():
                                                            self.my_waiting(2)
                                                            self.move_n_click(btn)
                                                except BaseException as e:
                                                    print("Click save password" + repr(e))

                                                try:
                                                    WebDriverWait(self.driver, 6).until(lambda browser: self.driver.find_element_by_class_name("popupContent"))
                                                    button_list = self.driver.find_elements_by_class_name("closebtn")
                                                    self.my_waiting(1)
                                                    self.move_n_click(button_list[1])
                                                    self.debuglog("Password Update Successfully")
                                                    try:
                                                        self.wait.until(lambda browser: self.driver.find_elements_by_id("topBanner"))
                                                        return 0
                                                    except:
                                                        pass
                                                    break
                                                except BaseException as e:
                                                    print("Failed to click" + repr(e))
                                            except BaseException as e:
                                                print("reset2 " + repr(e))
                                                login_fail_count += 1
                                except BaseException as e:
                                    print("checking reset password" + repr(e))
                            except BaseException as e:
                                if repr(e).find("TimeoutException") != -1:
                                    print("Not reset password process")
                                    break
                    except BaseException as e:
                        print("failed" + repr(e))

            if login_fail_count >= 3:
                print("login phone fail3")
                return -2
            else:
                return 0

    # check core dump
    def check_coredump(self):
        """
        @returnValue: -1 elem -2 core dump
        """
        if self.product_model == "GRP260X":
            self.version = ""
            for __ in range(0,3):
                if self.status[0] == False:
                    return 0
                try:
                    self.choose_nav_tab("Status", "System Info")
                    self.driver.implicitly_wait(3)
                except BaseException as e:
                    print("debug1 check_coredump" + repr(e))
                    if __ > 0:
                        self.driver.refresh()
                else:
                    self.debuglog("Checking core dump")
                    try:
                        for __ in range(3):
                            self.driver.refresh()
                            self.driver.implicitly_wait(5)
                            empty_flag = False
                            subtitle_list = self.driver.find_elements_by_xpath(
                                        '//*[@class="bak-sub-title"]/preceding-sibling::div/div[1]/label/span')
                            subobject_list = self.driver.find_elements_by_xpath(
                                        '//*[@class="bak-sub-title"]/preceding-sibling::div/div[2]/div/span/div')
                            cur_list_len = len(subtitle_list)
                            for i in range(cur_list_len):
                                label_name = subtitle_list[i].get_attribute("innerHTML")
                                if label_name.find("Prog") != -1:
                                    v_str = subobject_list[i].get_attribute("innerHTML")
                                    if v_str == "":
                                        pass
                                    else:
                                        empty_flag = True
                                        print( v_str )
                                        self.version = str(v_str)
                                        self.debuglog(label_name + " " + v_str)
                                        print("Ver: " + v_str)
                                        break
                            if empty_flag:
                                break
                            else:
                                continue
                    except:
                        print(traceback.format_exc())

                    try:
                        try:
                            count_core = 0
                            core_file = self.findElements("xpath", '//div[@class="ant-col ant-form-item-control-wrapper"]/div/span/div/div[@class="ant-row"]/div[1]')
                            for name in core_file:
                                if name.get_attribute('innerHTML').find('core') != -1:
                                    self.debuglog(name.get_attribute('innerHTML'), "error")
                                    count_core + 1
                        except BaseException as e:
                            print( "err find core" + repr(e) )
                        finally:
                            if count_core > 0 and self.coredumpStop == True:
                                return -2
                            else:
                                return 0
                    except BaseException as e:
                        print( "check_coredump" + repr(e) )
                        print(traceback.format_exc())
                        return -1
        elif self.product_model == "GXP21XX":
            try:
                try:
                    class_group = self.driver.find_elements_by_xpath("//div[@class='popupContent']")
                    for xpath_ele in class_group:
                        if xpath_ele.find_element_by_xpath('//div[@class="heading"]/div[@class="gwt-HTML"]').get_attribute('textContent') == "Admin Password":
                            try:
                                self.debuglog("Update password")
                                i = 0
                                for item in self.driver.find_elements_by_class_name('gwt-PasswordTextBox'):
                                    try:
                                        if i == 0:
                                            item.send_keys(self.factorPasswd)
                                        else:
                                            item.send_keys(self.web_passwd)
                                    except BaseException as e:
                                        print(repr(e))
                                        print(traceback.format_exc())
                                        pass
                                    finally:
                                        i = i + 1

                                button_list = self.driver.find_elements_by_class_name("gwt-Button")
                                for btn in button_list:
                                    if btn.get_attribute("innerHTML") == "Save" and btn.is_displayed():
                                        btn.click()
                                try:
                                    self.my_waiting(1)
                                    WebDriverWait(self.driver, 6).until(lambda browser: self.driver.find_element_by_class_name("popupContent"))
                                    button_list = self.driver.find_elements_by_class_name("closebtn")
                                    button_list[1].click()
                                    self.debuglog("Password Update Successfully")
                                    self.my_waiting(1)
                                except BaseException as e:
                                    print("Failed to click" + repr(e))
                            except BaseException as e:
                                print(repr(e))
                                print(traceback.format_exc())
                except BaseException as e:
                    print(repr(e))
                    print(traceback.format_exc())
                    return -1
                self.wait.until_not(lambda browser: self.driver.find_elements_by_class_name("gwt-PopupPanelGlass"))
            except BaseException as e:
                print("Its ok " + repr(e))
                return -1
            else:
                if self.status[0] == False:
                    return 0
                try:
                    self.choose_nav_tab("Status", "System Info")
                    self.driver.implicitly_wait(5)
                    self.driver.find_elements_by_css_selector('[class="first"]')
                    try:
                        info_list = self.driver.find_elements_by_xpath('//div[@class="editable"]/div')
                        for item in info_list:
                            temp = item.find_element_by_xpath("div[@class='cell label']")
                            try:
                                context = item.find_element_by_xpath("div[@class='cell contents']/div")
                            except:
                                continue
                            label_name = temp.get_attribute('textContent')
                            print(temp.get_attribute('textContent'))
                            if label_name.find("System Up Time") != -1:
                                self.debuglog("Up time " + context.get_attribute('textContent'), "info")
                            elif label_name.find("Prog") != -1:
                                self.version = context.get_attribute('textContent')
                                self.debuglog("Prog " + context.get_attribute('textContent'))
                                break
                    except BaseException as e:
                        self.debuglog("Find Prog version error :" + repr(e), "error")

                    try:
                        ver_label = self.driver.find_elements_by_xpath('//*[@id="verNo"]/div')
                        if len(ver_label) == 1:
                            text = ver_label[0].get_attribute('innerHTML')
                            if text != "":
                                self.version = text.replace('Version ', '').strip()
                                self.debuglog("Update Version : " + str(self.version))
                    except BaseException as e:
                        self.debuglog("Update new version error :" + repr(e), "error")

                    try:
                        self.driver.refresh()
                        label_list = self.driver.find_elements_by_xpath("//*[@class='data-list']/tbody/tr/td/div/table/tbody/tr[@class='table-row']/td[1]//div[@class='gwt-HTML last']")
                        flag = 1
                        count_core = 0
                        for item in label_list:
                            self.debuglog(item.get_attribute("textContent"))
                            if item.get_attribute("textContent").find("core") != -1:
                                flag = 0
                                count_core = count_core + 1
                        if flag == 1:
                            self.debuglog("Core dump status: normal; MEMs: " + str(len(label_list)))
                            return 0
                        else:
                            self.debuglog("Core dump has been find: find " + str(count_core), "error")
                            if count_core > 0 and self.coredumpStop == True:
                                return -2
                            else:
                                return 0
                    except BaseException as e:
                        print("Fail to find label " + repr(e))
                        return -1
                        # ignore the system info
                except BaseException as e:
                    print("Unknow error, checking coredump :" + repr(e))
                    return -1
        #
        return -1

    def top_Function(self, action="reboot"):
        self.debuglog("Click top function button")
        if self.product_model == "GRP260X":
            if action == "reboot":
                try:
                    self.my_get_page("/status/account")
                    self.driver.implicitly_wait(3)
                    self.wait.until(lambda browser: self.driver.find_elements_by_xpath("//i[@class='icons icon-reboot']"))
                    self.driver.find_element_by_css_selector("[class='icons icon-reboot']").click()
                    self.driver.implicitly_wait(3)
                    try:
                        self.wait.until(lambda browser: self.driver.find_elements_by_xpath("//div[@class='ant-modal ant-modal-confirm ant-modal-confirm-confirm']"))
                        self.wait.until(lambda browser: self.driver.find_elements_by_xpath("//button[@class='ant-btn ant-btn-primary']"))
                    except:
                        pass
                    try:
                        button_list = self.driver.find_elements_by_xpath("//button[@class='ant-btn ant-btn-primary']")
                        for item in button_list:
                            if item.get_attribute("innerHTML") == "<span>OK</span>":
                                item.click()
                                self.debuglog( "Click ok button on reboot subwindow" )
                                break
                    except BaseException as e:
                        print( "Failed to click button")
                        print( repr(e) )
                        return False
                except BaseException as e:
                    print( repr(e) )
            elif action == "reset":
                return False
                # try:
                # except BaseException as e:
            self.my_waiting(10)
            return True
        elif self.product_model == "GXP21XX":
            try:
                function_list = self.driver.find_elements_by_xpath('//div[@class="feature"]/a')
                if action == "reboot":
                    self.debuglog("reboot")
                    if self.status[0] == False:
                        return True
                    try:
                        link_btn = self.findElements("link_text", "Reboot")
                        for item in link_btn:
                            item.click()
                    except BaseException as e:
                        print( "GPX21xx reboot error: " + repr(e) )
                        for item in function_list:
                            if item.get_attribute("name") == "Reboot":
                                self.move_n_click(item)
                    finally:
                        for __ in range(3):
                            try:
                                self.wait.until(lambda browser: self.driver.find_elements_by_xpath("//button[@class='button green']"))
                                self.driver.find_element_by_css_selector("[class='button green']").click()
                                self.debuglog("Begin to REBOOT")
                                return True
                            except BaseException as e:
                                continue
                elif action == "reset":
                    try:
                        link_btn = self.findElements("link_text", "Factory Reset")
                        for btn in link_btn:
                            self.move_n_click(btn)
                    except:
                        print("No button try again")
                        try:
                            reset_flag = False
                            for item in function_list:
                                if item.get_attribute("name") == "Factory Reset":
                                    reset_flag = True
                                    self.move_n_click(item)
                            if reset_flag == False:
                                return False
                            else:
                                return True
                        except BaseException as e:
                            print(repr(e))
                            print(traceback.format_exc())
                            return False
                        return False
                    self.wait.until(lambda browser: self.driver.find_elements_by_xpath("//button[@class='button green']"))
                    try:
                        self.driver.find_element_by_css_selector("[class='button green']").click()
                        self.debuglog("Begin to reset")
                        return True
                    except:
                        self.debuglog("Failed: reset")
                        return False
                elif action == "provision":
                    try:
                        link_btn = self.findElement("link_text", "Provision")
                        self.move_n_click(link_btn)
                        print("Click provision")
                        return True
                    except BaseException as e:
                        try:
                            for item in function_list:
                                if item.get_attribute("name") == "Provision":
                                    self.move_n_click(item)
                                    return True
                        except BaseException as e:
                            print("Click provision with unkown error try 'tools'" + repr(e))
                            return False
                        return False
                elif action == "logout":
                    try:
                        for item in function_list:
                            if item.get_attribute("name") == "Admin Logout":
                                self.move_n_click(item)
                                return True
                    except:
                        print("Click logout with unkown error")
                        try:
                            link_btn = self.findElements("link_text", "Admin Logout")
                            for btn in link_btn:
                                self.move_n_click(link_btn)
                                return True
                        except BaseException as e:
                            return False
                    finally:
                        if self.driver.current_url.find("#signin:loggedOut") != -1:
                            self.debuglog("Successfully logout")
                            return True
                        else:
                            return False
            except BaseException as e:
                print( "GPX21xx top_Function error1: " + repr(e) )
                return False

    def change_provision_without_Conf(self):
        self.debuglog("Going to provision setting page")
        self.handle_expire()
        if self.provType == "browser":
            print("browser debug")
            if self.product_model == "GXP21XX":
                self.choose_nav_tab("Maintenance", "Upgrade and Provisioning")
                self.my_waiting(1)
                self.driver.refresh()
                try:
                    input_firmware_dir = self.driver.find_elements_by_xpath("//input[@name='P192']")
                    for input_box in input_firmware_dir:
                        # self.move_n_click(input_box)
                        input_box.click()
                        input_box.send_keys(Keys.CONTROL, "a")
                        input_box.send_keys(Keys.DELETE)
                        input_box.clear()
                        buttons = self.driver.find_elements_by_xpath('//div[@class="row-config last"]/button[@class="gwt-Button"]')
                        for btn in buttons:
                            if btn.get_attribute("innerHTML") == "Save and Apply":
                                self.move_n_click(btn)
                    start_btn = self.driver.find_elements_by_xpath('//div[@class="cell contents"]/div/button[@class="gwt-Button"]')
                    for btn in start_btn:
                        if btn.get_attribute("innerHTML") == "Start":
                            self.move_n_click(btn)
                            break
                    self.wait.until(lambda browser: self.driver.find_elements_by_xpath('//div[@class="wrapper"]/div[@class="content"]/div'))
                    upload_div = self.driver.find_elements_by_xpath('//div[@class="wrapper"]/div[@class="content"]/div')
                    for item in upload_div:
                        self.move_n_click(item)
                except:
                    print(traceback.format_exc())
            elif self.product_model == "GRP260X":
                self.choose_nav_tab("Maintenance", "Upgrade and Provisioning")
                self.my_waiting(1)
                self.driver.refresh()
                for _ in range(3):
                    try:
                        self.wait.until(lambda browser: self.driver.find_element_by_id('P6767'))
                    except BaseException as e:
                        self.choose_inner_menu_tab("Maintenance", "Upgrade and Provisioning", "Firmware")
                try:
                    input_firmware_dir = self.driver.find_elements_by_xpath("//input[@id='P192']")
                    for input_box in input_firmware_dir:
                        # print(input_box)
                        self.move_n_click(input_box)
                        input_box.click()
                        input_box.send_keys(Keys.CONTROL, "a")
                        input_box.send_keys(Keys.DELETE)
                        input_box.clear()
                        button = self.driver.find_elements_by_xpath("//button[@class='ant-btn sub-btn']")
                        for btn in button:
                            self.move_n_click(btn)
                    self.my_waiting(1)
                    self.handle_expire()
                    button2 = self.driver.find_elements_by_xpath("//button[@class='ant-btn sub-save-btn']")
                    for btn in button2:
                        self.move_n_click(btn)
                except BaseException as e:
                    print(repr(e))
                    print(traceback.format_exc())

                self.my_waiting(1)
                self.handle_expire()
                self.gui_close_prv()
                self.my_waiting(1)

                for __ in range(2):
                    try:
                        self.handle_expire()
                        start_btn = self.driver.find_elements_by_xpath('//button[@class="ant-btn ant-btn-primary"]')
                        for button in start_btn:
                            if button.is_displayed() and button.get_attribute("innerHTML") == "<span>Start</span>":
                                button.click()
                                break
                        break
                    except BaseException as e:
                        print("Start btn" + repr(e))
                        self.my_waiting(3)
                        continue

            self.my_waiting(3)
            # a = self.gui_control()
            self.handle_expire()

            if self.product_model == "GXP21XX":
                try:
                    start_list = self.findElements("xpath", '//table/tbody/tr/td/table/tbody/tr[2]/td/button')
                    for btn in start_list:
                        if btn.get_attribute('innerHTML') == "Start":
                            self.move_n_click(btn)
                            self.my_waiting(10)
                except BaseException as e:
                    pass
                
                try:
                    self.wait.until(lambda browser: self.driver.find_elements_by_xpath('//div[@class="gwt-Label"]'))
                    for warning in self.driver.find_elements_by_xpath('div[@class="gwt-Label"]'):
                        self.debuglog(warning.get_attribute("innerHTML"))
                except BaseException as e:
                    pass

            elif self.product_model == "GRP260X":
                for _ in range(3):
                    try:
                        self.wait.until(lambda browser: self.driver.find_elements_by_xpath('//div[@class="ant-modal install-tip-modal"]'))
                        break
                    except BaseException as e:
                        pass
                for _ in range(2):
                    try:
                        self.debuglog("Waiting Upload")
                        self.shortwait.until_not(lambda browser: self.driver.find_elements_by_xpath('//div[@class="ant-modal install-tip-modal"]'))
                        self.my_waiting(1)
                    except TimeoutException as e:
                        continue
                for _ in range(2):
                    try:
                        self.wait.until(lambda browser: self.driver.find_elements_by_xpath('//div[3]/div/span/div/div/div/span'))
                        self.debuglog("Upload error", "error")
                        self.choose_nav_tab("Maintenance", "Upgrade and Provisioning")
                        self.my_waiting(5)
                        self.choose_inner_menu_tab("Maintenance", "Upgrade and Provisioning", "Firmware")
                        # self.gui_control()
                    except TimeoutException as e:
                        break

            self.my_waiting(1)
        else:
            # Check new firmware
            self.handle_expire()
            if self.product_model == "GRP260X":
                self.choose_nav_tab("Maintenance", "Upgrade and Provisioning")
                self.my_waiting(3)
                self.choose_inner_menu_tab("Maintenance", "Upgrade and Provisioning", "Provision")
                self.my_waiting(3)
                if self.driver.current_url.find("provision") == -1:
                    self.choose_inner_menu_tab("Maintenance", "Upgrade and Provisioning", "Provision")
                try:
                    upgrade_confirm_radio = self.driver.find_elements_by_xpath('//*[@id="P8375"]')
                    for item_radio in upgrade_confirm_radio:
                        if item_radio.is_selected():
                            item_radio.click()
                except BaseException as e:
                    print( repr(e) )
            elif self.product_model == "GXP21XX":
                self.choose_nav_tab("Maintenance", "Upgrade and Provisioning")
                self.my_waiting(3)
                try:
                    self.debuglog("Select check new firmware")
                    print("Select check new firmware")
                    upgrade_confirm_radio = self.driver.find_elements_by_xpath('//*[@name="P8375" and @value="0"]')
                    for item_radio in upgrade_confirm_radio:
                        if item_radio.is_selected():
                            self.move_n_click(item_radio)
                            print("Click new firmware")
                            break
                except BaseException as e:
                    print( "Check new firmware :" + repr(e) )
                    print(traceback.format_exc())

            # click always
            self.handle_expire()
            if self.product_model == "GRP260X":
                for __ in range(2):
                    try:
                        for _ in range(2):
                            if self.driver.current_url.find("provision") == -1:
                                self.choose_inner_menu_tab("Maintenance", "Upgrade and Provisioning", "Provision")
                            else:
                                break

                        for _x in range(3):
                            try:
                                self.wait.until(lambda browser: self.driver.find_elements_by_xpath('//*[@id="P238"]/div[1]/div'))
                            except:
                                self.choose_inner_menu_tab("Maintenance", "Upgrade and Provisioning", "Provision")
                            else:
                                if self.driver.current_url.find("provision") == -1:
                                    self.my_get_page("/")
                                    self.choose_inner_menu_tab("Maintenance", "Upgrade and Provisioning", "Provision")
                                else:
                                    break
                        
                        for options in self.driver.find_elements_by_xpath('//*[@id="P238"]/div[1]/div/div'):
                            if options.get_attribute('innerHTML') == "Always Check for New Firmware":
                                self.debuglog( options.get_attribute('innerHTML') )
                                skip_flag = False
                            else:
                                self.move_n_click(options)
                                self.debuglog( "Change upgrade option" )
                                self.my_waiting(1)
                                try:
                                    self.wait.until(lambda browser: self.driver.find_elements_by_xpath('//form//div/ul/li'))
                                    target = self.driver.find_elements_by_xpath('//form//div/ul/li')
                                    for item in target:
                                        if item.get_attribute('innerHTML') == "Always Check for New Firmware":
                                            self.move_n_click(item)
                                            self.debuglog( "change to " + options.get_attribute('innerHTML') )
                                            break
                                except BaseException as e:
                                    print(repr(e))
                                    print(traceback.format_exc())
                                else:
                                    break

                    except BaseException as e:
                        print( repr(e) )
                        print(traceback.format_exc())
                        continue
                    break
            elif self.product_model == "GXP21XX":
                if self.driver.current_url.find("maintenance_upgrade") == -1:
                        self.my_get_page("/#page:maintenance_upgrade")

                for __ in range(2):
                    try:
                        option_always = self.findElements("xpath", '//input[@name="P238" and @value="0"]')
                        for item in option_always:
                            if not item.is_selected():
                                self.move_n_click(option_always)
                                print("Click always")
                                break
                    except BaseException as e:
                        print("Classic always opt click" + repr(e) )
                        print(traceback.format_exc())

            # save
            self.handle_expire()
            if self.product_model == "GRP260X":
                for __ in range(2):
                    try:
                        buttons = self.driver.find_elements_by_xpath("//button[@class='ant-btn sub-save-btn']")
                        for button in buttons:
                            self.debuglog("Find save button")
                            self.move_n_click(button)
                        self.my_waiting(3)
                    except BaseException as e:
                        print( "click button error: " + repr(e) )
                        print(traceback.format_exc())
                    else:
                        break
            elif self.product_model == "GXP21XX":
                btn_list = self.driver.find_elements_by_xpath('//div[@class="row-config last"]/button[@class="gwt-Button"]')
                for button in btn_list:
                    if button.get_attribute("innerHTML") == "Save and Apply":
                        print("Save and Apply")
                        self.move_n_click(button)
                        break
            self.handle_expire()
            self.enable_maintenance_tool("provision")
            print("finish")

    def handle_expire(self):
        if self.product_model == "GRP260X":
            try:
                self.driver.find_elements_by_xpath('//p[contains(text(),"Your session will expire in less than one minute.")]')
                yes_btn = self.driver.find_elements_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div/div/div[2]/button[2]')
                for btn in yes_btn:
                    self.move_n_click(btn)
                    self.my_waiting(1)
                    break
            except BaseException as e:
                print("handle expire " + repr(e))
        elif self.product_model == "GXP21XX":
            try:
                self.driver.find_elements_by_xpath('//p[contains(text(),"Your session will expire in less than one minute.")]')
                yes_btn = self.driver.find_elements_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[contains(text(),"Yes")]')
                for btn in yes_btn:
                    self.move_n_click(btn)
                    self.my_waiting(1)
                    break
            except BaseException as e:
                print("handle expire " + repr(e))

    def enable_maintenance_tool(self, toolname):
        self.debuglog("enable maintenance tool")
        print("enable maintenance tool")
        self.driver.refresh()
        if self.product_model == "GRP260X":
            if toolname == "provision":
                try:
                    self.choose_nav_tab("Maintenance", "Upgrade and Provisioning")
                except BaseException as e:
                    self.debuglog(repr(e), 'error')
                    self.my_waiting(3)
                    self.login_phone()
                    self.my_get_page("/maintenance/upgrade/firmware")
                self.my_waiting(3)
                self.debuglog("Go maintenance")
                self.handle_expire()

                for _ in range(3):
                    try:
                        if self.driver.current_url.find("maintenance/upgrade/firmware") == -1:
                            self.choose_nav_tab("Maintenance", "Upgrade and Provisioning")
                            self.my_waiting(2)

                        self.wait.until(lambda browser: self.driver.find_element_by_id('P6767'))
                        self.move_n_click(self.driver.find_element_by_id('P6767'))
                        self.my_waiting(1)

                        if self.provType == "HTTP":
                            item = self.driver.find_elements_by_xpath('//form//li[@title="HTTP"]')
                        if self.provType == "TFTP":
                            item = self.driver.find_elements_by_xpath('//form//li[@title="TFTP"]')
                        if self.provType == "HTTPS":
                            item = self.driver.find_elements_by_xpath('//form//li[@title="HTTPS"]')
                        if self.provType == "FTP":
                            item = self.driver.find_elements_by_xpath('//form//li[@title="FTP"]')
                        if self.provType == "FTPS":
                            item = self.driver.find_elements_by_xpath('//form//li[@title="FTPS"]')
                        self.move_n_click(item[0])
                        self.wait.until(lambda browser: self.driver.find_elements_by_xpath('//*[@id="backendContent"]'))
                        input_firmware_dir = self.driver.find_elements_by_xpath("//input[@id='P192']")
                        input_firmware_name = self.driver.find_elements_by_xpath("//input[@id='P6768']")
                        input_firmware_pass = self.driver.find_elements_by_xpath("//input[@id='P6769']")
                        input_firmware_pre = self.driver.find_elements_by_xpath("//input[@id='P232']")
                        input_firmware_post = self.driver.find_elements_by_xpath("//input[@id='P233']")
                        self.my_waiting(1)
                        if len(input_firmware_dir) > 0:
                            input_firmware_dir[0].clear()
                            input_firmware_dir[0].click()
                            input_firmware_dir[0].send_keys(Keys.CONTROL, "a")
                            input_firmware_dir[0].send_keys(Keys.DELETE)
                            input_firmware_dir[0].send_keys(self.prov_dir)

                        if len(input_firmware_name) > 0:
                            input_firmware_name[0].clear()
                            input_firmware_name[0].click()
                            input_firmware_name[0].send_keys(Keys.CONTROL, "a")
                            input_firmware_name[0].send_keys(Keys.DELETE)
                            input_firmware_name[0].send_keys("")

                        if len(input_firmware_pass) > 0:
                            input_firmware_pass[0].clear()
                            input_firmware_pass[0].click()
                            input_firmware_pass[0].send_keys(Keys.CONTROL, "a")
                            input_firmware_pass[0].send_keys(Keys.DELETE)
                            input_firmware_pass[0].send_keys("")

                        if len(input_firmware_pre) > 0:
                            input_firmware_pre[0].clear()
                            input_firmware_pre[0].click()
                            input_firmware_pre[0].send_keys(Keys.CONTROL, "a")
                            input_firmware_pre[0].send_keys(Keys.DELETE)
                            input_firmware_pre[0].send_keys("")

                        if len(input_firmware_post) > 0:
                            input_firmware_post[0].clear()
                            input_firmware_post[0].click()
                            input_firmware_post[0].send_keys(Keys.CONTROL, "a")
                            input_firmware_post[0].send_keys(Keys.DELETE)
                            input_firmware_post[0].send_keys("")

                        self.my_waiting(3)
                        self.handle_expire()
                    except BaseException as e:
                        print( repr(e) )
                        print(traceback.format_exc())
                    else:
                        break
                        
                for __ in range(2):
                    self.debuglog("Start Provision")
                    try:
                        print("Click save apply")
                        button = self.driver.find_elements_by_xpath("//button[@class='ant-btn sub-save-btn']")
                        for btn in button:
                            self.move_n_click(btn)
                        self.my_waiting(2)
                    except BaseException as e:
                        print( repr(e) )
                        print(traceback.format_exc())

                    try:
                        for __ in range(2):
                            self.handle_expire()
                            button_list = self.driver.find_elements_by_css_selector("[class='ant-btn']")
                            for btn in button_list:
                                if btn.get_attribute('innerHTML') == "<span>Start</span>":
                                    btn.click()
                                    print("Start prov")
                                    self.my_waiting(4)
                                    self.move_n_click(btn)
                                    self.my_waiting(1)
                                    break
                    except BaseException as e:
                        print( repr(e) )
                        print(traceback.format_exc())
                    else:
                        self.my_waiting(10)
                        break
                self.debuglog("finish provision setup")
                return
            elif toolname == "reset":
                if self.top_Function("reset") == False:
                    self.choose_nav_tab("Maintenance", "Upgrade and Provisioning")
                    self.my_waiting(2)
                    self.driver.refresh()
                    self.choose_inner_menu_tab("Maintenance", "Upgrade and Provisioning", "Advanced Settings")
                    try:
                        print("Search function button")
                        self.driver.refresh()
                        label_list = self.findElements("xpath", '//div[@class="ant-col ant-form-item-control-wrapper"]//button')
                        for item in label_list:
                            if item.get_attribute("innerHTML") == "<span>Start</span>":
                                self.move_n_click(item)
                                self.debuglog("Click Fartory Reset")
                                self.wait.until( lambda browser: self.driver.find_elements_by_xpath('//div[@class="ant-modal-confirm-body-wrapper"]') )
                                buttons = self.findElements("xpath", '//button[@class="ant-btn ant-btn-primary"]')
                                for button in buttons:
                                    if button.is_displayed() and (button.get_attribute("innerHTML") == "OK" or button.get_attribute("innerHTML") == "Start"):
                                        self.move_n_click(button)
                        try:
                            self.wait.until(lambda browser: self.driver.find_elements_by_xpath('//div[@class="ant-modal-content"]'))
                            btn_list = self.findElements("xpath", '//div[@class="ant-modal-content"]//button[@class="ant-btn ant-btn-primary"]')
                            for item in btn_list:
                                if item.get_attribute('innerHTML') == "<span>OK</span>" and item.is_displayed():
                                    self.move_n_click(item)
                            return
                        except BaseException as e:
                            print(repr(e))
                            if repr(e).find('click: JavascriptException("javascript error")') != -1:
                                self.move_n_click(item)
                            print(traceback.format_exc())
                    except BaseException as e:
                        self.debuglog("Click reset button" + repr(e))
        elif self.product_model == "GXP21XX":
            if toolname in ["provision", "reset", "ping", "traceroute"]:
                if toolname == "provision":
                    current_tool = "Provision"
                elif toolname == "reset":
                    current_tool = "Factory Reset"
                elif toolname == "ping":
                    current_tool = "Ping"
                elif toolname == "traceroute":
                    current_tool = "Traceroute"
            if toolname == "provision":
                for _ in range(2):
                    try:
                        self.choose_nav_tab("Maintenance", "Upgrade and Provisioning")
                        self.my_waiting(3)
                        if self.driver.current_url.find("maintenance_upgrade") == -1:
                            self.my_get_page("/#page:maintenance_upgrade")

                        item = None
                        if self.provType == "HTTP":
                            item = self.driver.find_element_by_xpath('//*[@name="P6767" and @value="1"]')
                        if self.provType == "TFTP":
                            item = self.driver.find_element_by_xpath('//*[@name="P6767" and @value="0"]')
                        if self.provType == "HTTPS":
                            item = self.driver.find_element_by_xpath('//*[@name="P6767" and @value="2"]')
                        if self.provType == "FTP":
                            item = self.driver.find_element_by_xpath('//*[@name="P6767" and @value="3"]')
                        if self.provType == "FTPS":
                            item = self.driver.find_element_by_xpath('//*[@name="P6767" and @value="4"]')
                        if item != None and item.is_selected() != True:
                            self.move_n_click(item)
                        self.handle_expire()
                        break
                    except BaseException as e:
                        self.my_get_page("/#page:maintenance_upgrade")
                        print("enable maintenance setting" + repr(e))
                        print(traceback.format_exc())
                
                try:
                    input_firmware_dir = self.driver.find_elements_by_xpath("//input[@name='P192']")
                    for input_box in input_firmware_dir:
                        self.move_n_click(input_box)
                        input_box.click()
                        input_box.send_keys(Keys.CONTROL, "a")
                        input_box.send_keys(Keys.DELETE)
                        input_box.clear()
                        input_box.send_keys(self.prov_dir)

                        btn_list = self.driver.find_elements_by_xpath('//div[@class="row-config last"]/button[@class="gwt-Button"]')
                        for button in btn_list:
                            if button.get_attribute("innerHTML") == "Save and Apply":
                                self.move_n_click(button)
                                try:
                                    self.wait.until(lambda browser: self.driver.find_elements_by_xpath('//div[@class="modal-container"]/div[@class="popupContent"]/div[@class="modal"]/div[@class="wrapper"]/div[@class="content"]') )
                                    cof_btn = self.driver.find_element_by_xpath('//div[@class="modal-container"]/div[@class="popupContent"]/div[@class="modal"]/div[@class="wrapper"]/div[@class="command"]/button[@class="button green"]')
                                    self.move_n_click(cof_btn)
                                except BaseException as e:
                                    print("enable maintenance setting" + repr(e))
                                    print(traceback.format_exc())
                                else:
                                    return
                    self.handle_expire()
                except BaseException as e:
                    print("enable maintenance setting" + repr(e))
                    print(traceback.format_exc())
                else:
                    self.debuglog("Save maintenance setting")
                    self.handle_expire()

                if self.top_Function("provision") == False:
                    try:
                        self.debuglog("Failed at click top function")
                        print("Failed at click top function")
                        self.wait.until(lambda browser: self.findElements("link_text", current_tool))
                        for item in self.findElements("link_text", current_tool):
                            self.move_n_click(item)
                    except:
                        self.handle_expire()
                        self.debuglog("link test click failed", "error")
                        self.debuglog("Move to tools")
                        self.choose_nav_tab("Maintenance", "Tools")
                        self.my_waiting(3)
                        self.driver.refresh()
                        if self.driver.current_url.find("tool") == -1:
                            self.debuglog("URL is wrong")
                            raise NoSuchElementException

                        for __failCount in range(0,2):
                            try:
                                option_list = self.findElements("xpath", '//div[@class="pad-Main"]')
                                for item in option_list:
                                    count = 0
                                    for row in item.find_elements_by_xpath('//div[@class="row editableRow"]'):
                                        if row.get_attribute("innerHTML").find(current_tool) != -1:
                                            self.debuglog(row.get_attribute("innerHTML"))
                                            btn = row.find_elements_by_xpath('//div[@class="cell contents"]/button')[count]
                                            self.debuglog(btn.get_attribute('innerHTML'))
                                            btn.click()
                                            self.move_n_click(btn)
                                            self.my_waiting(1)
                                            break
                                        else:
                                            count = count + 1
                            except BaseException as e:
                                print(repr(e))
                                self.debuglog("Failed to click start button, retry", "error")
                                print(traceback.format_exc())
                                self.choose_nav_tab("Maintenance", "Tools")
                                self.my_waiting(3)
                                continue
            elif toolname == "reset":
                print("Old Color Phone UI will go to top function after element check")
                if self.top_Function("reset") == False:
                    for __ in range(3):
                        self.choose_nav_tab("Maintenance", "Tools")
                        self.my_waiting(3)
                        if self.driver.current_url.find("maintenance_tools") != -1:
                            break

                    self.my_waiting(1)
                    self.handle_expire()
                    for __failCount in range(0,3):
                        try:
                            self.wait.until(lambda browser: self.findElements("xpath", '//div[@class="pad-Main"]'))
                            item = self.findElements("xpath", '//div[@class="pad-Main"]')
                            for row in item[0].find_elements_by_xpath('//div[@class="row editableRow"]'):
                                label_tool = row.find_elements_by_xpath('//div[@class="cell label"]')
                                tool_btn = row.find_elements_by_xpath('//div[@class="cell contents"]/button')
                                for tool_index in range(len(label_tool)):
                                    if label_tool[tool_index].get_attribute("innerHTML").find(current_tool) != -1:
                                        self.move_n_click(tool_btn[tool_index])
                                        try:
                                            self.wait.until(lambda browser: self.driver.find_element_by_css_selector("[class='button green']"))
                                            btnlistg = self.driver.find_elements_by_xpath("button[@class='button green']")
                                            for btn in btnlistg:
                                                self.move_n_click(btn)
                                                print("Begin to Reset")
                                            self.debuglog("Begin to Reset")
                                            return
                                        except BaseException as e:
                                            print(repr(e))
                                            print(traceback.format_exc())
                                            self.debuglog("Failed: Reset")
                                            raise BaseException
                        except BaseException as e:
                            print(repr(e))
                            print(traceback.format_exc())
                            self.debuglog("Failed to click start button, retry", "error")
                            self.choose_nav_tab("Maintenance", "Tools")
                            self.my_waiting(3)
                            continue

        self.debuglog("enable_maintence_tool finish")

    # choose submenu !! don't refresh
    def choose_submenu(self, topmenu, subname):
        self.my_waiting(3)
        self.handle_expire()
        print("Choose submenu")
        if self.product_model == "GRP260X":
            try:
                submenu_lists = self.findElements("xpath", '//*[@class="ant-menu ant-menu-sub ant-menu-inline"]/li/a')
                for submenu in submenu_lists:
                    if submenu.get_attribute("innerHTML").find(subname) != -1:
                        time.sleep(1)
                        self.debuglog("Click " + topmenu + " -> " + subname)
                        print(submenu.get_attribute("innerHTML"))
                        self.move_n_click(submenu)
                        break
            except BaseException as e:
                print("Elem not found submenu" + repr(e))
                print(traceback.format_exc())
        elif self.product_model == "GXP21XX":
            try:
                try:
                    self.wait.until(lambda browser: self.findElement("xpath", '//*[@id="left-pad"]//div[@class="verticalMenu level1 sel"]/div[contains(text(),"' + subname + '")]'))
                except BaseException:
                    self.my_waiting(2)
                    level_1 = self.findElement("xpath", '//*[@id="left-pad"]//div[@class="verticalMenu level1"]/div[contains(text(),"' + subname + '")]')
                    self.move_n_click(level_1)
            except BaseException as e:
                print("Elem not found submenu " + repr(e))
                print(traceback.format_exc())
                

    def choose_inner_menu_tab(self, topmenu, subname, name):
        self.handle_expire()
        if self.product_model == "GRP260X":
            try:
                for __ in range(2):
                    self.my_waiting(1)
                    if name == "Advanced Settings" and self.driver.current_url.find("maintenance/upgrade/advanced") != -1:
                        break
                tabs_lists = self.findElements("xpath", '//*[@id="backendContent"]//div[@class="ant-tabs-nav-wrap"]/div/div/div/div[@role="tab"]')
                for item in tabs_lists:
                    if item.get_attribute("innerHTML").find(name) != -1:
                        self.move_n_click(item)
                        break
            except BaseException as e:
                print("inner tab" + repr(e))

        elif self.product_model == "GXP21XX":
            try:
                level_1_tabs = self.findElements("xpath", '//*[@id="left-pad"]/div/div/div[@class="verticalMenu level1"]')
                for i in range(len(level_1_tabs)):
                    level_1_tabs_name = level_1_tabs[i].find_elements_by_xpath('div[@class="label"]')
                    if len(level_1_tabs_name) == 0:
                        raise NoSuchElementException
                        continue

                    for item in level_1_tabs_name:
                        if item.get_attribute("innerHTML").find(subname) != -1:
                            time.sleep(1)
                            print("find " + item.get_attribute("innerHTML"))
                            try:
                                level_1_tabs_plus = level_1_tabs[i].find_element_by_xpath('div[@class="expend plus"]')
                                self.move_n_click(level_1_tabs[i])
                            except BaseException as e:
                                pass
                    try:
                        sub_labels = self.driver.find_elements_by_xpath('//*[@id="left-pad"]//div[@class="verticalMenu level2"]/div[@class="label"]')
                        for tag in sub_labels:
                            print(tag.get_attribute("innerHTML"))
                            if tag.get_attribute("innerHTML").find(subname) != -1:
                                self.move_n_click(tag)
                                break
                    except BaseException as e:
                        print(repr(e))
                        print(traceback.format_exc())

            except BaseException as e:
                print(repr(e))
                print(traceback.format_exc())

    def choose_nav_tab(self, name, subname):
        self.handle_expire()
        self.debuglog("choose_nva_tab " + name + "->" + subname)
        print("choose_nva_tab " + name + " " + subname)
        self.driver.refresh()
        self.driver.implicitly_wait(5)
        if self.product_model == "GRP260X":
            """
            <span> <i class="icons icon-status active"></i><span>Status</span></span><i class="ant-menu-submenu-arrow"></i>
            <span> <i class="icons icon-account "></i><span>Accounts</span></span><i class="ant-menu-submenu-arrow"></i>
            <span> <i class="icons icon-callset "></i><span>Phone Settings</span></span><i class="ant-menu-submenu-arrow"></i>
            <span> <i class="icons icon-sysset "></i><span>Settings</span></span><i class="ant-menu-submenu-arrow"></i>
            <span> <i class="icons icon-network "></i><span>Network</span></span><i class="ant-menu-submenu-arrow"></i>
            <span> <i class="icons icon-sysset "></i><span>System Settings</span></span><i class="ant-menu-submenu-arrow"></i>
            <span> <i class="icons icon-maintenance "></i><span>Maintenance</span></span><i class="ant-menu-submenu-arrow"></i>
            <span> <i class="icons icon-app "></i><span>Application</span></span><i class="ant-menu-submenu-arrow"></i>
            """
            try:
                nav_lists = self.findElements("xpath", '//*[@class="ant-menu-submenu ant-menu-submenu-inline"]/div[@class="ant-menu-submenu-title"]')
                selected_item_open = self.findElements("xpath", '//*[@class="ant-menu-submenu ant-menu-submenu-inline ant-menu-submenu-open ant-menu-submenu-selected"]/div')
                selected_item_close = self.findElements("xpath", '//*[@class="ant-menu-submenu ant-menu-submenu-inline ant-menu-submenu-selected"]/div[@class="ant-menu-submenu-title"]')
                for item in nav_lists:
                    if item.get_attribute("innerHTML").find(name) != -1:
                        print(item.get_attribute("innerHTML"))
                        self.move_n_click(item)
                for item in selected_item_close:
                    if item.get_attribute("innerHTML").find(name) != -1:
                        print(item.get_attribute("innerHTML"))
                        self.move_n_click(item)
            # click
            except BaseException as e:
                print("choose nav " + repr(e))
            else:
                print("Finish and go submenu")
                self.choose_submenu(name, subname)
        elif self.product_model == "GXP21XX":
            """
            <td class="gwt-MenuItem gwt-MenuItem-selected" id="gwt-uid-56" role="menuitem" aria-haspopup="true">Status</td>
            """
            try:
                nav_lists = self.findElements("xpath", '//*[@id="midBanner"]//div[@class="pad-Menu"]//div/table/tbody/tr/td')
                for item in nav_lists:
                    if item.get_attribute("textContent") == name:
                        print("ClassicUI " + item.get_attribute("textContent"))
                        self.move_n_click(item)
                        self.driver.implicitly_wait(5)
                        self.choose_submenu(name, subname)
                        break
            except BaseException as e:
                print("choose_nav_tab" + repr(e))
                print(traceback.format_exc())

    # def gui_close_prv(self):
    #     try:
    #         wdname = '打开'
    #         hwnd = win32gui.FindWindow(None, wdname)
    #         if hwnd != 0:
    #             button = win32gui.FindWindowEx(hwnd, 0, 'Button', "取消")
    #             win32gui.SendMessage(hwnd,win32con.WM_COMMAND,1,button)
    #             time.sleep(1)
    #     except BaseException as e:
    #         print("gui_close_prv" + repr(e))

    # def gui_control(self, type="prov"):
    #     if type == "prov":
    #         try:
    #             wdname = '打开'
    #             hwnd = win32gui.FindWindow(None, wdname)
    #             # title = win32gui.GetWindowText(hwnd)
    #             if hwnd != 0:
    #                 win32gui.SetForegroundWindow(hwnd)
    #                 ComboBoxEx32 = win32gui.FindWindowEx(hwnd,0,"ComboBoxEx32",None)
    #                 comboBox = win32gui.FindWindowEx(ComboBoxEx32,0,"ComboBox",None)
    #                 filePath=""
    #                 edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)
    #                 win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filePath)

    #                 time.sleep(1)
    #                 filePath=self.prov_dir
    #                 win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filePath)
    #                 time.sleep(1)

    #                 button = win32gui.FindWindowEx(hwnd, 0, 'Button', "打开(&O)")
    #                 win32gui.SendMessage(hwnd,win32con.WM_COMMAND,1,button)
    #                 time.sleep(1)
    #                 filePath=self.firmware_bin
    #                 win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filePath)
    #                 time.sleep(1)
    #                 win32gui.SendMessage(hwnd,win32con.WM_COMMAND,1,button)
    #                 return 0
    #             else:
    #                 return -1
    #         except BaseException as e:
    #             print("gui_control" + repr(e))
    #             self.debuglog(traceback.format_exc())

    """
    flow control
    """
    def roll_version(self, number):
        try:
            number = int(number) + 1
            if number > self.versionCount or number <= 0:
                number = 1
            return number
        except BaseException as e:
            print(repr(e))
            print(traceback.format_exc())
            return 1

    # main flow control
    def exec_workflow(self):
        if self.ready == False:
            self.debuglog( "Not ready !!")
            return
        else:
            tracemalloc.start()
            self.currentloop = 0
            new_version = ""
            temp_index = 1
            count_success = 0
            failed_count = 0
            self.debuglog( "Start Tasks !!" + self.actionType )
            while self.currentloop < self.totalloop:
                print("mem: " + str(tracemalloc.get_traced_memory()[0]))
                if self.status[0] == False:
                    self.debuglog("Stop")
                    return
                if failed_count > 0:
                    print("Failed " + str(failed_count))
                if failed_count > 7:
                    self.debuglog("连续错误7-8次，停止测试", "error")
                    return
                if count_success > 0:
                    self.debuglog("=== Loop: " + str(self.currentloop) + " : success " + str(count_success) + " ===", "info")
                else:
                    self.debuglog("=== Loop: " + str(self.currentloop) + " ===", "info")
                ret = 0
                for __ in range(2):
                    try:
                        print("try open test")
                        ret = self.open_browser()
                        if ret == -1:
                            continue
                    except:
                        pass

                if ret == -1:
                    self.debuglog("Login: failed after retry", "error")
                    failed_count = failed_count + 1
                    self.currentloop = self.currentloop + 1
                    self.my_waiting(15)
                    self.status[1] = self.currentloop + 1
                    self.search_ip()
                    continue

                if self.actionType == "reset" and self.currentloop != 0:
                    ret = self.login_phone("reset")
                else:
                    self.debuglog("Login without reset")
                    ret = self.login_phone()

                if ret == -2:
                    failed_count = failed_count + 1

                if self.status[0] == False:
                    self.debuglog("Stop", 2)
                    return
                coredump_result = self.check_coredump()
                print("Coredump ret" + str(coredump_result))
                if coredump_result == -1:
                    self.debuglog( "Failed at web process", "error" )
                    failed_count = failed_count + 1
                    self.currentloop = self.currentloop + 1
                    self.my_waiting(15)
                    self.status[1] = self.currentloop + 1
                    self.search_ip()
                    continue
                elif coredump_result == -2:
                    self.debuglog( "找到CoreDump，停止测试，如要继续更改高级设置", "error" )
                    self.quit()
                    return
                if self.status[0] == False:
                    self.debuglog( "Stop", "error" )
                    self.quit()
                    return
                # go

                if self.actionType == "reboot":
                    self.top_Function("reboot")
                    if self.status[0] == False:
                        self.debuglog( "Stop", "error" )
                        self.quit()
                        return
                elif self.actionType == "provision":
                    if self.currentloop != 0:
                        if new_version.strip() != self.version.strip():
                            self.debuglog(new_version + "   " + self.version)
                            self.debuglog("Update failed! Firmware is not match!", "error")
                            failed_count = failed_count + 1
                        else:
                            temp_index = self.roll_version(temp_index)
                            count_success += 1
                            failed_count = 0
                    try:
                        if self.version == self.provList["ver{0}".format(temp_index)]:
                            temp_index = self.roll_version(temp_index)
                        if self.version == self.provList["ver{0}".format(temp_index)]:
                            self.debuglog("You select two same version firmwares", "error")
                            self.quit()
                            return

                        new_version_key = "ver{0}".format(temp_index)
                        new_version_dir = "dir{0}".format(temp_index)
                        if new_version_key in self.provList.keys():
                            self.prov_dir = self.provList[new_version_dir]
                            new_version = self.provList[new_version_key]
                    except BaseException as e:
                        self.debuglog(repr(e))

                    try:
                        if self.status[0] == False:
                            self.debuglog("Stop", "error")
                            return
                        self.debuglog("Current version: " + self.version)
                        self.debuglog("Moving to " + new_version, "info")
                        self.change_provision_without_Conf()
                    except BaseException as e:
                        self.debuglog(repr(e))

                elif self.actionType == "reset":
                    self.enable_maintenance_tool("reset")
                # waiting
                self.currentloop = self.currentloop + 1
                self.my_waiting(self.sleepTime)
                self.status[1] = self.currentloop + 1
                self.search_ip()
                if self.clean_cache:
                    self.driver.delete_all_cookies()
                    self.driver.close()
                    del self.driver
                    self.driver = webdriver.Chrome(chrome_options=self.chrome_options, service_args=self.service_args,
                                            executable_path=self.chromedriver_path)
            ##################################
            self.debuglog( "Finish Tasks !!" )

    def update_setting(self, ip, username, web_passwd, model, task_type, total, inTime, \
                        stopFlag, show_browser, browser_path, clean_cache=False, pcap_name="", ai_mode=False):
        self.ip = ip
        self.username = username
        self.web_passwd = web_passwd
        self.model = model
        if (task_type in self.taskList):
            pass
        else:
            self.debuglog("Wrong task type", "error")
            return

        if (model in self.modelList):
            spicType = ""
            if os.path.exists( os.path.abspath(configfile) ):
                f = open(os.path.abspath(configfile) , "r")
                line = f.readline()
                while line:
                    option = line.split("=")
                    if option[0] == "oldmodel":
                        if option[1].strip('"') != "":
                            filenamebin = option[1].strip()
                            spicType = filenamebin.strip('"').upper()
                        pass
                    line = f.readline()
                f.close()

            if model == "GXP21XX":
                if spicType == "GXP2130":
                    self.firmware_bin = "gxp2130fw.bin"
                elif spicType == "GXP2135":
                    self.firmware_bin = "gxp2135fw.bin"
                elif spicType == "GXP2140":
                    self.firmware_bin = "gxp2140fw.bin"
                elif spicType == "GXP2160":
                    self.firmware_bin = "gxp2160fw.bin"
                elif spicType == "GXP2170":
                    self.firmware_bin = "gxp2170fw.bin"
                else:
                    self.firmware_bin = "grp2610fw.bin"
            elif model == "GRP260X":
                self.firmware_bin = "grp2600fw.bin"
        else:
            self.debuglog("Wrong model type", "error")
            return

        if model == "":
            self.product_model = "GRP260X"
        else:
            self.product_model = model

        if browser_path != "":
            if os.path.exists(browser_path):
                self.browser_path = browser_path

        self.pcap_name = pcap_name
        print(pcap_name)
        self.search_lan_mac()
        self.actionType = task_type
        self.totalloop = int(total)
        self.sleepTime = int(inTime)
        self.coredumpStop = stopFlag
        self.headlessFlag = show_browser
        self.clean_cache = clean_cache

    def setMessageList(self, temp):
        self.messageList = temp

    def update_prov_setting(self, prov_type, temp_list):
        if prov_type == "":
            prov_type = "HTTP"
        self.provType = prov_type
        if 'ver3' in temp_list.keys() and 'dir3' in temp_list.keys():
            if temp_list['ver3'].strip() == "" or temp_list['dir3'].strip() == "":
                self.provList = {'ver1': temp_list["ver1"].strip(), 'dir1': temp_list["dir1"].strip(),
                                'ver2': temp_list["ver2"].strip(), 'dir2': temp_list["dir2"].strip()}
            else:
                self.provList = temp_list
        else:
            self.provList = {'ver1': temp_list["ver1"].strip(), 'dir1': temp_list["dir1"].strip(),
                            'ver2': temp_list["ver2"].strip(), 'dir2': temp_list["dir2"].strip()}
        count = 0
        if 'ver1' in self.provList.keys() and 'dir1' in self.provList.keys():
            count = count + 1
        if 'ver2' in self.provList.keys() and 'dir2' in self.provList.keys():
            count = count + 1
        if 'ver3' in self.provList.keys() and 'dir3' in self.provList.keys():
            count = count + 1
        print(self.provList)
        self.versionCount = count

    def setStatus(self, status):
        self.status = status

    def __del__(self):
        print("del")
        if self.driver != None:
            self.driver.quit()
            del self.driver
        if self.webServer != None:
            self.webServer.stop()
            del self.webServer

    def quit(self):
        self.status[0] = False
        print("Quit")

    def debuglog(self, msg, type="debug"):
        if type == "error":
            msg = '<span  style="color:red">' + msg + "</span>"
        elif type == "info":
            msg = '<span  style="color:blue">' + msg + "</span>"
        else:
            msg = "<span style=\"color:black\">" + msg + "</span>"
            
        timeStr = "<span style=\"color:black\">" + time.strftime("[%m-%d %H:%M:%S] ",time.localtime())
        msg = timeStr + "</span>" + msg
        self.messageList.append(msg)

if __name__ == "__main__":
    man = SpiderThread()
    testStatus = [False]
    man.setStatus(testStatus)
    messageList = deque()
    man.setup_chrome()
    man.setMessageList(messageList)
    man.update_setting("192.168.92.52", "admin", "123456", "GXP21XX", "reset", 3, 100)
    man.exec_workflow()
