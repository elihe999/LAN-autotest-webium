"""
@author:  Eli
@data: 2021-06-10
@function pytest 参数使用
"""
import sys
import json
from time import sleep
import pytest
from os.path import dirname, abspath

base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
from page.grp261x_page import Grp261xLoginPage, Grp261xPageStatusAccount, Grp261xPageAccountGeneral, Grp261xPageSettings, Grp261xPageNetwork, Grp261xPageMaintenance, Grp261xPageDirectory

def get_data(file_path):
    """
    读取参数化文件
    :param file_path:
    :return:
    """
    data = []
    with(open(file_path, "r")) as f:
        dict_data = json.loads(f.read())
        for i in dict_data:
            data.append(tuple(i.values()))
    return data

"""
@name: web context test
"""
class TestGrp261x:
    """Test Case Setup"""
    def setup_class(self):
        print('Pytest所有用例的前置，所有用例之前只执行一次！')
 
    def teardown_class(self):
        print('Pytest所有用例的后置，所有用例执行之后只执行一次')
 
    def setup(self):
        print('Pytest每个用例前置')
 
    def teardown(self):
        print('Pytest每个用例后置')

    """Basic Test"""
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize(
        "name, passwd, base_url",
        get_data(base_path + "/testcases/data/data_file.json")
    )
    def test_device_title(self, name, passwd, browser, base_url):
        """
        Name: Check Web Title
        Test Step:
        1. Open Device IP
        2. Check Title on browser tab
        CheckPoint:
        * Check Title for OEM
        """
        page = Grp261xLoginPage(browser)
        page.get(str(base_url)+"/#signin:loggedOut")
        sleep(2)
        print(browser.title)
        page.write_requests_log()
        assert browser.title == "Grandstream | Executive IP Phone"

    @pytest.mark.run(order=2)
    @pytest.mark.parametrize(
        "name, passwd, base_url",
        get_data(base_path + "/testcases/data/data_file.json")
    )
    def test_device_login(self, name, passwd, browser, base_url):
        """
        Name: Check Login
        Test Step:
        1. Open Device IP
        2. Entry username and password
        CheckPoint: version
        * Login Success
        """
        page = Grp261xLoginPage(browser)
        page.get(base_url)
        try:
            page.custom_wait(12).until_not(lambda browser: page.popout_panel_glass)
        except BaseException:
            pass
        sleep(1)
        page.username_input = name
        page.password_input = passwd
        sleep(1)
        page.submit_button.click()
        page.set_window_size()
        sleep(2)
        page.write_requests_log()
        authed_page = Grp261xPageStatusAccount(browser)
        authed_page.write_requests_log()
        sleep(2)
        assert authed_page.ver_label

    @pytest.mark.parametrize(
        "name, passwd, base_url",
        get_data(base_path + "/testcases/data/data_file.json")
    )
    def test_device_version(self, name, passwd, browser, base_url):
        """
        Name: Check version label
        Test Step:
        1. Open Device IP
        2. Entry username and password
        3. Check version
        CheckPoint: Version
        * Login Success
        """
        page = Grp261xLoginPage(browser)
        page.get(base_url)
        authed_page = Grp261xPageStatusAccount(browser)
        sleep(2)
        assert authed_page.ver_label

    @pytest.mark.parametrize(
        "name, passwd, base_url",
        get_data(base_path + "/testcases/data/data_file.json")
    )
    def test_device_account_status(self, name, passwd, browser, base_url):
        """
        Name: Check Account Status
        Test Step:
        1. Open Device IP
        2. Login
        3. Check account status on web browser
        CheckPoint: check Account number
        """
        page = Grp261xLoginPage(browser)
        page.get(str(base_url)+"/#page:status_account")
        try:
            assert page.login_box
            page.custom_wait(12).until_not(lambda browser: page.popout_panel_glass)
            page.username_input = name
            page.password_input = passwd
            sleep(1)
            page.submit_button.click()
        except BaseException:
            pass

        try:
            page.custom_wait(12).until_not(lambda browser: page.popout_panel_glass)
        except BaseException:
            pass

        page.set_window_size()
        authed_page = Grp261xPageStatusAccount(browser)
        sleep(2)
        account_num = len(authed_page.account_status)
        font = authed_page.account1_sub_title.value_of_css_property("font-family")
        submenu_nav = authed_page.vertical_menu_select.text
        print(submenu_nav)
        sleep(2)
        print("\t---\tcheck account amount\t---\t")
        assert account_num < 7
        assert authed_page.vertical_menu_select.is_displayed() == True
        assert font == "\"Open Sans\", sans-serif"
        assert submenu_nav == "Account Status"

    @pytest.mark.parametrize(
        "name, passwd, base_url",
        get_data(base_path + "/testcases/data/data_file.json")
    )
    def test_device_account_general(self, name, passwd, browser, base_url):
        """
        Name: Check Account General
        Test Step:
        1. Open Device IP
        2. Login
        3. Check account general page on web browser
        CheckPoint: Check Account Index and font-family
        """
        page = Grp261xLoginPage(browser)
        page.get(str(base_url)+"/#page:account_1_general")
        try:
            assert page.login_box
            page.custom_wait(12).until_not(lambda browser: page.popout_panel_glass)
            page.username_input = name
            page.password_input = passwd
            sleep(1)
            page.submit_button.click()
        except BaseException:
            pass

        try:
            page.custom_wait(12).until_not(lambda browser: page.popout_panel_glass)
        except BaseException:
            pass

        page.set_window_size()
        authed_page = Grp261xPageAccountGeneral(browser)
        # authed_page = Grp261xPageStatusAccount(browser)
        # sleep(2)
        # account_num = len(authed_page.account_status)
        # sleep(2)
        # print("\t---\tcheck account amount\t---\t")
        # assert account_num < 7
        # assert authed_page.vertical_menu_select.is_displayed() == True
        # assert authed_page.vertical_menu_select.get_attribute("innerHTML") == "Account Status"

    @pytest.mark.parametrize(
        "name, passwd, base_url",
        get_data(base_path + "/testcases/data/data_file.json")
    )
    def test_device_network_basic(self, name, passwd, browser, base_url):
        """
        Name: Check Network page
        Test Step:
        1. Open Device IP
        2. Login
        3. Check network basic page on web browser
        CheckPoint: Basic Settings
        """
        page = Grp261xLoginPage(browser)
        page.get(str(base_url)+"/#page:network_basic")
        try:
            assert page.login_box
            page.custom_wait(12).until_not(lambda browser: page.popout_panel_glass)
            page.username_input = name
            page.password_input = passwd
            sleep(1)
            page.submit_button.click()
        except BaseException:
            pass

        authed_page = Grp261xPageAccountGeneral(browser)

    @pytest.mark.parametrize(
        "name, passwd, base_url",
        get_data(base_path + "/testcases/data/data_file.json")
    )
    def test_device_maintenance_basic(self, name, passwd, browser, base_url):
        """
        Name: Check Maintenance page
        Test Step:
        1. Open Device IP
        2. Login
        3. Check Maintenance basic page on web browser
        CheckPoint: Maintenance
        """
        page = Grp261xLoginPage(browser)
        try:
            assert page.login_box
            page.custom_wait(12).until_not(lambda browser: page.popout_panel_glass)
            page.username_input = name
            page.password_input = passwd
            sleep(1)
            page.submit_button.click()
            sleep(1)
        except BaseException:
            pass
        page.get(str(base_url)+"/#page:maintenance_web_access")

        authed_page = Grp261xPageMaintenance(browser)
        password_elements = authed_page.password_title
        num_password_title = len(password_elements)
        title_contexts = True
        for title in password_elements:
            print(title.text)
            if title.text not in ["User Password", "Admin Password"]:
                title_contexts = False
        assert num_password_title == 2
        assert title_contexts

    @pytest.mark.parametrize(
        "name, passwd, base_url",
        get_data(base_path + "/testcases/data/data_file.json")
    )
    def test_device_directory_basic(self, name, passwd, browser, base_url):
        """
        Name: Check Directory page
        Test Step:
        1. Open Device IP
        2. Login
        3. Check Directory basic page on web browser
        CheckPoint: Directory
        """
        page = Grp261xLoginPage(browser)
        page.get(str(base_url)+"/#page:contact_PHONEBOOK")
        try:
            assert page.login_box
            page.custom_wait(12).until_not(lambda browser: page.popout_panel_glass)
            page.username_input = name
            page.password_input = passwd
            sleep(1)
            page.submit_button.click()
        except BaseException:
            pass

        authed_page = Grp261xPageDirectory(browser)

# class TestGrp261xReboot:
#     @pytest.mark.parametrize(
#         "name, passwd, base_url",
#         get_data(base_path + "/testcases/data/data_file.json")
#     )
#     def test_device_reboot(self, name, passwd, browser, base_url):
#         """
#         Name: Check Login
#         Test Step:
#         1. Open Device IP
#         2. Entry username and password
#         CheckPoint:
#         * Login Success
#         """
#         page = Grp261xLoginPage(browser)
#         page.get(base_url)
#         authed_page = Grp261xPageStatusAccount(browser)
#         sleep(2)
#         for func_btn in authed_page.navright_func_btns:
#             print(func_btn)
#         assert authed_page.navright_func_btns
# searchBox.value_of_css_property(“font-family”)

if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_GRP261x_Context.py::TestGrp261x::test_device_login"])