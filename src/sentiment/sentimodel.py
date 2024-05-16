from preprocess import Preprocess
import numpy as np
import pandas as pd
import matplotlib as plt
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

class Sentimodel:
    def __init__(self):
        self._data = pd.read_csv("res/IMDB.csv")
        self._process = Preprocess()
        self._X = self._data["review"].values.tolist()
        self._Y = self._data["sentiment"].values

    def override(self,text):
        return text
    
    def process(self):
        for i in range(len(self._X)):
            self._X[i] = self._process.preprocess(self._X[i])
        self._X = self._process.remove_stopwords(self._X) 
        self._X = self.vectorize(self._X)
    
    def vectorize(self,data):
        vectorizer = CountVectorizer(max_features = 300,
                                     preprocessor=self.override,
                                     token_pattern='[a-zA-Z0-9$&+,:;=?@#|<>.^*()%!-]+')
        return vectorizer.fit_transform(data).toarray()    

    def tune_model(self):
        X, Xt, Y, Yt = train_test_split(self._X, self._Y, test_size = 0.20, random_state = 0)

        model = LinearSVC(dual='auto').fit(X,Y)
        print(model.score(X,Y))
        print(model.score(Xt,Yt))

    def return_model(self):
        pass

model = Sentimodel()
model.process()
model.tune_model()