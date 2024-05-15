from preprocess import Preprocess
import numpy as np
import matplotlib as plt
from sklearn.svm import SVC

class Sentimodel:
    def __init__(self):
        self._data = np.loadtxt("res/IMBD.csv",skiprows=1,delimiter=",")
        self._X = self._data[:,0]
        self._Y = self._data[:,1]

    def process(self):
        process = Preprocess()
        process.preprocess(self._X)
        print(process)

    def tune_model(self):
        pass

    def return_model(self):
        pass

model = Sentimodel()

model.process()