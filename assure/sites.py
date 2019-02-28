from . import debug
import time
from abc import ABCMeta, abstractmethod

class Site:
    def __init__(self,driver,debug,tier,webster):
        self.driver=driver
        self.debug=debug
        self.tier=tier
        self.webster=webster
        self.check_modal_dictionary={
                'controlledchaoshair':self.controlledchaoshair_modal_exists,
                'beardedgoat':self.beardedgoat_modal_exists,
            }

        #site tests
        self.test_dictionary={}

    #COMMENCE TEST
    def unit_test(self):
        print("web tests")
        tests = [self.check_modal_functionality,self.viewport_meta_tag_exists,self.facebook_pixel_exists]
        for test in tests:
            self.debug.press(feed='Running test {}'.format(test.__name__),tier=self.tier+1)
            self.test_dictionary.update({test.__name__:test()})
        return self.test_dictionary

    def check_modal_functionality(self):
        return self.get_modal_response(self.webster.url)

    def viewport_meta_tag_exists(self):
        elements = self.driver.find_elements_by_xpath("//*[not(*)]")
        for element in elements:
            if 'meta name="viewport" content="width=device-width, initial-scale' in element.get_attribute('outerHTML'):
                return True
        return False

    def facebook_pixel_exists(self):
        elements = self.driver.find_elements_by_xpath("//*[not(*)]")
        for element in elements:
            if 'https://connect.facebook.net/' in str(element.get_attribute('outerHTML')):
                return True
        return False

    def get_modal_response(self,url):
        for key,value in self.check_modal_dictionary.items():
            if key in url:
                return value()

    def controlledchaoshair_modal_exists(self):
        dictionary={
                'email_location_method':self.driver.find_element_by_class_name,
                'email_element_identifier':'privy-email-input',
                'email_element_submit_method':self.driver.find_element_by_id,
                'email_element_submit_identifier':'privy-submit-btn',
                'modal_close_method':self.driver.find_element_by_class_name,
                'modal_close_identifier':'privy-dismiss-content',
            }
        controlledchaoshair=ControlledChaosHair(self.driver,dictionary)
        return controlledchaoshair.response_dictionary

    def beardedgoat_modal_exists(self, driver):
        pass

#MODAL ABSTRACT class
class AbstractModalFunctionality:
    def __init__(self,driver,dictionary):
        self.driver=driver
        self.dictionary=dictionary
        self.response_list=[
                self.activate,
                self.exists,
                self.email_keys,
                self.email_submit,
                self.close,
            ]
        self.response_dictionary={}
        self.act()

    @abstractmethod
    def act(self):
        print("On Abstract Function {}".format(self.act.__name__))
        for m in self.response_list:
            var = m()
            self.response_dictionary.update({m.__name__:var})
            if not var:
                break

    @abstractmethod
    def activate(self):
        print("On Abstract Function {}".format(self.activate.__name__))
        time.sleep(2)
        return True

    @abstractmethod
    def exists(self):
        print("On Abstract Function {}".format(self.exists.__name__))
        return bool(self.dictionary['email_location_method'](self.dictionary['email_element_identifier']))

    @abstractmethod
    def email_keys(self):
        print("On Abstract Function {}".format(self.email_keys.__name__))
        self.dictionary['email_location_method'](self.dictionary['email_element_identifier']).send_keys('john@gmail.com')
        if self.dictionary['email_location_method'](self.dictionary['email_element_identifier']).get_attribute('value'):
            return True
        return False


    @abstractmethod
    def email_submit(self):
        print("On Abstract Function {}".format(self.email_submit.__name__))
        e = self.dictionary['email_element_submit_method'](self.dictionary['email_element_submit_identifier']).click()
        if e:
            return True
        return False

    @abstractmethod
    def close(self):
        print("On Abstract Function {}".format(self.close.__name__))
        e = self.dictionary['modal_close_method'](self.dictionary['modal_close_identifier']).click()
        if e:
            return True
        return False


