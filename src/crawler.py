import bs4
import os
import requests
import sqlite3

from bs4 import BeautifulSoup as bs
from util import create_driver, load_db, random_wait

BASE_URL = "https://www.mtggoldfish.com"


class Crawler:
    def __init__(self, db_loc):
        self.db_loc = db_loc
        self.driver = create_driver()
        self.pages = load_db(db_loc)


    def _make_request(self, endpoint: str, params: dict) -> bytes|str:
        """Make a base get requests using `requests` library

        Parameters
        ----------
        endpoint
            the endpoint (appended to BASE_URL) to be requested
        params
            arguments to be passed to the request

        Returns
        -------
        string containing page html (or empty string if not found)
        """

        output = ''
        url = os.path.join(BASE_URL, endpoint.strip('/'))

        if endpoint.startswith('/deck'):
            print('requesting with selenium...')
            self.driver.get(url)
            output = self.driver.page_source

        else:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                output = response.content

        random_wait()

        return output


    def make_request(self, endpoint: str, params: dict = {}) -> bs4.BeautifulSoup:
        """Check the database for existing html on a given endpoint; request via
        selenium for deck pages

        Parameters
        ----------
        endpoint
            the endpoint (appended to BASE_URL) to be requested
        params
            arguments to be passed to the request

        Returns
        -------
        BeautifulSoup object from the resulting html string
        """

        if params.get('commit') == 'Search':
            print('searching...')
            html = self._make_request(endpoint, params)

        elif endpoint in self.pages:
            print(f'{endpoint} found in database')
            html = self.pages[endpoint]

        else:
            print(f'requesting {endpoint}...')
            html = self._make_request(endpoint, params)

            if html is not None:
                with sqlite3.connect(self.db_loc) as con:
                    con.execute("INSERT INTO pages (slug, html) VALUES (?, ?)", (endpoint, html))
                    con.commit()
                print(f'{endpoint} saved')

        return bs(html, 'html.parser')


    def tournament_search(self, format: str, date_range: str, page: int) -> bs4.BeautifulSoup:
        """Create a search for a list of tournaments within a date range

        Parameters
        ----------
        format
            the format of tournament to search for
        date_range
            example: "09/01/2024 - 09/14/2024"
        page

        Returns
        -------
        BeautifulSoup object from the resulting html string
        """

        args = {
            "commit": "Search",
            "page": page,
            "tournament_search[date_range]": date_range,
            "tournament_search[format]": format,
            "utf8": "✔",
        }

        return self.make_request('tournament_searches/create', args)


    def collect_tournament_links(self, format: str, date_range: str) -> dict:
        """Scrape all pages of tournament links for a given format, date range

        Parameters
        ----------
        format
            the format of tournament to search for
        date_range
            example: "09/01/2024 - 09/14/2024"

        Returns
        -------
        """
        page = 0
        data = {}
        while True:
            page += 1
            soup = self.tournament_search(format, date_range, page)
            table = soup.find('table', class_='table-striped')

            if not table:
                print('finished')
                break

            print(f'scraping page {page}...')

            for row in table.find_all('tr')[1:]:
                link = row.find('a')
                href = link['href']
                data[href] = link.text.strip()

        return data


    def collect_deck_links(self, tournaments: list) -> list:
        """
        Parameters
        ----------
        tournaments
            list of url endpoints of a tournament

        Returns
        -------
        list of links to all decks in given tournament
        """
        decks = []
        for slug in tournaments:
            soup = self.make_request(slug)
            table = soup.find('table', attrs={'class': 'table-tournament'})

            for row in table.find_all('tr')[1:]:
                a = row.find('a')
                if a:
                    decks.append(a['href'])

        return decks


    def collect_all_tournament_decks(self, format: str, date_range: str) -> dict:
        output = {}
        tournaments = self.collect_tournament_links(format, date_range)
        decks = self.collect_deck_links(list(tournaments))
        for slug in decks:
            soup = self.make_request(slug)
            output[slug] = str(soup)

        return output
