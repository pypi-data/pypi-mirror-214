import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold
from sklearn.metrics import roc_auc_score, fbeta_score

class AdversarialModel():
    def __init__(
        self,
        model
    ) -> None:
        self.model = model
    
    def fit(
        self,
        df1: pd.DataFrame,
        df2: pd.DataFrame,
        groups=None,
        features=None,
        cat_features=None,
        metrics=[(roc_auc_score,), (fbeta_score, {"beta": 0.5})]
    ):
        data_adversarial = pd.concat([
            df1.assign(label=0),
            df2.assign(label=1),
        ], ignore_index=True)
        # print(data_adversarial)
        # print(data_adversarial["label"].value_counts())
        if features == None:
            features = df1.columns

        # stratified_group split 80/20
        if groups != None:
            sgkf = StratifiedGroupKFold(n_splits=5)
        else:
            sgkf = StratifiedKFold(n_splits=5)
        for fold_ind, (dev_ind, val_ind) in enumerate(sgkf.split(data_adversarial, data_adversarial["label"], groups)):
            train_idx = dev_ind
            val_idx = val_ind
            break
        # Create train/dev data
        X_train = data_adversarial.iloc[train_idx][features]
        y_train = data_adversarial.iloc[train_idx]["label"]
        X_val = data_adversarial.iloc[val_idx][features]
        y_val = data_adversarial.iloc[val_idx]["label"]

        # Train adversarial model
        self.model.set_params(cat_features = cat_features)
        self.model.fit(X_train, y_train)
        # for metric, param in metrics:
        #     print(metric(y_val, self.model.predict(X_val), **param))
        self.auc_score = roc_auc_score(y_val, self.model.predict(X_val))

    def get_features_importance(
        self,
    ):
        pass

    def evaluate(self, threshold=0.7):
        if self.auc_score <= 0.7:
            return "pass"
        else:
            return "fail"
