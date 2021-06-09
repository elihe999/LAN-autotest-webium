# -*- coding:utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webium.controls.link import Link
from webium.driver import get_driver
from webium import BasePage, Find, Finds, Actions
from webium import settings
from webium.plugins import cvs_helper

wordlist = cvs_helper.load_custom_loc('preset_elm/gs_classic.csv')

class LoginPage(BasePage):
    url = ''
    name_input_field = wordlist.return_find_elem('usernameinput')
    passwd_input_field = wordlist.return_find_elem('passwordinput')
    button = wordlist.return_find_elem('loginsubmit')

class ResultItem(WebElement):
    link = Finds(Link, By.XPATH, './/h3/a')

class ResultsPage(BasePage):
    device_version = wordlist.return_finds_elem('versionTitle')

if __name__ == '__main__':
    print("Can not import configuration in this way")

"""
This is a test for device login
"""
# def testcases(*args, **kwargs)->bool:
def testcases(*args, **kwargs):
    case_result = False
    print("gs: Login device web management")
    print(kwargs)
    home_page = LoginPage(url=kwargs['ip'])
    home_page.open()
    try:
        home_page.name_input_field.send_keys('admin')
        home_page.passwd_input_field.send_keys(kwargs['passwd'])
        Actions().move_n_click(home_page.button)
        print("Go Main page")
        default_page = ResultsPage()
        print(default_page.device_version)
    except BaseException as e:
        print("__run_loop_testcases: ", e)
        return None
    return case_result

def testconfig():
    case_parameter = []
    return case_parameter