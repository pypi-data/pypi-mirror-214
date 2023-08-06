import unittest
import numpy as np
import pandas as pd
from adversarial.adversarial_test import AdversarialModel
from catboost import CatBoostClassifier, CatBoostRegressor, Pool, cv

class TestAdversarialModel(unittest.TestCase):
    def setUp(self):
        self.model = AdversarialModel(CatBoostClassifier(iterations=300, verbose=False))

    def test_fit_same_distribution(self):
        df1 = pd.DataFrame(np.random.rand(1000, 50))
        df2 = pd.DataFrame(np.random.rand(1000, 50))
        self.model.fit(df1, df2)
        self.assertEqual(self.model.evaluate(), "pass")
    
    def test_fit_differ_distribution(self):
        df1 = pd.DataFrame(np.random.rand(1000, 50))
        df2 = pd.DataFrame(np.random.randint(1, (1000, 50)))
        self.model.fit(df1, df2)
        self.assertEqual(self.model.evaluate(), "fail")


