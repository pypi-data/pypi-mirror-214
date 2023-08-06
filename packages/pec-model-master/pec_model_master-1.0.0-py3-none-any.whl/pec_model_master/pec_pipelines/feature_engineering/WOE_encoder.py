import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from category_encoders.woe import WOEEncoder


class LabelEncoder(BaseEstimator, TransformerMixin):
    """
    Class to label-enconde categorical columns with a Weight of Evidence Encoder

    input:
        df: dataframe
        cat_cols: list of categorical columns
        y: target
    """

    def __init__(self):
        self.cat_cols = ['sex', 'embarked']
        self.target_col = 'survived'
        self.encoder = None

    def fit(self, df: pd.DataFrame):
        self.encoder = WOEEncoder(cols=self.cat_cols, drop_invariant=True, return_df=True)
        self.encoder.fit(df[self.cat_cols], df[self.target_col])
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        cats = self.encoder.transform(df[self.cat_cols])
        df = df[list(set(df.columns.values).difference(set(self.cat_cols)))]
        df = pd.merge(df, cats, how='left', left_index=True, right_index=True)
        return df
