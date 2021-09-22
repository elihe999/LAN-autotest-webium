import csv
import errno
import os
from selenium.webdriver.common.by import By
from wpoium import Element, Elements, Browser, CSSElement

"""
Load a cvs
name  |  method  |  context
"""
class load_custom_loc():
    key_list = []
    replace_list = []
    def __init__(self, filename):
        if os.path.isfile(filename):
            temp_with_type = []
            temp_replace = []
            with open(filename) as f:
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
                            "method": 'xpath',
                            "context": row[1]
                        }
                        temp_replace.append(pending)
            # End with region
            self.key_list = temp_with_type
            self.replace_list = temp_replace
        else:
            print("File not found")
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    def get_by_value(self, name=""):
        for item in self.key_list:
            if item['name'] == name:
                return (item["method"], item["context"])

    def get_simple_result(self, name=""):
        for item in self.replace_list:
            if item['name'] == name:
                return item['context']

    def return_find_elem(self, name="", describe=""):
        tup_by_value = self.get_by_value(name)
        if tup_by_value == None:
            raise IndexError("Not matching keyword : " + name)
        if tup_by_value[0] == "id":
            return Element(id_=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "name":
            return Element(name=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "classname":
            return Element(classname=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "tagname":
            return Element(tag=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "linktext":
            return Element(class_name=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "partiallink":
            return Element(partial_link_text=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "xpath":
            return Element(xpath=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "cssselector":
            return Element(css=tup_by_value[1], describe=describe)

    def return_finds_elem(self, name="", describe=""):
        tup_by_value = self.get_by_value(name)
        if tup_by_value == None:
            raise IndexError("Not matching keyword : " + name)
        if tup_by_value[0] == "id":
            return Elements(id_=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "name":
            return Elements(name=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "classname":
            return Element(classname=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "tagname":
            return Element(tag=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "linktext":
            return Element(class_name=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "partiallink":
            return Element(partial_link_text=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "xpath":
            return Element(xpath=tup_by_value[1], describe=describe)
        if tup_by_value[0] == "cssselector":
            return Element(css=tup_by_value[1], describe=describe)

    def return_simple_string(self, name=""):
        answer_string = self.get_simple_result(name)
        if answer_string == None:
            raise IndexError("Not matching keyword : " + name)
        else:
            return answer_string

if __name__ == "__main__":
    pass