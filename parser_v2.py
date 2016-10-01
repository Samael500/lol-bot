# -*- coding: utf-8 -*-

import time
import pyglet

from random import choice
from splinter import Browser
from selenium.webdriver.common.keys import Keys

from .secret import LOGIN_DATA


class Visitor(object):

    """ Visit page and check new orders """

    browser_name = 'chrome'
    LOGIN_URL = 'https://booster.lol-eloboosting.com/'
    CHECK_URL = 'https://booster.lol-eloboosting.com/dashboard_booster'


    def __init__(self):
        self.browser = Browser(self.browser_name)

    def wait(self):
        time.sleep(3)

    def wait_check(self):
        """ Prevent CloudFlare DDOS protect """
        while 'Checking your browser before accessing' in self.browser.find_by_css("body").text:
            self.wait()

    def autorization(self):
        """ open login page and post credentials """
        self.browser.visit(LOGIN_URL)
        self.wait_check()
        self.browser.fill_form(LOGIN_DATA)
        self.browser.find_by_css('button.btn.btn-block').click()

    def dashboard(self):
        """ open dashboard page and check orders """
