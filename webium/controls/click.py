from selenium.webdriver.remote.webelement import WebElement


class Clickable(WebElement):

    def click(self, jquery=False):
        """
        Click by WebElement, if not, JQuery click
        """
        if jquery:
            from webium.jquery import JQuery
            e = JQuery(self)
            e.click()
        else:
            super(Clickable, self).click()
