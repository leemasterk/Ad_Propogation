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
        # self.m = np.array([[ 7.40287431e-07, -1.15234740e-07, -3.16733397e-07, -1.23115312e-08],
        #          [-1.15234740e-07,  1.92350266e-06, -8.96508054e-08,  5.49038595e-09],
        #          [-3.16733397e-07, -8.96508054e-08,  6.13053227e-06, -7.91933304e-08],
        #          [-1.23115312e-08,  5.49038595e-09, -7.91933304e-08, 2.04514885e-06]])

        self.m = np.array([[1.39120240528e-06, -7.11964361751e-08, 1.68554275438e-07],
                        [-7.1196436173e-08, 4.18367212413e-06, -2.45888145316e-07],
                        [1.6855427544e-07, -2.45888145311e-07, 1.43614586304e-06]])

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

    def _populate_initial_centers(self):
        rows = []
        rows.append(self._grab_random_point())
        # print ("rows ", rows[0])
        distances = None

        while len(rows) < self.k:
            if distances is None:
                # index = random.randint(0, self.numRows)
                # print ("index", index)
                distances = self.get_dist_point(self.data_frame ,rows[0])
            else:
                distances = self.get_dist_list(self.data_frame, rows)

            '''array / array'''
            normalized_distances = distances / distances.sum()
            # normalized_distances.sort()
            # print ("nor ", normalized_distances)
            index = random.choices(range(0,self.numRows), weights=normalized_distances, k=1)
            self.index.append(index)
            # print("index ",index)
            # dice_roll = np.random.rand()
            # min_over_roll = normalized_distances[
            #     normalized_distances.cumsum() >= dice_roll].min()
            # index = normalized_distances[
            #     normalized_distances == min_over_roll].index[0]
            # rows.append(self.data_frame[self.columns].iloc[index, :].values)
            centroid = self.data_frame[self.columns].iloc[index, :].values
            # print ("centroid ", centroid)
            # rows.append(centroid.reshape(len(centroid),1))
            # rows.append(centroid.T)]
            # print ("cen ",centroid)
            rows.append(centroid.reshape(centroid.shape[1]))
            # print (rows)
            # print (rows)
        # print ("col ",self.columns)
        # print (rows)
        self.centers = DataFrame(rows, columns=self.columns)
        # print ("cen \n",self.centers)

    def _grab_random_point(self):  # get values of an row
        index = np.random.random_integers(0, self.numRows - 1)
        self.index.append(index)
        # NumPy array
        return self.data_frame[self.columns].iloc[index, :].values

    def get_dist_single(self, x, y, M): #x is a sample, y is a the centroid of cluster
        # print ("X ",x)
        # print("Y ", y)
        Z = np.array([x - y])

        # print ("Z: ",Z.shape)
        # print("M: ", M.shape)
        # np.dot(Z, M)
        # print("ZM: ", np.dot(Z, M).shape)

        # print ()
        dist = np.sqrt(np.dot(np.dot(Z, M), Z.T))
        return dist[0][0]

    def get_dist_point(self, X, Y):
        M = self.m
        # print (M)
        dist_lst = []
        # print ("len ", len(X))
        for i in range(len(X)):
            x = np.array(X.iloc[i])
            # y = np.array(Y.iloc[i])
            y = Y
            dist_lst.append(self.get_dist_single(x, y, M))
        # dist = pd.DataFrame({'distance': dist_lst})
        # dist = pd.Series(dist_lst, index=np.arange(len(dist_lst)))
        # print (dist.values.shape)
        # return dist
        # print ("y ", Y)
        # print("dist ", dist_lst)
        l = np.array(dist_lst).reshape((len(dist_lst),1))
        # return dist.values
        return l

    def get_dist_list(self, X, Y):
        result = None

        for point in Y:
            if result is None:
                # result = self.get_dist_point(X, point.values)
                result = self.get_dist_point(X, point)
                # result = result.reshape((1,result.shape[0]))
                # print ("r_ ",result)
                # print (len(result))
            else:
                # print ("r ",result)
                # print("")
                l = self.get_dist_point(X, point)
                # l = l.reshape((1,l.shape[0]))
                # print (l)
                # print (l.shape)
                # print ("result",result)
                # print ("l ", l)
                result = np.concatenate((result, l), axis=1)

                # print (result)
                # result = pd.concat(
                #     [result, self.get_dist_point(X, point)], axis=1).min(axis=1)
        # M = self.m
        # dist_lst = []
        # for i in range(len(X)):
        #     x = np.array(X.iloc[i])
        #     # y = np.array(Y.iloc[i])
        #     y = Y
        #     dist_lst.append(self.get_dist_single(x, y, M))
        # # dist = pd.DataFrame({'distance': dist_lst})
        # dist = pd.Series(dist_lst, index=np.arange(len(dist_lst)))
        result = result.min(axis=1)
        return result


    # def get_metric(self):
    #     # ad = pd.read_csv('ad_feature.csv', header=0)
    #     ad = self.data_frame
    #     data = ad.values
    #     m = np.array([[.0, .0, .0, .0], [.0, .0, .0, .0], [.0, .0, .0, .0], [.0, .0, .0, .0]])
    #     itml = ITML_Supervised(num_constraints=200)
    #     for i in range(600):
    #         data_r = np.array(random.sample(data.tolist(), int(len(data) / 100)))
    #         x = data_r[:, [0, 2, 3, 4]]
    #         y = data_r[:, 1]
    #         itml.fit(x, y)
    #         m = m + itml.metric()
    #     m = m / 600
    #     return m

    # def get_metric(self):
    #     fr = open('metric.txt', 'r')
    #     m = []
    #     for line in fr.readlines():
    #         line = list(map(float, line.strip().split()))
    #         m.append(line)
    #     m = np.array(m)
    #     return m

    def _compute_distances(self):
        # dis_mat = DataFrame()
        dis_mat = np.zeros((len(self.data_frame.index),1))
        # print ('test')
        M= DataFrame(self.m,index=['campaign_id','customer','brand'],)
                     # columns=['adgroup_id','campaign_id','customer','brand'])
        M_transpose = DataFrame(self.m.T,index=['campaign_id','customer','brand'],)
        # print (M)
        # print(M_transpose)
        for i in range(self.k):
            d = self.centers.iloc[i,:] - self.data_frame
            # print (d.transpose())
            # print (d.shape)
            # print (M.shape)
            # test = np.dot(d.values, M.values)
            # print ("test ",test)
            # tran = np.dot(test,d.values.T)
            # print ("tarn ", tran)
            # print (np.isnan(tran).sum())




            # print (self.centers.iloc[0,:])
            # print (self.data_frame.iloc[0,:])
            # print ("d ",d)
            # print("M ",M)
            # dist = DataFrame.dot(d, M)
            df1 = DataFrame.dot(d, M).rename(columns=
              {0:'campaign_id',1:'customer',2:'brand'})
            # dist = DataFrame.dot(df1, d.transpose())
            dist = np.sqrt(np.diagonal(DataFrame.dot(df1, d.transpose())))
            # print ("df1 ",df1.shape)
            # print("dist ",dist.shape)
            # print("df1 ", df1)
            # print("dist ", dist)
            # if i == 0:
            #     dis_mat = dist.iloc[:,0]
            # else:
            # pd.concat([dis_mat,dist.iloc[:,0]])
            # print (dis_mat)
            # print (dist)
            dis_mat = np.concatenate((dis_mat, dist.reshape(dist.shape[0],1)),axis=1)
        # print (dis_mat)
        dis_mat = np.delete(dis_mat,0,1)
        # print(dis_mat)
        self.distance_matrix = DataFrame(
            dis_mat, columns=list(range(self.k)))
        # self.distance_matrix = dis_mat
        # print (self.distance_matrix)
        # return dist[0][0]

    def get_distance_matrix(self):
    #     dis = np.zeros((self.k,len(self.data_frame.index)))
    #     for i in range(self.k):
    #         for j in range(len(self.data_frame.index)):
    #             d = (self.centers.iloc[i]-self.data_frame).values
    #             t = np.dot(np.dot(d, self.m), d.T).diagonal()
    #             print("before ",t)
    #             t = np.sqrt(t)
    #             print("after sqrt ",t)
    #             # np.concatenate((,dis),axis=1)
    #             # d = self.get_dist_single(self.centers.iloc[i], self.data_frame.iloc[j], self.m)
    #             # dis[i][j] = d
    #     print(dis)
    #     print(dis.shape)



        dis = np.zeros((self.k,len(self.data_frame.index)))
        for i in range(self.k):
            for j in range(len(self.data_frame.index)):
                d = self.get_dist_single(self.centers.iloc[i], self.data_frame.iloc[j], self.m)
                dis[i][j] = d
        print (dis.T)

    # def compute_distances(self):
    #     if self.centers is None:
    #         raise Exception(
    #             "Must populate centers before distances can be calculated!")
    #
    #     # index = self.data_frame.index
    #     # column_dict = {}
    #     #
    #     # # for i in index:
    #     # #     column_dict[i] = self.get_dist_list(self.data_frame.iloc[i,:])
    #     #
    #     # for i in list(range(self.k)):
    #     #     # print ("center ",self.centers.iloc[1, :])
    #     #     # print("df ", self.data_frame.iloc[1:,:])
    #     #     column_dict[i] = self.get_dist_list(
    #     #         self.centers.iloc[i, :].values, self.data_frame.iloc[1:,:])
    #     #
    #     # self.distance_matrix = DataFrame(
    #     #     column_dict, columns=list(range(self.k)))
    #     print ("before")
    #     # self.distance_matrix
    #     # self.distance_matrix()


    def _get_clusters(self):
        if self.distance_matrix is None:
            raise Exception(
                "Must compute distances before closest centers can be calculated")

        min_distances = self.distance_matrix.min(axis=1)

        # We need to make sure the index
        min_distances.index = list(range(self.numRows))

        cluster_list = [boolean_series.index[j]
                        for boolean_series in
                        [
                            self.distance_matrix.iloc[i,
                                                      :] == min_distances.iloc[i]
                            for i in list(range(self.numRows))
                        ]
                        for j in list(range(self.k))
                        if boolean_series[j]
                        ]


        self.clusters = Series(cluster_list, index=self.data_frame.index)
        # print("cluster_list ", self.clusters)

    def _compute_new_centers(self):
        if self.centers is None:
            raise Exception("Centers not initialized!")

        if self.clusters is None:
            raise Exception("Clusters not computed!")

        for i in list(range(self.k)):
            self.centers.ix[i, :] = self.data_frame[
                self.columns].ix[self.clusters == i].mean()

    def cluster(self):

        self._populate_initial_centers()
        self._compute_distances()
        self._get_clusters()

        counter = 0

        while True:
            counter += 1

            self.previous_clusters = self.clusters.copy()

            self._compute_new_centers()
            self._compute_distances()
            self._get_clusters()

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



