from . import webster
from . import web as w
import pprint
from . import debug as bug
from . import viewport as vp
from . import response_behavior as rb
import sys
import os

class Main:
    def __init__(self, webster, viewport_num=2):
        #local variables
        self.tier=1
        self.debug=bug.Debug()
        self.webster=webster
        self.web=None

    def test_units(self):
        self.web=w.Web(tier=self.tier,webster=self.webster,debug=self.debug)
        #viewport test
        self.viewport=vp.ViewPort(tier=self.tier,webster=self.webster,debug=self.debug,web=self.web)
        self.debug.press(feed='Viewport Test',tier=self.tier)
        self.viewport.unit_test()

        node = self.web.linked_list_all_elements.cur_node
        while node:
            if node.pilot:
                self.web.linked_list_all_elements.print_specifications(node)
                self.web.scroll_element_view(node.selenium_object)
                self.web.highlight(node.selenium_object)
                input('>>>')
            node = node.next
    def debug_error(self,error):
        self.debug.press(feed=error,error=True,tier=0)
