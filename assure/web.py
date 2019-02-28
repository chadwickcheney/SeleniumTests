from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from . import firefox_browser
from . import chrome_browser
from fake_useragent import UserAgent
from selenium import webdriver
import pickle
import time
from pprint import pprint
from . import html_element
from . import sites

class Web:
    def __init__(self,tier,webster,debug):
        #local variables
        self.tier=tier+1
        self.driver=None
        self.viewport=None
        self.browser=None
        self.webster=webster
        self.desktop=self.webster.shared_dictionary['desktop']
        self.chrome=self.webster.shared_dictionary['chrome']
        self.debug=debug

        #variables for element_dictionary
        self.avoid_tag_names=["head","html","body","meta","style","link","script","title","noscript","path","polygon"]#what is noscript and should I worry about it
        self.break_tag_names=["head","html","body","meta"]#what is noscript and should I worry about it
        #("tag",find_if_in_parents)
        self.css_grab_tags_tuples=(("color",False),("height",False),("display",False),("overflow",True))
        self.css_grab_tags_break_tag={"overflow":"hidden"}
        self.attribute_grab_tags=["aria-expanded","aria-hidden","outerHTML","aria-labelledby"]
        self.ambigious_css_values=['100%','auto','inherited']
        self.sibling_responsibilty_perform_function={
            'aria-labelledby':self.determine_arie_labelledby,
        }
        self.sibling_responsibilty_perform_function_format_response={
            'element_id':None,
        }

        #determine browser string for debugging
        if self.chrome:
            self.browser="Chrome"
        else:
            self.browser="Firefox"

        #determine viewport string for debugging
        if self.desktop:
            self.viewport='desktop'
        else:
            self.viewport='mobile'

        #initate driver
        if self.chrome:
            self.chrome=chrome_browser.ChromeBrowser(tier,desktop=self.desktop,debug=self.debug)
            self.driver=self.chrome.get_driver()
        else:
            self.firefox=firefox_browser.FirefoxBrowser(tier,desktop=self.desktop,debug=self.debug)
            self.driver=self.firefox.get_driver()

        #client specifications
        self.client_width,self.client_height=self.get_client_specifications()

        #set url
        self.url=self.webster.url

        #go to initial url
        self.go_to(self.url)

        #cookies
        if self.webster.cookies_set:
            self.session_id=webster.session_id
            self.load_cookies,self.save_cookies=self.webster.cookies_set
            self.cookies_file=str(self.url).split('.')[1]+"_"+str(self.session_id)+"_cookies.pkl"
            if self.load_cookies:
                self.load_all_cookies(url=self.url)
                self.go_to(self.url)

        #local storage
        self.linked_list_all_elements=html_element.linked_list(self.debug)

        #get all elements on url page
        self.get_all_elements_on_page()

    def get_client_specifications(self):
        if self.chrome:
            return self.chrome.get_client_specifications()
        else:
            return self.firefox.get_client_specifications()

    def scroll_items_drop_down(self):
        from selenium.webdriver.support.ui import Select
        '''value = "Your desired option's value"
        select_element = Select(driver.find_element_by_tag_name('select')
        for option in select_element.options:
            if option.get_attribute('value') == value:
                select_element.select_by_visible_text(option.text)'''

    def go_to(self, url):
        self.driver.get(url)
        '''def page_has_loaded():
            page_state = self.driver.execute_script(
                'return document.readyState;'
            )
            return page_state == 'complete'
        self.wait_for(page_has_loaded)'''
        self.debug.press(feed="{} has loaded successfully".format(url),tier=self.tier)

    def wait_for(self, condition_function):
        start_time = time.time()
        while time.time() < start_time + 3:
            if condition_function():
                return True
            else:
                time.sleep(0.1)
        raise Exception(
                'Timeout waiting for {}'.format(condition_function.__name__)
            )

    def scroll_element_view(self, element):
        try:
            self.driver.execute_script("return arguments[0].scrollIntoView(true);", element)
        except StaleElementReferenceException as Exception:
            debug.press(feed=str(Exception))

    def get_all_elements_on_page(self):
        elements = self.driver.find_elements_by_xpath("//*[not(*)]")[:25]
        for element in elements:
            try:
                self.scroll_element_view(element)
                if not element.tag_name in self.avoid_tag_names:
                    self.linked_list_all_elements.add_node(element,element_dictionary=self.get_element_dictionary(element))
            except StaleElementReferenceException:
                pass
            except NoSuchElementException:
                pass
        self.linked_list_all_elements.print_specifications()

    def is_retrieved_value_ambigious(self, retrieved_value):
        #verify that its not 100% or auto, etc
        if str(retrieved_value) in self.ambigious_css_values:
            return True
        return False

    def value_of_css_property_value_if_void(self,element,tag_tuple,trace=False):
        css,in_parent=tag_tuple
        while True:
            if element.tag_name in self.avoid_tag_names:
                if trace:
                    print("breaking {}".format(element.tag_name))
                break
            else:
                attr = element.value_of_css_property(css)
                if trace:
                    print("in_parent {}".format(in_parent))
                if trace:
                    print(attr)
                if in_parent:
                    if trace:
                        print("is in_parent value {}".format(attr == self.css_grab_tags_break_tag[css]))
                    if attr == self.css_grab_tags_break_tag[css]:
                        return attr
                elif not self.is_retrieved_value_ambigious(attr):
                    if trace:
                        print('returning {}'.format(attr))
                    return attr

            #Next parent element
            element = self.get_parent_of_element(element)
            if trace:
                print("parent retrieved, tag {}".format(element.tag_name))
        return None

    def determine_arie_labelledby(self, element, attribute):
        return None

    def get_attribute_if_void(self,element,attribute,trace=False):
        while True:
            if element.tag_name in self.avoid_tag_names:
                break
            if element.get_attribute(attribute) == None:
                element = self.get_parent_of_element(element)
            else:
                attr = element.get_attribute(attribute)
                return (element, attr)
        return None

    def get_element_dictionary(self, element):
        element_dictionary={}
        css_dict={}
        attribute_dict={}
        element_from_tuple=False
        aria_labelledby_dict={}

        #specs dictionary
        specifications_dictionary = self.driver.execute_script("return arguments[0].getBoundingClientRect()",element)

        for tag_tuple in self.css_grab_tags_tuples:
            css_dict.update({tag_tuple[0]:self.value_of_css_property_value_if_void(element,tag_tuple)})

        for attribute in self.attribute_grab_tags:
            var = self.get_attribute_if_void(element,attribute)
            if isinstance(var, tuple):
                element_from_tuple,var=var
            attribute_dict.update({attribute:var})

        for s,r in self.sibling_responsibilty_perform_function.items():
            if attribute_dict[s]:
                siblings=self.ask_parent_if_i_have_siblings(element_from_tuple)
                for sibling in siblings:
                    sibling_id = sibling.get_attribute('id')
                    if sibling_id == element_from_tuple.get_attribute(s):
                        attribute_dict.update({'dropdown-toggle':True})

        element_dictionary.update({'css_dictionary':css_dict})
        element_dictionary.update({'attribute_dictionary':attribute_dict})
        element_dictionary.update({'element_specifications':specifications_dictionary})
        element_dictionary.update({'xpath':self.determine_xpath(element)})

        return element_dictionary

    def report_test_result(self, selenium_object, pilot):
        self.linked_list_all_elements.add_report(selenium_object, pilot)

    def determine_xpath(self, element):
        tag_names=[]
        while True:
            elements = self.ask_parent_if_i_have_siblings(element)
            index=0
            for e in elements:
                if element==e:
                    break
                index+=1

            tag_names.append(element.tag_name)
            tag_names.append(index)
            element = self.get_parent_of_element(element)
            if element.tag_name == 'html':
                tag_names.append(element.tag_name)
                break
        xpath=''
        for tag in tag_names:
            xpath+=" \ "+str(tag)
        return xpath

    def inject_css(self, element, alteration):
        self.driver.execute_script("arguments[0].setAttribute('overflow', arguments[1]);",element,aleration)

    def highlight(self, element):
        """Highlights (blinks) a Selenium Webdriver element"""
        driver = element._parent
        original_style = element.get_attribute('style')
        def apply_new_style(s):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                    element, s
                )
        def apply_original_style():
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                    element, original_style
                )
        apply_new_style("background: red; border: 10px solid blue;")
        dictionary=self.webster.get_debug_prompt_parameter(
                function_to_call=apply_original_style,
                question_to_ask="Error? (True of False)",
            )
        dictionary=self.debug.press(feed=dictionary, prompt=True,tier=self.tier)
        self.webster.perform_response(dictionary=dictionary)

    def replace_element(self, element):
        next_sibling = driver.execute_script("""
                return arguments[0].nextElementSibling
            """, element)
        return next_sibling

    def get_parent_of_element(self,element):
        return element.find_element_by_xpath('..')

    def load_all_cookies(self,url):
        self.debug.press(feed='Loading cookies for {}'.format(str(str(self.url)+" "+str(self.session_id))),tier=self.tier)
        cookies = pickle.load(open(self.cookies_file,"rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
            self.debug.press(feed=str(cookie),tier=self.tier+1)
        self.debug.press(feed='Cookies loaded',tier=self.tier)

    def save_all_cookies(self):
        num=0
        while True:
            num+=1
            print(num)
            try:
                if num>3:
                    raise FileNotFoundError
                pickle.dump(self.driver.get_cookies(),open(self.cookies_file,"wb"))
                break
            except FileNotFoundError:
                file = open(self.cookies_file, "w+")
                file.close()
                self.save_all_cookies()

    def ask_parent_if_i_have_siblings(self,element):
        parent_element=self.get_parent_of_element(element)
        return parent_element.find_elements_by_xpath('.//*')