class ControlledChaosHair(AbstractModalFunctionality):
    def __init__(self,driver,dictionary):
        self.driver=driver
        self.dictionary=dictionary
        self.response_dictionary={}
        self.response_list=[
                self.activate,
                self.exists,
                self.email_keys,
                self.email_submit,
                self.close,
            ]
        self.act()

    def act(self):
        print("On Function {}".format(self.act.__name__))
        super().act()

    def activate(self):
        print("On Function {}".format(self.activate.__name__))
        super().activate()

    def exists(self):
        print("On Function {}".format(self.exists.__name__))
        super().exists()

    def email_keys(self):
        print("On Function {}".format(self.email_keys.__name__))
        super().email_keys()

    def email_submit(self):
        print("On Function {}".format(self.email_submit.__name__))
        super().email_submit()

    def close(self):
        print("On Function {}".format(self.close.__name__))
        super().close()











'''class ControlledChaosHair:
    def __init__(self,driver):
        self.driver=driver
        self.dictionary={
                'email_location_method':self.driver.find_element_by_class_name,
                'email_element_identifier':'privy-email-input',
                'email_element_submit_method':self.driver.find_element_by_id,
                'email_element_submit_identifier':'privy-submit-btn',
                'modal_close_method':self.driver.find_element_by_class_name,
                'modal_close_identifier':'privy-dismiss-content',
            }

        self.response_list=[
                self.activate,
                self.exists,
                self.email_keys,
                self.email_submit,
                self.close,
            ]

        self.response_dictionary={}

        self.act()

    def act(self):
        for m in self.response_list:
            var = m()
            self.response_dictionary.update({m.__name__:var})
            if not var:
                break

    def activate(self):
        time.sleep(2)
        return True

    def exists(self):
        return bool(self.dictionary['email_location_method'](self.dictionary['email_element_identifier']))

    def email_keys(self):
        self.dictionary['email_location_method'](self.dictionary['email_element_identifier']).send_keys('john@gmail.com')
        if self.dictionary['email_location_method'](self.dictionary['email_element_identifier']).get_attribute('value'):
            return True
        return False


    def email_submit(self):
        e = self.dictionary['email_element_submit_method'](self.dictionary['email_element_submit_identifier']).click()
        if e:
            return True
        return False

    def close(self):
        e = self.dictionary['modal_close_method'](self.dictionary['modal_close_identifier']).click()
        if e:
            return True
        return False


class BeardedGoat:
    def __init__(self,driver):
        self.driver=driver
        self.dictionary={
                'email_location_method':self.driver.find_element_by_xpath,
                'email_element_identifier':'/html/body/div[3]/div/div/div/div/div/div[2]/div/div/input',
                'email_element_submit_method':self.driver.find_element_by_xpath,
                'email_element_submit_identifier':'/html/body/div[3]/div/div/div/div/div/div[3]/div/button',
                'modal_close_method':self.driver.find_element_by_xpath,
                'modal_close_identifier':'privy-dismiss-content',
            }

        self.response_list=[
                self.activate,
                self.exists,
                self.email_keys,
                self.email_submit,
                self.close,
            ]

        self.response_dictionary={}

        self.act()

        def act(self):
        for m in self.response_list:
            var = m()
            self.response_dictionary.update({m.__name__:var})
            if not var:
                break

        def activate(self):
            time.sleep(2)
            return True

        def exists(self):
            return bool(self.dictionary['email_location_method'](self.dictionary['email_element_identifier']))

        def email_keys(self):
            self.dictionary['email_location_method'](self.dictionary['email_element_identifier']).send_keys('john@gmail.com')
            if self.dictionary['email_location_method'](self.dictionary['email_element_identifier']).get_attribute('value'):
                return True
            return False


        def email_submit(self):
            e = self.dictionary['email_element_submit_method'](self.dictionary['email_element_submit_identifier']).click()
            if e:
                return True
            return False

        def close(self):
            e = self.dictionary['modal_close_method'](self.dictionary['modal_close_identifier']).click()
            if e:
                return True
            return False'''
