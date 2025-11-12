__author__ = "Baris"
__version__ = 1.0
__doc__ = """
This is a program to clean provided CSV file and gives a cleaned version
of it under output folder. It is an interactive program.
"""


import logging.config
from datacleaner import Datacleaner
import config as cfg


logger = logging.getLogger()
logging.config.fileConfig('logging.ini')



def main():
    cleaner = Datacleaner("./data/input/my_data.csv")

    #Data analytics --> one can ask customer about the data and how to clean it using created .html
    cleaner.create_data_profile(original=True, cleaned=False)

    cleaner.clean_data()

    # Data analytics after cleaning and Save cleaned data --> Final version is of the data is saved as .csv and analytics as .html
    cleaner.create_data_profile(original=False, cleaned=True)
    cleaner.save_csv()

if __name__ == "__main__":
    logger.info(f"Application started: {cfg.APP_VERSION}")
    main()
    logger.info(f"Application closed: {cfg.APP_VERSION}")

    

