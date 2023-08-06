from sklearn.model_selection import train_test_split
from pec_pipelines.preproces_pipeline import Preprocess
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import GridSearchCV
from pec_pipelines.feature_engineering.utils import save_model

if __name__ == "__main__":
    path = 'notebooks/data/titanic.csv'
    df = pd.read_csv(path, sep=';')
    print(df.shape)

    X_train, X_test, y_train, y_test = train_test_split(df, df.survived, test_size=0.3, random_state=42)

    model_pipe = Preprocess()

    prepro_train = model_pipe.pipe.fit_transform(X_train)
    prepro_test = model_pipe.pipe.transform(X_test)

    best = CatBoostClassifier(eval_metric="AUC")
    cb_params = dict(n_estimators=[800],
                     learning_rate=[0.01],
                     max_depth=[4, 6],
                     scale_pos_weight=[50]
                     )
    grid = GridSearchCV(best, cb_params, cv=5, scoring='roc_auc', verbose=2, refit=True)
    grid.fit(prepro_train, y_train, use_best_model=True)
    # print('Roc_Auc score: ', grid.best_score_)
    model = grid.best_estimator_
    save_model(grid.best_estimator_)

    # y_pred = model.predict(prepro_test)
    # y_proba = model.predict_proba(prepro_test)[:,1]
    # X_test['Predict'] = y_pred.tolist()
    # X_test['Probabilidad'] = y_proba.tolist()

    # from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve
    # roc_auc_score(y_test, X_test['Probabilidad'])
