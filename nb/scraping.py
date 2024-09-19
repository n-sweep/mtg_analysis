# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.16.2
#   kernelspec:
#     display_name: Python3
#     language: python
#     name: Python3
# ---

# %%
import os
import sqlite3
import numpy as np
import pandas as pd
import plotly.io as pio
import requests
import time

import bs4
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
# import plotly.express as px
from util import Crawler

# plotly setup
pio.renderers.default = 'notebook'
pd.options.plotting.backend = 'plotly'

def pwrite(fig, plt='/tmp/vis/plot.json'):
    fig = fig.update_layout(autosize=False)
    fig.write_json(plt)

# %% [markdown]
# # Template Notebook
# https://www.mtggoldfish.com/

# %%
with sqlite3.connect('./mtggf.db') as con:
    res = con.execute("select * from pages where slug like '/deck%' limit 1")
    pages = res.fetchall()

# %%
pages[0][0]

# %%
soup.find('h4', class_="price-card-purchase-header")

# %%
soup = bs(pages[0][1], 'html.parser')
deck = soup.find('div', class_='deck-container')

# %%
# process header
header = deck.find('div', class_='header-container')

title = header.find('h1', class_='title').text.replace('\n', ' ').strip()
pilot = header.find('span', class_='author').text.replace('\n', ' ').strip()
title = title.replace(pilot, '').strip()
pilot = pilot.replace('by ', '')
price = header.find('div', class_='paper').text.replace('\xa0', '').strip()
rarity = header.find('div', class_='header-prices-rarity')
rarity = rarity.text.replace('\xa0', ' ').strip().split(',')
rarity = {label: int(count) for count, label in (r.strip().split(' ') for r in rarity) }

title, pilot, rarity, price

# %%
# process meta info
meta = []
br = soup.new_tag('br')

info = deck.find('p', class_='deck-container-information')
children = [c for c in info.children if c.text != '\n']

while True:
    if br in children:
        i = children.index(br)
        slice = children[:i]
        if slice:
            meta.append(slice)
        children = children[i+1:]
    else:
        meta.append(children)
        break

format = meta[0][0].text.strip().split(': ')[1]
record = meta[1][2].strip(' ,\n').split(',')
place = record[0] if len(record) > 1 else None
record = record[1] if place else record[0]
event_name = meta[1][1].text
event_slug = meta[1][1]['href']
deck_source = meta[2][1]['href']
archetype = meta[4][1].text
archetype_slug = meta[4][1]['href']

# %%
# process decklist
decklist = deck.find('div', class_='deck-table-container')
items = []
for table in decklist.find_all('table'):
    items += table.find_all('tr')

# %%
data = items[1].find_all('td')

# %%
cards = []
board = 'mainboard'
for item in items:

    if 'deck-category-header' in item.get('class', []):
        if 'sideboard' in item.text.lower():
            board = 'sideboard'
        continue

    card_a = item.find('span', class_='card_id').a
    card_data = item.find_all('td')

    count = int(card_data[0].text.strip())

    cards.append((
        card_a.text,
        count,
        board,
        card_a['data-card-id'],
        card_a['href']
    ))

# %%
cards

# %%
deck_table = soup.find('div', class_='deck-table-container')
deck_table.find_all('tr')

# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
