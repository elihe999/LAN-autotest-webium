from wpoium import Page, Element, Elements
from wpoium.plugins import cvs_helper

from os.path import dirname, abspath, join
import sys

base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
page_path = join(base_path, 'page')
wordlist = cvs_helper.load_custom_loc( join( page_path, 'grp261x_elem.csv') )

class Grp261xCommonPage(Page):
    ver_label = wordlist.return_finds_elem("versionLabel")
        # xpath="/html/body/div[2]/div/div/div[4]/div/div[2]/div", describe="Version Label")
    top_banner = Element(
        xpath='//*[@id="topBanner"]/div/div[1]/div', describe="Top Banner")
    navright_func_btns = Elements(
        xpath="/html/body/div[2]/div/div/div[3]/div[1]/div/div[2]/div[@class=\"feature\"]", describe="Function Button")
    config_button_div = Elements(
        xpath='//div[@class="row-config last"]/button', describe="Button row for save")
    title = Element(xpath="//div/table/tbody/tr//div/h1",
                    describe="table title")
    popout_panel = Elements(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]')

class Grp261xLoginPage(Grp261xCommonPage):
    login_box = Element(id_="login-box", describe="Login Box")
    username_input = Element(class_name="gwt-TextBox",
                             describe="Username Input")
    password_input = Element(
        class_name="gwt-PasswordTextBox", describe="Password Input")
    submit_button = Element(class_name="gwt-Button", describe="Password Input")
    language_select = Element(
        xpath='//*[@id="control-pad"]//div/select[@class="gwt-ListBox"]', describe="Language Select")
    info_popout = Element(
        xpath="//*[@class='left message']/p", describe="Popout alert")
    popout_close = Element(
        xpath='//div[@class="popupContent"]//span[@class="closebtn"]', describe="Close Popout button")
    popout_panel_glass = Element(
        class_name="gwt-PopupPanelGlass", describe="popout panel")


class Grp261xPageStatusAccount(Grp261xCommonPage):
    account_status = Elements(
        xpath='//tbody/tr[1]//tr[@class="table-row"]', describe="Account Status")
    vertical_menu_select = Element(
        xpath='//div[@class="verticalMenu level1 sel"]/div[@class="label"]', describe="Selected Submenu")
    popout_panel_glass = Element(
        class_name="gwt-PopupPanelGlass", describe="popout panel")
    account1_sub_title = Element(
        xpath='//*/tbody/tr[1]/td/div/table/tbody/tr[2]/td[1]/div[@class="column column-accounts"]/div', describe="account1 title")

class Grp261xPageSettings(Grp261xCommonPage):
    general_settings_title = Element(
        xpath='//*[@id="main-container"]/div/table/tbody/tr/td[@id="main-pad"]/div[@class="pad-Main"]/h1', describe="General Setting Title")
    sub_options = Elements(
        xpath='//*[@class="cell label"]', describe="General Setting Option")


class Grp261xPageNetwork(Grp261xCommonPage):
    ipv46_title = Elements(
        xpath="/html/body/div/div/div/div/div/table/tbody/tr/td/div/h3", describe="Title for ipv4/ipv6")
    ipv4_address = Elements(
        xpath='//select[@name="P8"]/option', describe="ipv4 address")
    ipv6_address = Elements(
        xpath='//select[@name="P1419"]/option', describe="ipv6 address")


class Grp261xPageMaintenance(Grp261xCommonPage):
    password_title = Elements(
        xpath="/html/body/div/div/div/div/div/table/tbody/tr/td/div/h3", describe="Title for user/admin")


class Grp261xPageDirectory(Grp261xCommonPage):
    contect_select = Element(
        xpath='//tbody/tr/td[@id="main-pad"]//table/tbody/tr/td/select[@class="gwt-ListBox"]', describe="Contect Type Select")
    add_context_wrapper = Elements(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]', describe="Add context wrapper")
    first_name_input = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[1]/div[@class="contents"]/input')
    last_name_input = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[2]/div[@class="contents"]/input', describe="")
    favorite_checkbox = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[3]/div[@class="contents"]/span/input')
    # 4div
    company_input = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[4]/div[1]//input')
    department_input = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[4]/div[2]//input')
    job_input = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[4]/div[3]//input')
    job_title_input = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[4]/div[4]//input')
    #
    work_input = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[6]/div[@class="contents"]/input', describe="Work")
    home_input = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[7]/div[@class="contents"]/input', describe="Home")
    moblie_input = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[8]/div[@class="contents"]/input', describe="Moblie")
    work_checkbox = Element(
        xpath='//div//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[6]/div[@class="contents"]/span')
    home_checkbox = Element(
        xpath='//div//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[7]/div[@class="contents"]/span')
    moblie_checkbox = Element(
        xpath='//div//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[8]/div[@class="contents"]/span')
    #
    accounts_select = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[9]/div[@class="contents"]/select')
    blocklist_checkbox = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[10]/div[@class="contents"]/div/span/input[@value="1"]')
    allowlist_checkbox = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[10]/div[@class="contents"]/div/span/input[@value="2"]')
    ringtone_pop_btn = Element(
        xpath='//div[@class="popupContent"]//div[@class="wrapper"]//form/div/div[11]/div[@class="contents"]/div//button')


class Grp261xPageAccountGeneral(Grp261xCommonPage):
    vertical_menu_select = Element(
        xpath='//div[@class="verticalMenu level2 sel"]/div[@class="label"]')


class Grp261xPageStatusNetworkStatus(Grp261xPageStatusAccount):
    ns_status_labels = Elements(
        xpath='//td[@id="main-pad"]/div[@class="pad-Main"]//div[@class="cell label"]', describe="Network Status Label")
    ns_status_contents = Elements(
        xpath='//td[@id="main-pad"]/div[@class="pad-Main"]//div[@class="cell contents"]', describe="Network Status Contents")

class Grp261xPageStatusSystemInfo(Grp261xPageStatusAccount):
    coredump_download_a = Elements(xpath='//tbody/tr[1]/td/div/table/tbody/tr[2]//a', describe="")

# Share with Grp261xPageStatusSoftkey
class Grp261xPageStatusVPK(Grp261xPageStatusAccount):
    vpk_name = Elements(xpath='//td[1]/div[@class="column column-accounts"]/div', describe="")
    vpk_mode = Elements(xpath='//td[2]/div[@class="column column-accounts"]/div', describe="")
    vpk_account = Elements(xpath='//td[3]/div[@class="column column-accounts"]/div', describe="")
    vpk_descript = Elements(xpath='//td[4]/div[@class="column column-accounts"]/div', describe="")
    vpk_value = Elements(xpath='//td[5]/div[@class="column column-accounts"]/div', describe="")


