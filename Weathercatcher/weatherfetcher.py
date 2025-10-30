
import logging.config

import sqlite3
import requests
import logging
import config as cfg

logging.basicConfig(level=logging.INFO)


class Weatherfetcher:

    def __init__(self, db_name: str, api_key: str,table_name:str, languages: list):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.api_key = api_key # Constant
        self.languages = languages # Constant across the code
        self.tb_name = table_name # constant across the code
        self.create_table()  # Corrected method name

    def create_table(self):
        """Create the weather table if it doesn't exist"""
        sql = f"""
              CREATE TABLE IF NOT EXISTS {self.tb_name} \
              ( \
                  ID \
                  INTEGER \
                  PRIMARY \
                  KEY \
                  AUTOINCREMENT, \
                  Cityname \
                  TEXT, \
                  Temperature \
                  TEXT, \
                  Description_en \
                  TEXT, \
                  Description_de \
                  TEXT
              ); \
              """
        self.c.execute(sql)
        self.conn.commit()
        logging.info("Table 'weather' created or already exists.")

    def insert_data(self, cityname, temperature, description_en, description_de):
        """Insert data into SQL table"""
        try:
            params = (cityname, temperature, description_en, description_de)
            sql = f"""
                  INSERT INTO {self.tb_name} (Cityname, Temperature, Description_en, Description_de)
                  VALUES (?, ?, ?, ?) \
                  """
            self.c.execute(sql, params)
            self.conn.commit()
            logging.info(f"Data inserted to SQL for {cityname}")

        except Exception as e:
            logging.error(f"Error inserting data for {cityname}: {e}")

    def fetch_weather_city(self, city):
        """Fetch weather data from OpenWeather API"""
        weather_data = {}
        for lang in self.languages:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric&lang={lang}"
            try:
                response = requests.get(url)
                data = response.json()

                if response.status_code == 200:
                    weather_data["Cityname"] = data["name"]
                    weather_data["Temperature"] = data["main"]["temp"]
                    weather_data[f"Description_{lang}"] = data["weather"][0]["description"]
                else:
                    logging.warning(f"Failed request for {city} in {lang}: {data}")
            except Exception as e:
                logging.error(f"Exception fetching data for {city} in {lang}: {e}")

        if weather_data:
            logging.info(f"Weather data fetched for {city}.")
            return weather_data

        else:
            logging.warning(f"No weather data fetched for {city}.")
            return None

    def close_db(self):
        self.conn.close()
        logging.info("Database connection closed.")



    def fetch_weather(self):
        """Fetch weather data for a list of cities"""

        for city in cfg.CITIES:
            data = self.fetch_weather_city(city)

            if data:
                self.insert_data(
                    cityname=data["Cityname"],
                    temperature=data["Temperature"],
                    description_en=data.get("Description_en", ""),
                    description_de=data.get("Description_de", ""),
                )

        self.close_db()


