from wpoium import Page, Element
from wpoium.plugins import cvs_helper

from os.path import dirname, abspath, join
import sys

base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
page_path = join(base_path, 'page')
wordlist = cvs_helper.load_custom_loc( join( page_path, 'baidu_preset.csv') )

class BaiduPage(Page):
    login_button = Element(id_="s-top-loginbtn", describe="顶部登录按钮")

class BaiduIndexPage(BaiduPage):
    search_input = Element(id_="kw", describe="搜索框")
    search_button = Element(id_="su", describe="搜索按钮")
    settings = Element(css="#s-usersetting-top", describe="设置")
    search_setting = Element(css="#s-user-setting-menu > div > a.setpref", describe="搜索设置")
    save_setting = Element(link_text="保存设置", describe="保存设置")