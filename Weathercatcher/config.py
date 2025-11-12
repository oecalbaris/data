import json
from dotenv import load_dotenv
import os

with open("./config.json", mode = "r", encoding= "UTF-8") as file:
    config = json.load(file)



# PARSING
APP_TITLE = config["title"]
APP_VERSION = config["version"]

#Importing API KEY from .env
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Importing parameters from config.json
CITIES = config["fetch_parameters"]["cities"]
LANGUAGES = config["fetch_parameters"]["languages"]
TABLE_NAME = config["fetch_parameters"]["table_name"]
DB_NAME = config["fetch_parameters"]["db_name"]

