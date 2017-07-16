# -*- coding: utf-8 -*-

import sys
import traceback
import time
import pyglet
import datetime

from random import choice
from splinter import Browser
from selenium.webdriver.common.keys import Keys

from secret import LOGIN_DATA


is_js_loaded = "document.readyState === 'complete';"

class Visitor(object):

    """ Visit page and check new orders """

    browser_name = 'chrome'
    LOGIN_URL = 'https://boost-center.com/login'
    CHECK_URL = 'https://boost-center.com/dashboard_booster.html'
    NOLIMIT_CHECK_URL = 'https://boost-center.com/dashboard_booster/active_orders_refresh'
    MUSIC_PATH = 'alarm.wav'
    QUELONG = 5  # 10

    def __init__(self):
        self.browser = Browser(self.browser_name)
        self.browser.driver.set_page_load_timeout(15)
        self.orders = 0
        self.sessions = [None] * self.QUELONG
        self.current_session = 0

    def wait(self, timeout=3):
        time.sleep(timeout)

    def visit(self, url):
        """ Open page in browser and prewent wait_check """
        self.browser.visit(url)
        while 'Checking your browser before accessing' in self.browser.html:
            # Prevent CloudFlare DDOS protect
            self.wait()
        if '<h1>Booster dashboard. Sign In</h1>' in self.browser.html and url != self.LOGIN_URL:
            self.autorization()
            return self.visit(url)
        self.wait(.5)

    def beep(self):
        """ Run allarm beep """
        sound = pyglet.media.load(self.MUSIC_PATH)
        sound.play()

        def exiter(dt):
            pyglet.app.exit()

        pyglet.clock.schedule_once(exiter, sound.duration + 1)
        pyglet.app.run()

    def autorization(self):
        """ open login page and post credentials """
        self.visit(self.LOGIN_URL)
        self.browser.fill_form(LOGIN_DATA)
        self.browser.find_by_css('button.btn.btn-block').click()
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        msg = '\n{} Log in'.format(now)
        print (msg)

    def dashboard(self):
        """ open dashboard page and check orders """
        self.visit(self.NOLIMIT_CHECK_URL)
        while not self.browser.evaluate_script(is_js_loaded):
            self.wait(.1)
        # tSortable_active_order
        tr_list = self.browser.find_by_css('#tSortable_test_order tbody').first.find_by_tag('tr')
        tr_list_len = max([len(tr_list), 0])
        no_data = 'No data available in table' in tr_list[0].text if tr_list_len else True
        active_orders = tr_list_len if not no_data else 0
        if active_orders > self.orders:
            self.beep()
            # self.visit(self.CHECK_URL)
            # self.wait(15)
        # set orders as new value
        self.orders = active_orders
        self.log(self.orders)

    def log(self, orders):
        """ Simple log to print output """
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        msg = '\r{} active orders: {:3d}'.format(now, orders)
        sys.stdout.write(msg)
        sys.stdout.flush()

    def run(self):
        """ Login and check """
        self.autorization()
        while True:
            self.dashboard()

    def tear_down(self):
        """ Safe exit """
        self.browser.quit()
        pyglet.app.exit()


if __name__ == '__main__':
    try:
        while True:
            try:
                vis = Visitor()
                vis.run()
            except (KeyboardInterrupt, SystemExit):
                print '\nEXIT'
                raise
            except Exception as err:
                print '\nERROR:', err, err.message
                traceback.print_exc()
            finally:
                vis.tear_down()
    except (KeyboardInterrupt, SystemExit):
        pass
