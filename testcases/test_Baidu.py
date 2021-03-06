"""
@author:  Eli
@data: 2021-06-10
@function pytest 参数使用
"""
from page.baidu_page import BaiduPage, BaiduIndexPage
import sys
import json
from time import sleep
import pytest
from os.path import dirname, abspath

base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)


@pytest.fixture(scope='session')
def global_mac_addr():
    return {'presetMac': ''}


"""
@name: Baidu context test
"""


class TestBaidu:
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

    def test_Baidu_Main(self, browser, metadata, global_mac_addr):
        """
        emtpy
        """
        print(browser)

        page = BaiduIndexPage(browser)
        page.get("http://www.baidu.com")
        sleep(10)
        print("test search")
        page.search_input = "page object"
        page.search_button.click()


if __name__ == '__main__':

    pytest.main(["-v", "-s", "test_Empty.py::TestBaidu::test_Baidu_Main"])
