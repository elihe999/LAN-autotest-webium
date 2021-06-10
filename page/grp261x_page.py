from wpoium import Page, Element


class Grp260xLoginPage(Page):
    login_box = Element(id_="login-box", describe="Login Box")
    username_input = Element(class_name="gwt-TextBox", describe="Username Input")
    password_input = Element(class_name="gwt-PasswordTextBox", describe="Password Input")
    submit_button = Element(class_name="gwt-Button", describe="Password Input")
    language_select = Element(xpath='//*[@id="control-pad"]//div/select[@class="gwt-ListBox"]', describe="Language Select")
    info_popout = Element(xpath="//*[@class='left message']/p", describe="Popout alert")
    popout_close = Element(xpath='//div[@class="popupContent"]//span[@class="closebtn"]', describe="Close Popout button")
