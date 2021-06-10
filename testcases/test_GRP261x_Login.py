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
from page.grp261x_page import Grp260xLoginPage



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


@pytest.mark.parametrize(
    "name, passwd, base_url",
    get_data(base_path + "/testcases/data/data_file.json")
)
def test_baidu_search(name, passwd, browser, base_url):
    page = Grp260xLoginPage(browser)
    page.get(base_url)
    page.username_input = passwd
    page.submit_button.click()
    sleep(2)
    assert browser.title == "Grandstream | Executive IP Phone"
