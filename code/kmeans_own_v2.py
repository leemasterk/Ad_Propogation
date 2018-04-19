from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import warnings
from numbers import Integral
import random


class KMeansPlusPlus:

    def __init__(self, data_frame, k, columns=None, max_iterations=None,
                 appended_column_name=None):
        if not isinstance(data_frame, DataFrame):
            raise Exception("data_frame argument is not a pandas DataFrame")
        elif data_frame.empty:
            raise Exception("The given data frame is empty")

        if max_iterations is not None and max_iterations <= 0:
            raise Exception("max_iterations must be positive!")

        if not isinstance(k, Integral) or k <= 0:
            raise Exception("The value of k must be a positive integer")

        self.data_frame = data_frame  # m x n
        self.numRows = data_frame.shape[0]  # m
        # self.m = self.get_metric()
        # k x n, the i,j entry being the jth coordinate of center i
        self.centers = None
        self.index = []
        # m x k , the i,j entry represents the distance
        # from point i to center j
        # (where i and j start at 0)
        self.distance_matrix = None

        # Series of length m, consisting of integers 0,1,...,k-1
        self.clusters = None

        # To keep track of clusters in the previous iteration
        self.previous_clusters = None

        self.max_iterations = max_iterations
        self.appended_column_name = appended_column_name
        self.k = k
        # print ("df: ",self.data_frame.shape)

        if columns is None:
            self.columns = data_frame.columns
        else:
            for col in columns:
                if col not in data_frame.columns:
                    raise Exception(
                        "Column '%s' not found in the given DataFrame" % col)
                if not self._is_numeric(col):
                    raise Exception(
                        "The column '%s' is either not numeric or contains NaN values" % col)
            self.columns = columns

    def populate_initial_centers(self):
        rows = []
        # rows.append(self.data_frame.iloc[0,:])
        rows.append(self._grab_random_point())
        distances = None

        while len(rows) < self.k:
            if distances is None:
                distances = self.get_dist_point(self.data_frame ,rows[0])
            else:
                distances = self.get_dist_list(self.data_frame, rows)

            '''array / array'''
            normalized_distances = distances / distances.sum()
            index = random.choices(range(0,self.numRows), weights=normalized_distances, k=1)
            self.index.append(index)
            centroid = self.data_frame[self.columns].iloc[index, :].values
            rows.append(centroid.reshape(centroid.shape[1]))
        self.centers = DataFrame(rows, columns=self.columns)
        # print(self.centers)

    def _grab_random_point(self):  # get values of an row
        index = np.random.random_integers(0, self.numRows - 1)
        self.index.append(index)
        return self.data_frame[self.columns].iloc[index, :].values

    def get_dist_single(self, x, y): #x is a sample, y is a the centroid of cluster
        # print ("X ",x)
        # print("Y ", y)

        Z = np.array([x - y])
        # print(Z)
        dist = np.sum(Z != 0)
        # print(dist)
        return dist

    def get_dist_point(self, X, Y):
        dist_lst = []
        # print ("len ", len(X))
        for i in range(len(X)):
            x = np.array(X.iloc[i])
            # y = np.array(Y.iloc[i])
            y = Y
            dist_lst.append(self.get_dist_single(x, y))
        l = np.array(dist_lst).reshape((len(dist_lst),1))
        # return dist.values
        return l

    def get_dist_list(self, X, Y):
        result = None

        for point in Y:
            if result is None:
                # result = self.get_dist_point(X, point.values)
                result = self.get_dist_point(X, point)
            else:
                # print ("r ",result)
                # print("")
                l = self.get_dist_point(X, point)
                result = np.concatenate((result, l), axis=1)
        result = result.min(axis=1)
        return result

    def compute_distances(self):
        # dis_mat = DataFrame()
        dis_mat = np.zeros((len(self.data_frame.index),1))

        for i in range(self.k):
            d = self.centers.iloc[i,:] - self.data_frame
            # print(d)
            # print(d!=0)
            dist = np.sum(d!=0,axis=1)
            # print(dist)
            dis_mat = np.concatenate((dis_mat, dist.reshape(dist.shape[0],1)),axis=1)
        # print (dis_mat)
        dis_mat = np.delete(dis_mat,0,1)
        # print(dis_mat)
        self.distance_matrix = DataFrame(
            dis_mat, columns=list(range(self.k)))

    def get_clusters(self):
        if self.distance_matrix is None:
            raise Exception(
                "Must compute distances before closest centers can be calculated")

        # min_distances = self.distance_matrix.min(axis=1)
        #
        # # We need to make sure the index
        # min_distances.index = list(range(self.numRows))
        self.clusters = Series(self.distance_matrix.idxmin(axis=1).values, index=self.data_frame.index)

    def compute_new_centers(self):
        if self.centers is None:
            raise Exception("Centers not initialized!")

        if self.clusters is None:
            raise Exception("Clusters not computed!")

        # print(self.data_frame)
        # data
        for i in list(range(self.k)):
            self.centers.ix[i, :] = self.data_frame[
                self.columns].ix[self.clusters == i].mean()
        # print("before ",self.centers)
        # self.centers = self.centers.astype(int)
        try:
            self.centers =  self.centers.astype(int)
        except ValueError:


            index = (np.sum(self.distance_matrix, axis=1) == 9).values.nonzero()[0]
            # print(type(index))
            # print((np.sum(self.distance_matrix, axis=1) == 9).nonzero()[0])
            # asdf
            # print("index, ",index)
            # print("before ",self.centers)
            # self.distance_matrix
            ind =np.random.choice(index, int(len(index)/10))
            # print("ind", ind)
            self.clusters[ind] = 2
            for i in list(range(self.k)):
                self.centers.ix[i, :] = self.data_frame[
                    self.columns].ix[self.clusters == i].mean()
            # self.centers[np.sum(self.distance_matrix,axis=1) == 9]
            self.centers = self.centers.astype(int)
            # print(self.centers)

    def cluster(self):

        self.populate_initial_centers()
        self.compute_distances()
        self.get_clusters()

        counter = 0

        while True:
            counter += 1

            self.previous_clusters = self.clusters.copy()

            self.compute_new_centers()
            # print(self.centers)
            self.compute_distances()
            # print(self.distance_matrix)
            self.get_clusters()
            # print(self.clusters)

            if self.max_iterations is not None and counter >= self.max_iterations:
                break
            elif all(self.clusters == self.previous_clusters):
                break

        if self.appended_column_name is not None:
            try:
                self.data_frame[self.appended_column_name] = self.clusters
            except:
                warnings.warn(
                    "Unable to append a column named %s to your data." %
                    self.appended_column_name)
                warnings.warn(
                    "However, the clusters are available via the cluster attribute")



