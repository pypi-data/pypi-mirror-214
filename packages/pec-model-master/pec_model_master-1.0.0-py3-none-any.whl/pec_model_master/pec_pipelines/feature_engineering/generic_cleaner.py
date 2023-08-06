import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from pec_pipelines.feature_engineering.utils import drop_columns, lower_names, missing_values


class GenericCleaner(BaseEstimator, TransformerMixin):
    """
    Class to do an initial cleanup of the dataframe
    """

    def __init__(self):
        self.columns_remove = ['name', 'cabin', 'ticket']

    def fit(self, df: pd.DataFrame):
        return self

    def transform(self, df: pd.DataFrame):
        self.filter_columns(df)
        missing_values(df)
        lower_names(df)
        return df

    def filter_columns(self, df: pd.DataFrame):
        for col in self.columns_remove:
            drop_columns(df, col)
