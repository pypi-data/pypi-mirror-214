import pickle
import pandas as pd
from datetime import datetime

PATH_MODEL = 'pec_model_master/pec_pipelines/model/'


def save_model(estimator):
    t_st = datetime.now().strftime('%Y%m%dT%H%M%S')
    output = open(PATH_MODEL + 'catboost_' + t_st + '.pkl', 'wb')
    pickle.dump(estimator, output, -1)
    output.close()


def open_model(path: str):
    pkl = open(path, 'rb')
    model = pickle.load(pkl)
    pkl.close()
    return model


def drop_columns(df: pd.DataFrame, col: str):
    del df[col]


def lower_names(df: pd.DataFrame):
    df.columns = map(str.lower, df.columns)


def missing_values(df: pd.DataFrame):
    num_cols = df.select_dtypes(include=['number', 'int', 'float', 'float64']).columns.tolist()
    for i in num_cols:
        try:
            df[i].fillna(value=100, inplace=True)
        except Exception as e:
            print(f'Could not apply missing values to column {e}')
