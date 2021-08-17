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

@pytest.fixture(scope = 'session')
def global_ip_addr():
    return {'presentIpAddr': ''}

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
    def test_device_title(self, browser, metadata, global_ip_addr):
        """
        Name: Check Web Title
        Test Step:
        1. Open Device IP
        2. Check Title on browser tab
        CheckPoint:
        * Check Title for OEM
        """
        _passwd = metadata["passwd"]
        _url_str = metadata["base_url"]
        _name = metadata["name"]
        # set ip addr        
        global_ip_addr['presentIpAddr'] = _url_str

        page = Grp261xLoginPage(browser, url=_url_str)
        # test begin
        page.get(_url_str)
        sleep(2)
        print(browser.title)
        page.write_requests_log()
        assert browser.title == "Grandstream | Executive IP Phone"

    @pytest.mark.run(order=2)
    def test_device_login(self, browser, metadata, global_ip_addr):
        """
        Name: Check Login
        Test Step:
        1. Open Device IP
        2. Entry username and password
        CheckPoint:
        1. IP
        2. Login find version
        Expect:
        * Login Success
        """
        _passwd = metadata["passwd"]
        _url_str = metadata["base_url"]
        _name = metadata["name"]
        page = Grp261xLoginPage(browser, url=_url_str)
        page.get(_url_str)
        page.goto("/#signin:loggedOut")
        page.refresh()
        page.refresh()
        assert global_ip_addr['presentIpAddr'] in page.get_url

        try:
            page.custom_wait(12).until_not(lambda browser: page.popout_panel_glass)
        except BaseException:
            pass
        sleep(1)
        page.username_input = _name
        page.password_input = _passwd
        sleep(1)
        page.submit_button.click()
        page.set_window_size()
        sleep(2)
        page.write_requests_log()
        authed_page = Grp261xPageStatusAccount(browser)
        authed_page.write_requests_log()
        sleep(2)
        assert authed_page.ver_label

if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_GRP261x_Context.py::TestGrp261x::test_device_login"])