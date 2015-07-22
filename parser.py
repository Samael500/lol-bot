# -*- coding: utf-8 -*-

# settings section -----------------------------------------------------------

LOGIN_URL = 'http://booster.lol-eloboosting.com/'
CHECK_URL = 'http://booster.lol-eloboosting.com/dashboard_booster'
# CHECK_URL = 'file:///home/maks/s50/arturka/page.html'

MUSIC_PATH = 'alarm.wav'

TIMEOUT = 5, 65

LOGIN_DATA = {'email': 'arturka77703@yandex.ru', 'pwd': 'assass1nicctrmsn'}

# ----------------------------------------------------------------------------

import pyglet
from splinter import Browser
import time
from random import randint


def beep():
    sound = pyglet.media.load(MUSIC_PATH)
    sound.play()

    def exiter(dt):
        pyglet.app.exit()

    pyglet.clock.schedule_once(exiter, sound.duration + 1)
    pyglet.app.run()

def status_message(orders):
    print 'Active orders: %d' % orders


if __name__ == '__main__':

    try:
        browser = Browser('chrome')
        # autorization
        browser.visit(LOGIN_URL)
        browser.fill_form(LOGIN_DATA)
        browser.find_by_css('button.btn.btn-block').click()
        # active orders counter
        orders = 0

        while True:  # run check
            try:
                browser.visit(CHECK_URL)
                # find elements and check count
                tr_list = browser.find_by_css('#tSortable_active_order tbody').first.find_by_tag('tr')
                tr_list_len = len(tr_list)
                no_data = 'No data available in table' in tr_list[0].text 
                active_orders = tr_list_len if not no_data else 0
                if active_orders > orders:
                    beep()
                # set orders as new value
                orders = active_orders
                status_message(orders)
                time.sleep(randint(*TIMEOUT))
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as err:
                print 'ERROR:', err.message

    except (KeyboardInterrupt, SystemExit):
        print 'EXIT'
    finally:
        browser.quit()
        pyglet.app.exit()


# pip install splinter
# pip install Pyglet
