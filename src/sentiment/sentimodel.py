from preprocess import Preprocess
import numpy as np
import pandas as pd
import matplotlib as plt
from sklearn.svm import SVC

class Sentimodel:
    def __init__(self):
        self._data = pd.read_csv("res/IMDB.csv")
        self._process = Preprocess()
        self._X = self._data["review"].values.tolist()
        self._Y = self._data["sentiment"].values


    def process(self):
        for i in range(len(self._X)):
            self._X[i] = self._process.preprocess(self._X[i])
        self._X = self._process.remove_stopwords(self._X)

    def tune_model(self):
        pass

    def return_model(self):
        pass

model = Sentimodel()

model.process()