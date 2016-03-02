# -*- coding: utf-8 -*-

# settings section -----------------------------------------------------------

LOGIN_URL = 'http://booster.lol-eloboosting.com/'
CHECK_URL = 'http://booster.lol-eloboosting.com/dashboard_booster'
# LOGIN_URL = 'file:///home/maks/s50/arturka/boost/Login booster - Lol-eloboosting.com.html'
# CHECK_URL = 'file:///home/maks/s50/arturka/boost/Dashboard booster - Lol-eloboosting.html'

MUSIC_PATH = 'alarm.wav'

TIMEOUT = 1, 2

QUELONG = 7

LOGIN_DATA = {'email': 'arturka77703@yandex.ru', 'pwd': 'assass1nicctrmsn'}


# ----------------------------------------------------------------------------

import time
import pyglet

from random import randint
from splinter import Browser
from selenium.webdriver.common.keys import Keys


def sleep():
    time.sleep(randint(*TIMEOUT))

def beep():
    sound = pyglet.media.load(MUSIC_PATH)
    sound.play()

    def exiter(dt):
        pyglet.app.exit()

    pyglet.clock.schedule_once(exiter, sound.duration + 1)
    pyglet.app.run()

def status_message(orders):
    print 'Active orders: %d' % orders


class BoostBot(object):

    """ Manage browser sesion and look to orders """

    BROWSER = 'chrome'
    # BROWSER = 'firefox'

    def killalert(self):
        try:
            self.browser.get_alert().accept()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            pass

    def __init__(self):
        self.browser = Browser(self.BROWSER)
        self.orders = 0
        self.autorization()
        for i in range(QUELONG):
            if i:
                self.new_tab()
            self.browser.visit(CHECK_URL)
            self.killalert()
            sleep()

    def autorization(self):
        """ open login page and post credentials """
        self.browser.visit(LOGIN_URL)
        sleep()
        self.browser.fill_form(LOGIN_DATA)
        sleep()
        self.browser.find_by_css('button.btn.btn-block').click()
        sleep()

    def next(self):
        """ Go to next tab """
        self.browser.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)

    def new_tab(self):
        """ Open a new tab in browser """
        self.browser.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')

    def close_tabs(self):
        """ Close tabs in browser """
        self.browser.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.SHIFT + 'w')

    def check(self):
        for i in range(QUELONG):
            self.check_orders()
            sleep()
            self.next()

    def check_orders(self):
        """ visit profile page url and check orders is change """
        self.browser.reload()
        self.killalert()
        # find elements and check count
        tr_list = self.browser.find_by_css('#tSortable_active_order tbody').first.find_by_tag('tr')
        tr_list_len = len(tr_list)
        no_data = 'No data available in table' in tr_list[0].text 
        active_orders = tr_list_len if not no_data else 0
        if active_orders > self.orders:
            beep()
        # set orders as new value
        self.orders = active_orders
        status_message(self.orders)

    def tear_down(self):
        """ Safe exit """
        self.close_tabs()
        self.browser.quit()
        pyglet.app.exit()


if __name__ == '__main__':

    try:
        while True:
            bot = BoostBot()
            try:
                while True:  # run check
                    bot.check()
            except (KeyboardInterrupt, SystemExit):
                print 'EXIT'
                raise
            except Exception as err:
                print 'ERROR:', err, err.message
            finally:
                bot.tear_down()

    except (KeyboardInterrupt, SystemExit):
        pass

# pip install splinter
# pip install Pyglet
