# -*- coding: utf-8 -*-


def frange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

# settings section -----------------------------------------------------------

LOGIN_URL = 'https://booster.lol-eloboosting.com/'
CHECK_URL = 'https://booster.lol-eloboosting.com/dashboard_booster'
# LOGIN_URL = 'file:///home/maks/s50/arturka/boost/Login booster - Lol-eloboosting.com.html'
# CHECK_URL = 'file:///home/maks/s50/arturka/boost/Dashboard booster - Lol-eloboosting.html'


TIMEOUT = list(frange(1, 3, .3))
FAST_SLEEP = list(frange(1.1, 2.7, .03))
LONG_SLEEP = list(frange(7.5, 10.7, .2))

QUELONG = 10


# ----------------------------------------------------------------------------

import time
import pyglet

from random import choice
from splinter import Browser
from selenium.webdriver.common.keys import Keys


def long_sleep():
    time.sleep(choice(LONG_SLEEP))


def sleep():
    time.sleep(choice(TIMEOUT))


def fast_sleep():
    time.sleep(choice(FAST_SLEEP))


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

    CHROME = 'chrome'
    FIREFOX = 'firefox'

    def killalert(self):
        try:
            self.browser.get_alert().accept()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            pass

    def __init__(self):
        self.browser = Browser(self.CHROME)
        self.orders = 0
        self.cookies = []
        for index in range(QUELONG):
            self.new_tab(index)
            fast_sleep()

    def wait_redirect(self, do_sleep=True):
        if do_sleep:
            sleep()
        while 'Checking your browser before accessing' in self.browser.find_by_css("body").text:
            sleep()

    def autorization(self):
        """ open login page and post credentials """
        self.browser.visit(LOGIN_URL)
        self.wait_redirect(False)
        self.browser.fill_form(LOGIN_DATA)
        self.wait_redirect(False)
        self.browser.find_by_css('button.btn.btn-block').click()
        self.wait_redirect(False)

    def next(self, index):
        """ Go to next tab """
        self.browser.cookies.delete()
        self.browser.cookies.add(self.cookies[index])
        # check orders and upd cookies
        self.check_orders()

    def new_tab(self, index):
        """ Open a new tab in browser """
        # login
        if index:
            self.browser.cookies.delete()
            self.browser.cookies.add({
                'cf_clearance': self.cookies[0]['cf_clearance'], '__cfduid': self.cookies[0]['__cfduid']})
            # self.browser.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
            # self.browser.windows.current = self.browser.windows[index]
        self.autorization()
        self.cookies.append(self.browser.cookies.all())
        sleep()
        self.killalert()

    def check(self):
        for index in range(QUELONG):
            self.next(index)
            fast_sleep()

    def check_orders(self):
        """ visit profile page url and check orders is change """
        self.browser.reload()
        self.wait_redirect(False)
        self.killalert()

        attempts = 5

        text = self.browser.find_by_css("body").text
        while 'You refreshed too many times' in text:  # or '#tSortable_active_order tbody' not in text:
            sleep()
        #     self.browser.reload()
        #     text = self.browser.find_by_css("body").text

        #     attempts -= 1
        #     if not attempts:
        #         raise Exception('Not found on page')

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
