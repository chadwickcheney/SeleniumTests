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

    def test_units(self,test=False):
        return_dictionary={}
        if test:
            return True
        else:
            #Site Tests
            self.web=w.Web(tier=self.tier,webster=self.webster,debug=self.debug)
            self.site_tests=self.web.unit_test()

            #Viewport Tests
            self.viewport=vp.ViewPort(tier=self.tier,webster=self.webster,debug=self.debug,web=self.web)
            self.viewport_tests=self.viewport.unit_test()

            creed_dictionary={}
            creed_dictionary.update({"Site":self.site_tests})
            creed_dictionary.update({"Viewport":self.viewport_tests})
            return creed_dictionary

    def debug_error(self,error):
        self.debug.press(feed=error,error=True,tier=0)
