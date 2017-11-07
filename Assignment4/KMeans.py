import pandas as pd
import random as ra
import numpy as np
import math

class KMeans():
    def __init__(self, k, df: pd.DataFrame, iter=10):
        self.k = k
        self.iter = iter
        self.centroids = []
        self.tags = None
        self.df = df
        self.numfeatures = len(self.df.columns)
        self.features = df.columns


    def fit(self):
        """
        fit the data
        :param df: list
        :return:
        """

        if not self.checkvalid(self.df):
            raise NameError("Not all the columns are numeric.")


        numrows = len(self.df)

        # initialize the centroid randomly
        for i in range(self.k):
            centroid = []
            for feature in self.features:
                centroid.append(ra.uniform(self.df[feature].min(), self.df[feature].max()))
            self.centroids.append(centroid)
        self.centroids = np.array(self.centroids)

        iteration = 0
        # prevtag = [[] for i in range(self.k)]
        while iteration < self.iter:
            self.tags = [[] for i in range(self.k)]
            for i in range(numrows):
                tag = self.belongto(np.array(self.df.iloc[i,]))
                self.tags[tag].append(i)
            old = self.centroids.copy()
            self.updatecentroids()
            if np.sum(abs((self.centroids-old)/old) > abs(old) * 0.2) == 0:
                break
            iteration += 1

    def checkvalid(self, df: pd.DataFrame):
        return True

    def belongto(self, obs: np.array):
        mindist = None
        group = None

        # centroids is 2d array
        for row in range(self.k):
            dist = 0
            for num in range(self.numfeatures):
                dist += (obs[num] - self.centroids[row, num]) ** 2
            dist = math.sqrt(dist)
            if mindist is None:
                mindist = dist
                group = row
            elif dist < mindist:
                mindist = dist
                group = row
        return group

    def updatecentroids(self):
        for k in range(self.k):
            for col in range(self.numfeatures):
                if len(self.tags[k]) != 0:
                    self.centroids[k, col] = self.df.iloc[self.tags[k], col].mean()