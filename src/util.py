import random
import sqlite3
import time

from selenium import webdriver


def create_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', options=options)

    print('webdriver connected.')
    return driver


def load_db(db_loc):
    with sqlite3.connect(db_loc) as con:
        res = con.execute("select slug, html from pages")
        pages = dict(res.fetchall())

        print('database loaded.')
        return pages


def random_wait():
    # random wait between 0.25 and 0.75
    time.sleep(0.25 + (random.random() * 0.5))
