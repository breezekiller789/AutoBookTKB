# !/usr/bin/python
# -*-coding:utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Pool
import io

# TODO:
#     在做選課的時候，用類似stack的方式呼叫，先呼叫最後一個也就是select_session
#     ，然後這樣就好，然後select_session一進去就往上呼叫，叫select_date()，依此類推
#     這樣試試看，因為那個網路異常的alert隨時會出現，所以如果萬一我在某一個phase
#     出現alert，然後我沒有去listen他，機器人就會卡在那邊，所以每一個function一進去
#     都先try，就做正常的事情看看，如果有問題，丟exception，然後return False回去上
#     給父親，然後父親就是while loop一直去做，直到他兒子return True為止，這樣試試看。

class AutoBookTKB:

    def __init__(self, settings):
        import json
        with io.open(settings, 'r', encoding="utf-8") as fp:
            self.settings = json.load(fp)
        with io.open('locationList.json', 'r', encoding="utf-8") as fp:
            self.location_list = json.load(fp)
        fp.close()

        opts = webdriver.ChromeOptions()
        # if you're running as root, you'll need these code
        #opts.binary_location = './chromedriver'
        #opts.headless = True
        #opts.add_argument('--no-sandbox')
        #opts.add_argument('--disable-dev-shm-usage')
        #opts.add_argument('--remote-debugging-port=9222')
        #opts.add_argument('--headless')
        #opts.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=opts)
        self.driver.get("https://bookseat.tkblearning.com.tw/book-seat/student/bookSeat/index")

        self.wait = WebDriverWait(self.driver, 60)

    def login(self):
        try:
            element = self.driver.find_element_by_id("id")
            element.clear()
            element.send_keys(self.settings['id'])

            element = self.driver.find_element_by_id("pwd")
            element.clear()
            element.send_keys(self.settings['password'])

            self.click_send()

            self.accept_alerts()
            return True
        except Exception:
            return False

    def click_send(self):
        element = self.driver.find_element_by_link_text(u"送出")
        element.click()

    def wait_until_noon_or_midnight(self):
        import datetime, time
        midnight = datetime.datetime.replace(
            datetime.datetime.now() + datetime.timedelta(days=1),
            hour=0, minute=0, second=0)

        noon = datetime.datetime.now().replace(hour=12, minute=0, second=0)

        now = datetime.datetime.now()

        delta = noon - now
        if delta.days < 0: # It's afternoon now, wait until midnight.
            delta = midnight - now

        print("Current time : " + time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Sleep for " + str(delta.seconds) + " seconds..."
            "do not close this window and the web driver.")
        time.sleep(delta.seconds)

    def refresh(self):
        """Refresh current page."""
        self.driver.refresh()

    def select_class(self):
        element = self.driver.find_element_by_id("class_selector")
        element.click()
        Select(element).select_by_index(self.settings['classIndex'])
        element.click()

    def send_securitycode(self):
        element = self.driver.find_element_by_id("userinputcode")
        element.click()
        element.clear()
        code = self.driver.execute_script("return SecurityCode;")
        element.send_keys(code)

    def select_location(self):
        location_value = self.location_list[self.settings['location']]
        element = self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "option[value=%s]" % location_value
            ))
        )
        element = self.driver.find_element_by_id("branch_selector")
        element.click()
        Select(element).select_by_value(location_value)
        element.click()

    def select_date(self):
        """Select the newest date."""
        import datetime
        date = datetime.date.today() + datetime.timedelta(days=6)

        element = self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "option[value='%d-%02d-%02d']" % (date.year, date.month,
                                                  date.day)
            ))
        )
        element = self.driver.find_element_by_id("date_selector")
        element.click()
        Select(element).select_by_value(str(date))
        element.click()

    def select_sessions(self):
        element = self.wait.until(
            EC.presence_of_element_located((By.ID, "session_time_div"))
        )
        element = self.driver.find_element_by_name("session_time")
        for i in self.settings['sessions']:
            if self.driver.find_elements_by_xpath('//input[@value="%d"]' % i):
                self.driver.find_element_by_xpath('//input[@value="%d"]' % i).click()

    def accept_alerts(self):
        """Keep accepting alerts until there's a result."""
        while self.wait.until(EC.alert_is_present()):
            if self.accept_one_alert():
                break

    def accept_one_alert(self):
        alert = self.driver.switch_to_alert()
        print('**' + alert.text + '**')

        mylist = [u'上次登入IP', u'已滿', u'請勾選場次時間', u'預約成功', u'請選擇', u'異常', u'確定預約第1場次?'
                  ,u'確定預約第2場次?', u'確定預約第3場次?', u'確定預約第4場次?'
                  ,u'網路發生異常,請重新整理！_',u'請勾選場次時間，謝謝!!']
        for s in mylist:
            # if s is u'網路發生異常,請重新整理！_':
            #     self.refresh()
            #     return True
            # if s in u'請勾選場次時間，謝謝!!':
            #     print("場次已滿，無法勾選 " + self.settings['sessions'])
            #     return True
            if s in alert.text:
                break
        else:
            return False

        alert.accept()
        return True

    def main(self):
        print("Mission started...")
        # self.wait_until_noon_or_midnight()
        while not self.login():
            self.refresh()

        # try:
        #     self.refresh()
        # except Exception:
        #     pass

        for _ in range(10):
            try:
                self.select_class()
                self.select_date()
                #self.send_securitycode()
                self.select_location()
                self.select_sessions()
                self.click_send()
                self.accept_alerts()
                break
            except Exception:
                time.sleep(1)
        print("Task completed. Plese check your booking:)")


if __name__ == '__main__':
    atb = AutoBookTKB('AutoBookTKB-settings.json')
    atb.main()

