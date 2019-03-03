import time
from . import web
from pprint import pprint
import random

class ViewPort:
    def __init__(self,tier,webster,debug,web):
        #local variables
        self.webster=webster

        #debug object
        self.debug=debug
        self.tier=tier+1

        #set local browser for viewport tests
        self.web=web

        #Test Dictionary
        self.test_dictionary={}

    #COMMENCE TEST
    def unit_test(self):
        print("viewport tests")

        #self.web.linked_list_all_elements.add_report(node.selenium_object,pilot)
        node=self.web.linked_list_all_elements.cur_node
        tests = [self.is_element_obstructed,self.is_element_text_blocked]
        while node:
            for test in tests:
                if test(node):
                    value=None
                    key=node.element_dictionary['attribute_dictionary']['outerHTML'][:50]
                    if key in self.test_dictionary.keys():
                        if isinstance(self.test_dictionary[key], list):
                            value=self.test_dictionary[key]
                            value.append(test.__name__)

                        elif isinstance(self.test_dictionary[key], str):
                            value=[]
                            value.append(self.test_dictionary[key])
                            value.append(test.__name__)
                    else:
                        value=test.__name__
                    self.test_dictionary.update({key:value})
            node=node.next

        return self.test_dictionary

    def is_element_obstructed(self,node):
        if (    (self.is_element_off_page_partial(node) and not self.is_element_off_page_entirely(node)) and
                (not node.element_dictionary['attribute_dictionary']['aria-hidden'])
            ):
            return True
        else:
            return False

    def is_element_off_page_partial(self,node):
        if ( (node.element_dictionary['element_specifications']['x'] < 0 or
                (node.element_dictionary['element_specifications']['x']+node.element_dictionary['element_specifications']['width']) > self.web.client_width)

            or

            (node.element_dictionary['element_specifications']['y'] < 0 or
                (node.element_dictionary['element_specifications']['y']+node.element_dictionary['element_specifications']['height']) > self.web.client_height) ):

            return True
        else:
            return False

    def is_element_off_page_entirely(self,node):
        if ( (node.element_dictionary['element_specifications']['x']+node.element_dictionary['element_specifications']['width']) <= 0 or
                (node.element_dictionary['element_specifications']['x'] >= self.web.client_width)

            or

            (node.element_dictionary['element_specifications']['y']+node.element_dictionary['element_specifications']['height']) <= 0 or
                (node.element_dictionary['element_specifications']['y'] >= self.web.client_height) ):

            return True
        else:
            return False

    def is_element_text_blocked(self, node):
        return False
