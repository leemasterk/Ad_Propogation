from kmeans_own_v1 import *
# from kmeans_own import *
# from distribute_test import *
import pandas as pd
import random
import numpy as np





data = pd.read_csv()
# d = data.iloc[:,:4]
# data = data.fillna(random.randint(461497,800000))
data = data.dropna(axis=0)

# print (data)
# sdfs
# d = data
data.astype(int)
d = data.iloc[:5,[2,3,4]]
print(d)
# d = data.iloc[:20,[2,3,4]]
# print(len(d))
# print(d)
# print (data['brand'].max())
# print (d)
kmpp = KMeansPlusPlus(d, 3, max_iterations=10)
# kmpp.populate_initial_centers()
# kmpp.test()
# kmpp.get_distance_matrix()
# kmpp.distance_matrix()
# kmpp.compute_distances()
kmpp.cluster()
# print (kmpp.distance_matrix)
# # kmpp.get_distance_matrix()
#
# # print ("df ",kmpp.data_frame)
print(type(kmpp.clusters))
print(type(kmpp.centers))
print (kmpp.clusters)
print ("center ",kmpp.centers)
clu = kmpp.clusters.to_frame()
print(type(clu))
# clu.columns
clu.to_csv("cluster_result")
kmpp.centers.to_csv("centroid_result")
# print (type(kmpp.centers))
# print ("index ",kmpp.index)




