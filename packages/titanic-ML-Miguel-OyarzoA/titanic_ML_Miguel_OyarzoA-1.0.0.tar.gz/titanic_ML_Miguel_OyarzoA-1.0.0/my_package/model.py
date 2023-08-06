import pandas as pd
import numpy as np
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from feature_engine.imputation import (
    MeanMedianImputer,
    AddMissingIndicator
)
from feature_engine.selection import DropFeatures
from feature_engine.encoding import OrdinalEncoder

class TitanicSurvivalModel:
    def __init__(self):
        self.pipeline = None

    def preprocess_data(self, X):
        NUMERICAL_VARS_WITH_NA = ['age']
        DROP_FEATURES = ["name", "sibsp", "parch", "ticket", "cabin", "embarked"]
        FEATURES = ['pclass', 'sex', 'age', 'fare']

        pipeline = Pipeline([
            ('drop_features', DropFeatures(features_to_drop=DROP_FEATURES)),
            ('missing_indicator', AddMissingIndicator(variables=NUMERICAL_VARS_WITH_NA)),
            ('mean_imputation', MeanMedianImputer(imputation_method='mean', variables=NUMERICAL_VARS_WITH_NA)),
            ('categorical_encoding', OrdinalEncoder(encoding_method='arbitrary', variables=['sex'])),
            ('LogisticRegression', LogisticRegression())
        ])

        preprocessed_X = pipeline.transform(X)
        return preprocessed_X

    def train(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
        X_train = pd.DataFrame(X_train, columns=["pclass","name", "sex", "age", "sibsp", "parch", "ticket", "fare", "cabin", "embarked"])
        y_train = pd.DataFrame(y_train, columns=['survived'])
        self.pipeline = Pipeline([('preprocessing', self.preprocess_data), ('LogisticRegression', LogisticRegression())])
        self.pipeline.fit(X_train, y_train.values.ravel())

    def predict(self, X):
        preprocessed_X = self.preprocess_data(X)
        predictions = self.pipeline.predict(preprocessed_X)
        return predictions

    def save_model(self, file_path):
        joblib.dump(self.pipeline, file_path)

    def load_model(self, file_path):
        self.pipeline = joblib.load(file_path)