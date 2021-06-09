import csv
import os
from selenium.webdriver.common.by import By
from webium import Find, Finds

class load_custom_loc():
    key_list = []
    replace_list = []
    def __init__(self, file_name):
        if os.path.isfile(file_name):
            temp_with_type = []
            temp_replace = []
            with open(file_name) as f:
                f_cvs = csv.reader(f)
                for row in f_cvs:
                    if len(row) == 3:
                        pending = {
                            "name": row[0],
                            "method": row[1],
                            "context": row[2]
                        }
                        temp_with_type.append(pending)
                    elif len(row) == 2:
                        pending = {
                            "name": row[0],
                            "context": row[1]
                        }
                        temp_replace.append(pending)

            self.key_list = temp_with_type
            self.replace_list = temp_replace

    def get_by_value(self, name=""):
        for item in self.key_list:
            if item['name'] == name:
                return (item["method"], item["context"])

    def get_simple_result(self, name=""):
        for item in self.replace_list:
            if item['name'] == name:
                return item['context']

    def return_find_elem(self, name=""):
        tup_by_value = self.get_by_value(name)
        if tup_by_value == None:
            raise IndexError("Not matching keyword : " + name)
        if tup_by_value[0] == "id":
            return Find(by = By.ID, value = tup_by_value[1])
        if tup_by_value[0] == "name":
            return Find(by = By.NAME, value = tup_by_value[1])
        if tup_by_value[0] == "classname":
            return Find(by = By.CLASS_NAME, value = tup_by_value[1])
        if tup_by_value[0] == "tagname":
            return Find(by = By.TAG_NAME, value = tup_by_value[1])
        if tup_by_value[0] == "linktext":
            return Find(by = By.LINK_TEXT, value = tup_by_value[1])
        if tup_by_value[0] == "partiallink":
            return Find(by = By.PARTIAL_LINK_TEXT, value = tup_by_value[1])
        if tup_by_value[0] == "xpath":
            return Find(by = By.XPATH, value = tup_by_value[1])
        if tup_by_value[0] == "cssselector":
            return Find(by = By.CSS_SELECTOR, value = tup_by_value[1])

    def return_finds_elem(self, name=""):
        tup_by_value = self.get_by_value(name)
        if tup_by_value == None:
            raise IndexError("Not matching keyword : " + name)
        if tup_by_value[0] == "id":
            return Finds(by = By.ID, value = tup_by_value[1])
        if tup_by_value[0] == "name":
            return Finds(by = By.NAME, value = tup_by_value[1])
        if tup_by_value[0] == "classname":
            return Finds(by = By.CLASS_NAME, value = tup_by_value[1])
        if tup_by_value[0] == "tagname":
            return Finds(by = By.TAG_NAME, value = tup_by_value[1])
        if tup_by_value[0] == "linktext":
            return Finds(by = By.LINK_TEXT, value = tup_by_value[1])
        if tup_by_value[0] == "partiallink":
            return Finds(by = By.PARTIAL_LINK_TEXT, value = tup_by_value[1])
        if tup_by_value[0] == "xpath":
            return Finds(by = By.XPATH, value = tup_by_value[1])
        if tup_by_value[0] == "cssselector":
            return Finds(by = By.CSS_SELECTOR, value = tup_by_value[1])

    def return_simple_string(self, name=""):
        answer_string = self.get_simple_result(name)
        if answer_string == None:
            raise IndexError("Not matching keyword : " + name)
        else:
            return answer_string