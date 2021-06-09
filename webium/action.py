from webium.errors import WebiumException
from webium.driver import get_driver
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.remote.webelement import WebElement

class Actions(object):
    """
    """
    def __init__(self):
        self.actions = ActionChains(get_driver())

    def move_n_click(self, _target_element, delay=0):
        try:
            self.actions.move_to_element(_target_element)
            if delay > 0:
                get_driver().implicitly_wait(delay)
            self.actions.click()
            self.actions.perform()
        except BaseException as e:
            print("move_n_click: " + repr(e))

    def drag_to(self, from_elem, to_elem):
        self.actions = ActionChains(get_driver())
        self.actions.drag_and_drop(from_elem, to_elem)
        self.actions.perform()