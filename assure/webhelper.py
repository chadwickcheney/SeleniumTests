from selenium.webdriver.common.keys import Keys

class WebHelper:
    def __init__(self,driver):
        self.driver=driver
        self.head_window = self.driver.current_window_handle

    def open_new_tab_switch_focus(self,url):
        self.driver.execute_script("window.open('"+str(url)+"', 'new_window')")
        self.driver.switch_to_window(self.driver.window_handles[len(self.driver.window_handles)-1])

    def switch_focus_main_window(self):
        self.driver.switch_to_window(self.head_window)
