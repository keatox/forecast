from preprocess import Preprocess
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
import pickle

class Sentimodel:
    def __init__(self): 
        self.__process = Preprocess()
        self.__vectorizer = None
        self.__model = self.tune_model()
        # self.__data = pd.read_csv("res/IMDB.csv")
        # self.__X = self.__data["review"].values.tolist()
        # self.__Y = self.__data["sentiment"].values

    # returns a list of predictions with either POSITIVE or NEGATIVE sentiment
    def prediction(self,text):
        return self.__model.predict(text)
    
    # generates bag-of-words representation of text
    def vectorize(self,data):
        # loads vectorizer pretrained on IMDB dataset
        if not self.__vectorizer:
            with open("models/countvectorizer.pkl", "rb") as f:
                self.__vectorizer = pickle.load(f)
            # uncomment below when fitting new data for vectorizer
            """
            from sklearn.feature_extraction.text import CountVectorizer

            vectorizer = CountVectorizer(max_features = 2500,
                                         preprocessor=self.override,
                                         token_pattern='[a-zA-Z0-9$&+,:;=?@#|<>.^*()%!-]+')
            self.__vectorizer = vectorizer.fit(data)
            with open("models/countvectorizer.pkl", "wb") as f:
                pickle.dump(self.__vectorizer, f)
            """
        return self.__vectorizer.transform(data).toarray()  

    # to override preprocessing step in vectorization
    def override(self,text):
        return text
    
    # new processing method that override accounts for
    def process(self):
        self.__X = self.__process.preprocess(self.__X)
        self.__X = self.vectorize(self.__X)

    # loads pretrained sentiment model, includes code to retrain/test
    def tune_model(self):
        with open("models/sentimentmodel.pkl", "rb") as f:
             return pickle.load(f)

        self.process()
        X, Xt, Y, Yt = train_test_split(self.__X, self.__Y, test_size = 0.20, random_state = 0)

        # below code can be used to help optimize model
        """
        import numpy as np
        import matplotlib.pyplot as plt
    
        C = np.logspace(-10,10,50)
        acc = np.empty(50)
        acct = np.empty(50)
        for i in range(50):
            model = LinearSVC(dual='auto',C=C[i],fit_intercept=False).fit(X,Y)
            acc[i] = model.score(X,Y)
            acct[i] = model.score(Xt,Yt)
        plt.plot(acc,label="train")
        plt.plot(acct,label="test")
        plt.legend()
        plt.show()
        print(C[np.argmax(acc)])
        print(C[np.argmax(acct)])
        """

        model = LinearSVC(dual='auto',C=0.245,fit_intercept=False).fit(X,Y)
        # print(model.score(X,Y))
        # print(model.score(Xt,Yt))
        with open("models/sentimentmodel.pkl", "wb") as f:
            pickle.dump(model, f)
        return model