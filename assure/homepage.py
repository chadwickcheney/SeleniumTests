from . import webhelper
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

class HomePage:
    def __init__(self,web,debug,tier,webster):
        self.web=web
        self.driver=self.web.driver
        self.debug=debug
        self.tier=tier
        self.webster=webster
        self.webhelper = webhelper.WebHelper(self.driver)
        self.test_dictionary={}

    def unit_test(self):
        print("Homepage Tests")
        tests=[self.product_links_are_successful, self.get_brands_colors]
        for test in tests:
            self.debug.press(feed='Running test {}'.format(test.__name__),tier=self.tier+1)
            self.test_dictionary.update({test.__name__:test()})
        return self.test_dictionary

    def product_links_are_successful(self):
        elements_product_links_false=[]
        node = self.web.linked_list_all_elements.cur_node
        while node:
            try:
                url=node.selenium_object.get_attribute('href')
                if url:
                    if url != self.url_after_click(url):
                        elements_product_links_false.append(node.selenium_object.get_attribute('outerHTML'))
            except NoSuchElementException:
                pass
            except AttributeError:
                pass
            node=node.next
        if len(elements_product_links_false)==0:
            return True
        return elements_product_links_false

    def get_brands_colors(self):
        colors=[]
        node = self.web.linked_list_all_elements.cur_node
        while node:
            if not node.element_dictionary['css_dictionary']['background-color'] in colors:
                colors.append(node.element_dictionary['css_dictionary']['background-color'])
            node = node.next
        return colors

    def has_href(self, element):
        if element.get_attribute('href'):
            return element.get_attribute('href')
        else:
            return False

    def url_after_click(self,url):
        self.webhelper.open_new_tab_switch_focus(url)
        post_url = self.driver.current_url
        self.webhelper.switch_focus_main_window
        return post_url
