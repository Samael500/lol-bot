# -*- coding: utf-8 -*-

import time
import pyglet

from random import choice
from splinter import Browser
from selenium.webdriver.common.keys import Keys

from secret import LOGIN_DATA


class Visitor(object):

    """ Visit page and check new orders """

    browser_name = 'chrome'
    LOGIN_URL = 'https://booster.lol-eloboosting.com/login.html'
    CHECK_URL = 'https://booster.lol-eloboosting.com/dashboard_booster'
    MUSIC_PATH = 'alarm.wav'

    def __init__(self):
        self.browser = Browser(self.browser_name)
        self.orders = 0

    def wait(self, timeout=3):
        time.sleep(timeout)

    def visit(self, url):
        """ Open page in browser and prewent wait_check """
        self.browser.visit(url)
        while 'Checking your browser before accessing' in self.browser.html:
            # Prevent CloudFlare DDOS protect
            self.wait()
        if 'You refreshed too many times' in self.browser.html:
            # Prevent LOL DDOS protect
            self.wait(7)
            return self.visit(url)
        self.wait(1)

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

    def dashboard(self):
        """ open dashboard page and check orders """
        self.visit(self.CHECK_URL)
        if not 'tSortable_active_order' is self.browser.html:
            return
        tr_list = self.browser.find_by_css('#tSortable_active_order tbody').first.find_by_tag('tr')
        tr_list_len = len(tr_list)
        no_data = 'No data available in table' in tr_list[0].text
        active_orders = tr_list_len if not no_data else 0
        if active_orders > self.orders:
            beep()
        # set orders as new value
        self.orders = active_orders
        self.log(self.orders)

    def log(orders):
        """ Simple log to print output """
        print 'Active orders: {}'.format(orders)

    def run(self):
        """ Login and check """
        self.autorization()
        while True:
            self.dashboard()

if __name__ == '__main__':
    vis = Visitor()
    vis.run()
