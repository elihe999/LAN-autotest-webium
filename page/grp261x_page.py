from wpoium import Page, Element, Elements


class Grp261xLoginPage(Page):
    login_box = Element(id_="login-box", describe="Login Box")
    username_input = Element(class_name="gwt-TextBox", describe="Username Input")
    password_input = Element(class_name="gwt-PasswordTextBox", describe="Password Input")
    submit_button = Element(class_name="gwt-Button", describe="Password Input")
    language_select = Element(xpath='//*[@id="control-pad"]//div/select[@class="gwt-ListBox"]', describe="Language Select")
    info_popout = Element(xpath="//*[@class='left message']/p", describe="Popout alert")
    popout_close = Element(xpath='//div[@class="popupContent"]//span[@class="closebtn"]', describe="Close Popout button")
    popout_panel_glass = Element(class_name="gwt-PopupPanelGlass", describe="popout panel")

class Grp261xPageStatusAccount(Page):
    ver_label = Element(xpath="/html/body/div[2]/div/div/div[4]/div/div[2]/div", describe="Version Label")
    navleft_oem_product = Element(xpath="/html/body/div[2]/div/div/div[4]/div/div[2]/div", describe="Product Name")
    navright_func_btns = Elements(xpath="/html/body/div[2]/div/div/div[3]/div[1]/div/div[2]/div[@class=\"feature\"]", describe="Function Button")
    account_status = Elements(xpath='//tbody/tr[1]//tr[@class="table-row"]', describe="Account Status")
    vertical_menu_select = Element(xpath='//div[@class="verticalMenu level1 sel"]/div[@class="label"]', describe="Selected Submenu")
    popout_panel_glass = Element(class_name="gwt-PopupPanelGlass", describe="popout panel")

class Grp261xPageAccountGeneral(Page):
    ver_label = Element(xpath="/html/body/div[2]/div/div/div[4]/div/div[2]/div", describe="Version Label")
    title = Element(xpath="//div/table/tbody/tr//div/h1", describe="table title")

class Grp261xPageSettings(Page):
    ver_label = Element(xpath="/html/body/div[2]/div/div/div[4]/div/div[2]/div", describe="Version Label")

