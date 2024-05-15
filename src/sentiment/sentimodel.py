from preprocess import Preprocess
import numpy as np
import matplotlib as plt
from sklearn.svm import SVC

class Sentimodel:
    def __init__(self):
        self.data = np.loadtxt("res/IMBD.csv",skiprows=1,delimiter=",")
        self.X = self.data[:,0]
        self.Y = self.data[:,1]

    def create_model(self):
        pass
