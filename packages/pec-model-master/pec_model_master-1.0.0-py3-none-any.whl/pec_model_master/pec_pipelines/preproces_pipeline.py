from sklearn.pipeline import Pipeline
from pec_pipelines.feature_engineering.generic_cleaner import GenericCleaner
from pec_pipelines.feature_engineering.WOE_encoder import LabelEncoder


class Preprocess:
    def __init__(self):
        self.pipe = Pipeline(steps=[('generic_cleaner', GenericCleaner()),
                                    ('woe_transform', LabelEncoder())
                                    ])
