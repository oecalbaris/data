import pandas as pd
import logging
from ydata_profiling import ProfileReport
from scipy import stats
import config as cfg

logger = logging.getLogger()


class Datacleaner:

    def __init__(self, input_file_path: str):

        self.df_original = self.read_data(input_file_path)  # # uncleaned file

        self.df = self.read_data(input_file_path)  # Process file

        logger.debug("Data is loaded")

    def read_data(self, input_file_path: str) -> pd.DataFrame:
        """Reads the data for provided file

        Args:
            input_file_path (str): the relative path of the input file

        Returns:
            pd.DataFrame: DataFrame of the Data
        """

        df = pd.read_csv(input_file_path)
        return df

    def create_data_profile(self, original=False, cleaned=False):
        if original:
            profile = ProfileReport(self.df_original, title="My Data Profile of original File",
                                    dataset={
                                        "description": "This is a data profile of the eCommerce WebShop - Cleaned Data",
                                        "author": "Baris"
                                    })
            profile.to_file("./dataprofiles/report_original.html")
            logger.info("Data Profile for orignal created.!")

        if cleaned:
            profile = ProfileReport(self.df, title="My Data Profile of cleaned DataFrame",
                                    dataset={
                                        "description": "This is a data profile of the eCommerce WebShop - Cleaned Data",
                                        "author": "Baris"
                                    })
            profile.to_file("./dataprofiles/report_cleaned.html")
            logger.info("Data Profile for cleaned created.!")




    def drop_column(self,featurename:str):

        if featurename not in self.df.columns:
            logger.error("Invalid feature list.")
            return self.df


        self.df.drop(featurename, axis=1, inplace=True)
        logger.info(f"Columns '{featurename}' is dropped successfully.")


    def na_handle(self, choice):

        if choice == "drop":  # deletes NA
            self.df.dropna(inplace=True)
            logger.info("NA values are dropped.")

        elif choice == "forward_fill":  # forward fill
            self.df.fillna(method="ffill", inplace=True)
            logger.info("NA values are forward filled")

        elif choice == "backward_fill":  # Backward fill
            self.df.fillna(method="bfill", inplace=True)
            logger.info("NA values are backward filled")

        elif choice == "mean_fill":  # Replacing with mean value
            self.df.fillna(self.df.mean(), inplace=True)
            logger.info("NA values are mean filled")

        elif choice == "median_fill":  # replacing with median value
            self.df.fillna(self.df.median(), inplace=True)
            logger.info("NA values are median filled")

        else:  # in case of wrong input doesn´t change the data and
            logger.error("Invalid choice")

            return self.df

        return self.df

    def drop_duplicate(self, choice:str):

        if choice == "all_drop":
            self.df.drop_duplicates(inplace=True)
            print("All duplicated data is deleted.")


        elif choice == "first_drop":
            self.df.drop_duplicates(inplace=True, keep="first")
            logger.info("Kept first of duplicates. Others removed.")


        elif choice == "last_drop":
            self.df.drop_duplicates(inplace=True, keep="last")
            logger.info("Kept last of duplicates. Others removed.")

        else:
            logger.error("Invalid choice for duplicate handling.")

        return self.df


    def convert_dtype(self,featurename:str,datatype:str):

        if datatype is None:
            logger.error("Invalid datatype choice.")
            return self.df

        if featurename is None:
            logger.error("Invalid feature name.")
            return self.df

        try:
            self.df[featurename] = self.df[featurename].astype(datatype)
            logger.info(f"Data type of '{featurename}' converted to {datatype} successfully.")
            return self.df

        except (ValueError, TypeError, KeyError) as e:
            logger.error(f"Data type conversion failed: {e}")
            return self.df

    def outlier_cleaning(self,featurename):

        if featurename not in self.df.columns:
            logger.error(f"Feature '{featurename}' not found in the dataframe.")
            raise ValueError(f"Feature '{featurename}' not found in the dataframe.")

        z_scores = stats.zscore(self.df[featurename])
        mask = (z_scores >= -3) & (z_scores <= 3)  # -3 and 3 is the common choises in z-score method
        self.df = self.df.loc[mask]

        logger.info(f"Outliers removed from '{featurename}' using z-score method successfully.")
        return self.df


    def outlier_cleaning_all(self):

        z_scores = stats.zscore(self.df)
        mask = (z_scores >= -3) & (z_scores <= 3)  # -3 and 3 is the common choises in z-score method
        self.df = self.df.loc[mask]

        logger.info(f"Outliers removed  using z-score method successfully.")
        return self.df


    def clean_data(self):

        if cfg.DROP_COLUMNS:
            for col in cfg.DROP_COLUMNS_LIST:
                self.drop_column(col)

        if cfg.NA_HANDLE:
            self.na_handle(cfg.NA_HANDLE_TYPE)

        if cfg.DROP_DUPLICATE:
            self.drop_duplicate(cfg.DROP_DUPLICATE_TYPE)

        if cfg.CONVERT_DTYPE:
            for col in cfg.CONVERT_DTYPE_LIST:
                self.convert_dtype(col, cfg.CONVERT_DTYPE_TYPE)

        if cfg.OUTLIER_CLEANING:
            for col in cfg.OUTLIER_CLEANING_LIST:
                self.outlier_cleaning(col)

        if cfg.OUTLIER_CLEANING_ALL:
            self.outlier_cleaning_all()

    def save_csv(self):
        self.df.to_csv(f'./data/output/cleaned_data.csv', index=False)
        logger.info("Data is saved successfully.")
