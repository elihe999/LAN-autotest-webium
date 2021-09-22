"""
@author:  Eli
@data: 2021-06-10
@function pytest 参数使用
"""
import sys
import json
import pytest
from os.path import dirname, abspath

from wpoium.plugins.networking.Utils.base import Base

base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
from page.grp261x_page import Grp261xLoginPage, Grp261xPageStatusSystemInfo, Grp261xPageAccountGeneral, Grp261xPageSettings, Grp261xPageNetwork, Grp261xPageMaintenance, Grp261xPageDirectory

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

def get_ip(mac_addr):
    import time
    from wpoium.plugins.networking.Scanners.arp_scanner import ArpScan
    base: Base = Base(admin_only=True, available_platforms=['Linux', 'Darwin', 'Windows'])
    current_network_interface = "本地连接"
    arp_scan: ArpScan = ArpScan(network_interface=current_network_interface)
    if mac_addr != "":
        ip = arp_scan.get_ip_address(mac_addr,show_scan_percentage=True)
        print("Find IP: ", ip)
        return ip
    else:
        base.print_error("Can not find Device IP Address!!")
        raise None
        return None

@pytest.fixture(scope = 'session')
def global_mac_addr():
    return {'presetMac': ''}

"""
@name: web context test
"""
class TestGrp261x:
    """Test Case Setup"""
    def setup_class(self):
        base: Base = Base(admin_only=True, available_platforms=['Linux', 'Darwin', 'Windows'])
        print(base.list_of_network_interfaces())
 
    def teardown_class(self):
        print('Pytest所有用例的后置，所有用例执行之后只执行一次')
 
    def setup(self):
        print('Pytest每个用例前置')
 
    def teardown(self):
        print('Pytest每个用例后置')

    """Basic Test"""
    @pytest.mark.run(order=1)
    def test_device_title(self, browser, metadata, global_mac_addr):
        """
        Name: Check Web Title
        Test Step:
        1. Open Device IP
        2. Check Title on browser tab
        CheckPoint:
        * Check Title
        """
        _passwd = metadata["passwd"]
        _mac = metadata["mac"]
        _name = metadata["name"]
        # set mac addr        
        global_mac_addr['presetMac'] = _mac
        # get ip addr
        ip_addr = get_ip(_mac)
        http_ip_addr = "http://" + ip_addr
        page = Grp261xLoginPage(browser, url=http_ip_addr)
        # test begin
        page.get(http_ip_addr)
        page.custom_wait(2)
        print(browser.title)
        if "Loading Web" in browser.title:
            page.custom_wait(10)
        page.write_requests_log()
        # assert browser.title == "Grandstream | Executive IP Phone"

        page.goto("/#signin:loggedOut")
        page.refresh()
        page.refresh()
        assert ip_addr in page.get_url
        # Ignore glass panel
        try:
            page.custom_wait(12).until_not(lambda browser: page.popout_panel_glass)
        except BaseException:
            pass
        page.custom_wait(1)
        page.username_input = _name
        page.password_input = _passwd
        page.custom_wait(1)
        page.submit_button.click()
        page.set_window_size()
        page.custom_wait(2)
        page.write_requests_log()
        authed_page = Grp261xPageStatusSystemInfo(browser)
        authed_page.write_requests_log()
        page.custom_wait(2)
        assert authed_page.ver_label

if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_GRP261x_Context.py::TestGrp261x::test_device_login"])