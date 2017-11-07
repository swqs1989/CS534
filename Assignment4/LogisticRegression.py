import pandas as pd
import random as ra
import numpy as np
import math

class logistic():
    def __init__(self, X, y, rate=0.01, iter=100, lda=1, sample=None):
        self.X = np.array(X)
        self.y = np.array(y)
        self.rate = rate
        self.iter = iter
        intercept = np.ones((self.X.shape[0], 1))
        self.X = np.hstack((intercept, self.X))
        self.weights = np.zeros(self.X.shape[1])
        self.lda = lda

    def fit(self):
        for i in range(self.iter):
            scores = np.dot(self.X, self.weights)
            yhat = self.sigmoid(scores)
            # Update weights with gradient
            error = self.y - yhat
            gradient = np.dot(self.X.T, error) + self.lda/self.X.shape[0]
            self.weights += self.rate * gradient

    def predict(self, ndf):
        ndf = np.array(ndf)
        intercept = np.ones((ndf.shape[0], 1))
        ndf = np.hstack((intercept, ndf))
        prob = np.dot(ndf, self.weights)
        prediction = self.sigmoid(prob)
        return prediction

    def sigmoid(self, scores):
        return 1 / (1 + np.exp(-scores))