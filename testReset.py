# -*- coding : utf-8 -*-
# coding:unicode_escape
from webium.testsuite.standard import dhcp_testsuite
import time
# from nose.tools import assert_false, ok_, eq_

class TestResult:
    total_number = 0
    success_number = 0
    failed_number = 0
    date_string = ""
    current_case = ""
    current_index = 0
    stop_flag = 0
    case_loop = 1

@dhcp_testsuite
def myfun(ip, passwd, sleep, flag, suite_info, initwd='admin', username='admin'):
    print("cleaning")
    time.sleep(sleep)

Test = False
newTestSuite = TestResult()
myfun(ip='192.168.92.41', passwd='1', sleep=3, flag=Test, suite_info=newTestSuite)

# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webelement import WebElement
# from webium.controls.link import Link
# from webium.controls.select import Select

# from webium.driver import get_driver
# from webium import BasePage, Find, Finds, Actions
# from webium import settings
# from webium.plugins import cvs_helper
# from webium import wait
# import time

# wordListClassic = cvs_helper.load_custom_loc('preset_elm/gs_classic.csv')
# wordListAntD = cvs_helper.load_custom_loc('preset_elm/gs_antd.csv')

# class AntDesignLoginPage(BasePage):
#     login_box = wordListAntD.return_find_elem('loginbox')
#     name_field = wordListAntD.return_find_elem('usernameinput')
#     password_field = wordListAntD.return_find_elem('passwordinput')
#     button = wordListAntD.return_find_elem('loginsubmit')
#     # language
#     lang_select = wordListAntD.return_find_elem('loginboxlangselect')
#     language_ul = Finds(by=By.XPATH, value='//*[@id="localeSelect"]//div/ul[@class="ant-dropdown-menu ant-dropdown-menu-light ant-dropdown-menu-root ant-dropdown-menu-vertical"]/li')

# class AntDesignMainPage(BasePage):
#     reboot_link_btn = Find(by=By.XPATH, value='//*[@id="root"]//header//i[@class="icons icon-reboot"]')
#     reboot_ok_btn = Find(by=By.XPATH, value='/html/body/div[3]/div/div[2]/div/div[2]/div/div/div[2]/button[2]')

# class ClassicLoginPage(BasePage):
#     login_box = wordListClassic.return_find_elem('loginbox')
#     name_field = wordListClassic.return_find_elem('usernameinput')
#     password_field = wordListClassic.return_find_elem('passwordinput')
#     button = wordListClassic.return_find_elem('loginsubmit')
#     # language
#     lang_select = wordListClassic.return_simple_string('loginboxlangselect')
#     lang_select_box = Find(Select, By.XPATH, lang_select)

# class ClassicMainPage(BasePage):
#     reboot_link_btn = Find(by=By.LINK_TEXT, value="Reboot")
#     ver_label = Find(by=By.XPATH, value='//*[@id="verNo"]/div')
#     reboot_ok_btn = Find(by=By.XPATH, value="//button[@class='button green']")
#     label_list = Finds(by=By.XPATH, value='//div[@class="ant-col ant-form-item-control-wrapper"]/div/span/div/div[@class="ant-row"]/div[1]')
#     topbaner = wordListClassic.return_find_elem('topBanner')
#     popoutwindow = wordListClassic.return_finds_elem('popupContent')
#     resetpassword = wordListClassic.return_finds_elem('resetpassword')

# class ClassicToolsPage(BasePage):
#     provisonButton = Find(by=By.XPATH, value='//*[@id="elm-23"]')
#     resetButton = Find(by=By.XPATH, value='//*[@id="elm-25"]')


# class task_flow():
#     username = ''
#     password = ''
#     initpasswd = ''
#     loop = 1
#     interval = 100
#     def __init__(self, style):
#         self.style = style
#         self.find_core_stop = False
    
#     def login_info(self, user, passwd):
#         self.username = user
#         self.password = passwd

#     def set_coredump_flag(self, flag):
#         if flag:
#             self.find_core_stop = True
#         else:
#             self.find_core_stop = False

