import json

with open("./config.json", mode = "r", encoding= "UTF-8") as file:
    config = json.load(file)



# PARSING
APP_TITLE = config["title"]
APP_VERSION = config["version"]



NA_HANDLE = config["dataclean"]["na_handle"]
NA_HANDLE_TYPE = config["dataclean"]["na_handle_type"]

DROP_COLUMNS= config["dataclean"]["drop_columns"]
DROP_COLUMNS_LIST = config["dataclean"]["drop_columns_list"]

DROP_DUPLICATE = config["dataclean"]["drop_duplicate"]
DROP_DUPLICATE_TYPE = config["dataclean"]["drop_duplicate_type"]

CONVERT_DTYPE = config["dataclean"]["convert_dtype"]
CONVERT_DTYPE_LIST = config["dataclean"]["convert_dtype_list"]
CONVERT_DTYPE_TYPE = config["dataclean"]["convert_dtype_type"]


OUTLIER_CLEANING = config["dataclean"]["outlier_cleaning"]
OUTLIER_CLEANING_LIST = config["dataclean"]["outlier_cleaning_features"]

OUTLIER_CLEANING_ALL = config["dataclean"]["outlier_cleaning_all"]

