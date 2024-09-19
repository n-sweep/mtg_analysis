from src.crawler import Crawler

DB_LOC = "./data/mtggf.db"


def main():
    agent = Crawler()
    format = 'legacy'
    date_range = "09/01/2024 - 09/17/2024"
    data = agent.collect_all_tournament_decks(format, date_range)

    agent.driver.quit()


if __name__ == '__main__':
    main()