#     def set_loop(self, count, interval):
#         if count >= 1:
#             self.loop = count
#         if interval >= 30:
#             self.interval = interval
#         else:
#             print("You interval is too small")

# ###############################
# #      Custom   Action        #
# ###############################
#     def change_language(self, page):
#         if self.style == "classic":
#             page.lang_select_box.select_option('English')
#         elif self.style == "antd":
#             Actions().move_n_click(page.lang_select)
#             for lang_li in page.language_ul:
#                 print(lang_li)
#                 if lang_li.get_attribute('textContent') == "English":
#                     Actions().move_n_click(lang_li)
#         else:
#             raise IndexError("Not matching UI")

#     def find_coredump(self, elem_list):
#         for name in elem_list:
#             if name.get_attribute('innerHTML').find('core') != -1:
#                 return True
#         return False

#     def check_reset_window(self, page):
#         page.open()
#         if self.style == "classic":
#             try:
#                 wait.webiumWait().until(lambda browser: page.popoutwindow)
#                 if get_driver().find_element_by_xpath('//div[@class="heading"]/div[@class="gwt-HTML"]').get_attribute('textContent') == "Admin Password":
#                     try:
#                         i = 0
#                         for passinputbox in get_driver().find_elements_by_xpath('//input[@class="gwt-PasswordTextBox"]'):
#                             try:
#                                 if i == 0:
#                                     Actions().move_n_click(passinputbox)
#                                     passinputbox.send_keys(self..username)
#                                 else:
#                                     Actions().move_n_click(passinputbox)
#                                     passinputbox.send_keys(self.password)
#                             except BaseException as e:
#                                 print("reset " + repr(e))
#                                 pass
#                             finally:
#                                 i = i + 1
#                     except BaseException as e:
#                         print(repr(e))
#                     try:
#                         button_list = get_driver().find_elements_by_class_name("gwt-Button")
#                         for btn in button_list:
#                             if btn.get_attribute("innerHTML") == "Save" and btn.is_displayed():
#                                 Actions().move_n_click(btn)
#                     except BaseException as e:
#                         print("Click save password " + repr(e))
#             except TimeoutException:
#                 pass
#         elif self.style == "antd":
#             pass


#     def my_waiting(self, count):
#         # if count > 4:
#             # self.debuglog("waiting ：{}".format(str(count)))
#         for i in range(count):
#             time.sleep(1)
#             # if count > 4:
#         #         self.status[2] = count - i
#         #     if self.status[0] == False:
#         #         self.status[2] = 0
#         #         break
#         # self.status[2] = 0

#     def reboot(self):
#         currentloop = 0
#         while currentloop < self.loop:
#             if self.style == "classic":
#                 home_page = ClassicLoginPage(url=url)
#             elif self.style == "antd":
#                 home_page = AntDesignLoginPage(url=url)
#             home_page.open()
#             # Change language
#             change_language(home_page)
#             home_page.name_field.send_keys(tester.username)
#             home_page.password_field.send_keys(tester.password)
#             home_page.button.click()
#             # Check password reset
#             temp_page = ClassicMainPage(url=self.url)
#             self.check_reset_window(temp_page)
#             # Check system status
#             main_page = ClassicMainPage(url=self.url+"#page:status_system_info")
#             main_page.open()
#             time.sleep(5)
#             main_page.refresh
#             label_list = Finds(by=By.XPATH, value='//*[@class="data-list"]/tbody/tr/td/div/table/tbody/tr[@class="table-row"]/td[1]//div[@class="gwt-HTML last"]')
#             print(main_page.ver_label.get_attribute('textContent'))
#             time.sleep(1)
#             main_page.reboot_link_btn.click()
#             wait.webiumWait().until(lambda browser: main_page.reboot_ok_btn)
#             main_page.reboot_ok_btn.click()
#             get_driver().quit()
#             # sleep
#             self.my_waiting(self.interval)


# if __name__ == "__main__":
#     url = 'http://192.168.92.83'
#     username = 'admin'
#     password = '1'
#     style = "antd"
#     reboot(url, username, password, style)