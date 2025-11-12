__author__ = "Baris"
__version__ = 1.0
__doc__ = """
This is a program to fetch the weather information of given cities and store it in a database called weather.db.
city names and languages can be imported from a json file
"""


import logging.config
import config as cfg
from weatherfetcher import Weatherfetcher



logger = logging.getLogger()
logging.config.fileConfig('logging.ini')




def main():

    wf = Weatherfetcher(cfg.DB_NAME, cfg.API_KEY, cfg.TABLE_NAME, cfg.LANGUAGES)
    wf.fetch_weather()

if __name__ == "__main__":
    logger.info(f"Application started: {cfg.APP_VERSION}")
    main()
    logger.info(f"Application closed: {cfg.APP_VERSION}")

    

