from . import webster
from . import web as w
from pprint import pprint
from . import debug as bug
from . import viewport as vp
from . import response_behavior as rb
import sys
import os
from . import sites

class Main:
    def __init__(self, webster, viewport_num=2):
        #local variables
        self.tier=1
        self.debug=bug.Debug()
        self.webster=webster
        self.web=None

    def test_units(self,url,test=False):
        self.webster.url = url
        return_dictionary={}
        if test:
            return True
        else:
            #Site Tests
            self.web=w.Web(tier=self.tier,webster=self.webster,debug=self.debug)

            #Site Tests
            self.site=sites.Site(self.web.driver,self.debug,self.tier+1,self.webster)
            self.site_tests=self.site.unit_test()

            #Viewport Tests
            self.viewport=vp.ViewPort(tier=self.tier,webster=self.webster,debug=self.debug,web=self.web)
            self.viewport_tests=self.viewport.unit_test()

            creed_dictionary={}
            creed_dictionary.update({"site":self.site_tests})
            creed_dictionary.update({"viewport":self.viewport_tests})
            pprint(creed_dictionary)
            return creed_dictionary

    def quit_driver(self):
        try:
            self.web.driver.quit()
        except:
            pass

    def debug_error(self,error):
        self.debug.press(feed=error,error=True,tier=0)
