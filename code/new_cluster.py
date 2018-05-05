import pyspark
from pyspark.mllib.linalg import *
import numpy as np
from pandas import Series,DataFrame
import random
from pyspark import SparkConf,SparkContext
from pyspark.sql import SQLContext
# sc = pyspark.SparkContext()

# v = sc.textFile('hdfs:///data/test.csv')\
#     .map(lambda line: line.split(","))\
#     .filter(lambda line: line[4]!='NULL') \
#     .map(lambda line: (line[0],[line[1], line[3], line[4],line[5]]))#.collect()
# vl = v.map(lambda i:DenseVector(i[1]))
# index_vl = v.map(lambda i:(int(i[0]),DenseVector(i[1])))
#
# k = 3
# clusters = []       #contain several dense vectors that is choosen to be centroid
# '''for test purpose'''
#
# met = np.array([[ 7.40287431e-07, -1.15234740e-07, -3.16733397e-07, -1.23115312e-08],
#                  [-1.15234740e-07,  1.92350266e-06, -8.96508054e-08,  5.49038595e-09],
#                  [-3.16733397e-07, -8.96508054e-08,  6.13053227e-06, -7.91933304e-08],
#                  [-1.23115312e-08,  5.49038595e-09, -7.91933304e-08, 2.04514885e-06]])
# b_met = sc.broadcast(met)   #broadcast met,access value by b_met.value
# b_row = sc.broadcast(vl.count())    #broadcast row numbers

def get_dist_single(ele, centroid):         #conpute point-wise distance with index
    # cls = clusters
    M = b_met.value
    l = []
    x = ele[1]
    index = ele[0]
    Z = x - centroid
    dist = np.sqrt((Z.dot(M).dot(Z.T)))
    l.append((float(index),dist))
    return l

def grab_random_point():  # get values of an row
    index = np.random.random_integers(0, b_row.value - 1)
    centroid = index_vl.filter(lambda x: x[0] == index)
    while (len(centroid.collect())==0):
        index = np.random.random_integers(0, b_row.value - 1)
        centroid = index_vl.filter(lambda x: x[0] == index)
    clusters.append(centroid.collect()[0][1])

def merge_dis(l_rdd, d1):        #merge distances
    total_d = d1
    for i in l_rdd:
        i.collect()
        total_d = total_d.union(i)
    # z = total_d.map(lambda i: min(i[1]))
    z = total_d.groupByKey()
    z.collect()
    d = z.map(lambda x: (x[0], min(x[1])))
    return d

def populate_initial_centers():
    # distances = None
    grab_random_point()
    l_rdd = []
    while len(clusters) < k:
        length = len(clusters)
        distances = index_vl.flatMap(lambda j: get_dist_single(j, clusters[length - 1]))
        '''array / array'''
        if length == 1:
            d1 = distances
            distances = distances.mapValues(lambda x: x**2)
            s = distances.values().sum()
            normalized_distances = distances.mapValues(lambda x: x / s)
            # normalized_distances = distances / s
        else:
            l_rdd.append(distances)
            dis = merge_dis(l_rdd, d1)
            """test"""
            # for i in l_rdd:
            #     i.collect()
            #     # print (list(total_d.collect()[0][1]))
            #     total_d = total_d.union(i)
                # print(list(total_d.collect()[0][1]))
            # z = total_d.groupByKey()
            # z.collect()
            """test end"""
            dis = dis.mapValues(lambda x: x ** 2)
            s = dis.values().sum()
            # normalized_distances = dis / s
            normalized_distances = dis.mapValues(lambda x: x / s)
            """b = a.union(e)
            c = b.groupByKey()
            d = c.map(lambda x: (x[0], min(x[1])))"""
        weights = normalized_distances.sortByKey()
        '''May crash the program, may sort the array and get top 1000'''
        try:
            index = np.random.choice(b_row.value,size=1, replace=False, p=weights.values().collect())
            # index = random.choices(range(0, b_row.value), weights=weights.values().collect(), k=1)
            centroid = index_vl.filter(lambda x: x[0] == index)
            clusters.append(centroid.collect()[0][1])
        except IndexError:
            try:
                index = np.random.choice(b_row.value, size=1, replace=False, p=weights.values().collect())
                # index = random.choices(range(0, b_row.value), weights=weights.values().collect(), k=1)
                centroid = index_vl.filter(lambda x: x[0] == index)
                clusters.append(centroid.collect()[0][1])
            except IndexError:
                grab_random_point()

def simply_merge(l_rdd):
    total_d = l_rdd[0]
    for i in range(1,len(l_rdd)):
        total_d = total_d.union(l_rdd[i])
    return total_d
    # z = total_d.map(lambda i: min(i[1]))
    # z = total_d.groupByKey()
    # d = z.map(lambda x: (x[0], min(x[1])))


def get_dist_index(ele, centroid_list, k):      #line 1
    # cls = clusters
    M = b_met.value
    l = []
    x = ele[1]
    index = ele[0]
    Z = x - centroid_list[k]
    dist = np.sqrt((Z.dot(M).dot(Z.T)))
    # l.append((float(index), dist))
    l.append(((float(index),float(k)),dist))
    return l

def compute_distances():
    # l_rdd = [0]*b_row.value
    distances = index_vl.flatMap(lambda j: get_dist_index(j, clusters, 0))
    # l_rdd[0] = distances
    for i in range(1,k):
        # index_vl.flatMap(lambda j: get_dist_index(j, clusters, i)).collect()
        # l_rdd.append(index_vl.flatMap(lambda j: get_dist_index(j, clusters, co)))
        d = index_vl.flatMap(lambda j: get_dist_index(j, clusters, i))
        # l_rdd[i] = d
        # distances = l_rdd[0]
        # d.first()
        distances = distances.union(d)
    return distances
# d_mat = simply_merge(l_rdd)
        # return d_mat

# def compute_distances():
#     l_rdd = []
#     for co in range(k):
#         # distances = index_vl.flatMap(lambda j: get_dist_single(j, clusters[k]))
#         distances = index_vl.flatMap(lambda j: get_dist_index(j, clusters, co))
#         l_rdd.append(distances)
#     d_mat = simply_merge(l_rdd)
#     return d_mat

# def compute_distances():
# l_rdd = [0]*b_row.value
# distances = index_vl.flatMap(lambda j: get_dist_index(j, clusters, 0))
# l_rdd[0] = distances
# for i in range(1,k):
#     # index_vl.flatMap(lambda j: get_dist_index(j, clusters, i)).collect()
#     # l_rdd.append(index_vl.flatMap(lambda j: get_dist_index(j, clusters, co)))
#     d = index_vl.flatMap(lambda j: get_dist_index(j, clusters, i))
#     l_rdd[i] = d
#     d.first()
#     distances.union(d)
    # distances.first()
    # l_rdd.append(distances)
# l_rdd = [0]*k
'''spark is lazy!!!'''
# l_rdd = []
# for i in range(k):
#     # l_rdd.append(index_vl.flatMap(lambda j: get_dist_index(j, clusters, co)))
#     distances = index_vl.flatMap(lambda j: get_dist_index(j, clusters, i))
#     distances.first()
#     l_rdd.append(distances)
    # distances.take(1)
    # distances.collect()
    # l_rdd[co] = distances
    # print (distances.collect())
    # distances = index_vl.flatMap(lambda j: get_dist_single(j, clusters[k]))
    # distances = index_vl.flatMap(lambda j: get_dist_index(j, clusters, co))

    # d_mat = simply_merge(l_rdd)
    # return d_mat


# def map_min(i, dis):
#     c = d.map(lambda x: (x[0][0], x[1])).groupByKey().map(lambda x: (x[0], min(x[1]))) #minimun distance
#     p = sc.parallelize([t for t in range(k)])
#     q = c.cartesian(p)
#     z = q.map(lambda x: ((x[0][0], x[1]), x[0][1])) #index with minimum distance
#     z = q.map(lambda x: (x[0][0], x[1]))    #only index
#     a = d.intersection(z)       #index

def get_clusters(d):
    c = d.map(lambda x: (x[0][0], x[1])).groupByKey().map(lambda x: (x[0], min(x[1])))  # minimun distance
    p = sc.parallelize([t for t in range(k)])
    q = c.cartesian(p)
    z = q.map(lambda x: ((x[0][0], x[1]), x[0][1]))  # index with minimum distance,x[0][0] is sample
    # z = q.map(lambda x: (x[0][0], x[1]))  # only index          x[1] is the nth cluster
    a = d.intersection(z)  # index like (1,2,3.546) means sample 1 belongs to cluster 2, distance is 3.54
    return a
    # for i in range(b_row.value):
    #     c = d.filter(lambda j: j[0][0] == i)
    #     z = c.map(lambda x: x[1])       #form a list to store distances
    #     z.takeOrdered(1)
    # if self.distance_matrix is None:
    #     raise Exception(
    #         "Must compute distances before closest centers can be calculated")
    #
    # min_distances = self.distance_matrix.min(axis=1)
    #
    # # We need to make sure the index
    # min_distances.index = list(range(self.numRows))
    #
    # cluster_list = [boolean_series.index[j]
    #                 for boolean_series in
    #                 [
    #                     self.distance_matrix.iloc[i,
    #                                               :] == min_distances.iloc[i]
    #                     for i in list(range(self.numRows))
    #                 ]
    #                 for j in list(range(self.k))
    #                 if boolean_series[j]
    #                 ]
    #
    #
    # self.clusters = Series(cluster_list, index=self.data_frame.index)
    # # print("cluster_list ", self.clusters)

def compute_new_centers(a):
    x = a.map(lambda x: x[0])
    q = index_vl.join(x)
    new_cen = [0]*k
    for i in range(k):
        new_cen[i] = q.filter(lambda x:x[1][1]==i).map(lambda x:x[1][0]).mean()
    return new_cen
    # (1, (DenseVector([313401.0, 83237.0, 1.0, 87331.0]), 1.0))
    # if self.centers is None:
    #     raise Exception("Centers not initialized!")
    #
    # if self.clusters is None:
    #     raise Exception("Clusters not computed!")
    #
    # for i in list(range(self.k)):
    #     self.centers.ix[i, :] = self.data_frame[
    #         self.columns].ix[self.clusters == i].mean()


conf = SparkConf()
#conf.set("spark.executor.memory","2460m")
#conf.set("spark.executor.memory","3g")
# conf.set("spark.speculation", "True")
sc = SparkContext(conf = conf)
# v = sc.textFile('hdfs:///data/ad_feature.csv') \
v = sc.textFile('hdfs:///data/ad_f_train.csv') \
    .map(lambda line: line.split(",")) \
    .filter(lambda line: line[5] != 'NULL') \
    .map(lambda line: (int(line[0]), line[1], [line[3], line[4], line[5]]))  # .collect()
# v = sc.textFile('hdfs:///data/ad_feature.csv') \
#     .map(lambda line: line.split(",")) \
#     .filter(lambda line: line[4] != 'NULL') \
#     .map(lambda line: (line[0], [line[3], line[4], line[5]]))  # .collect()
vl = v.map(lambda i: DenseVector(i[2]))
index_vl = v.map(lambda i: (i[0], DenseVector(i[2])))
index_vl.cache()
#index_vl.cache(pyspark.Storagelevel.MEMORY_AND_DISK)
max_iterations = 33
k = 20
#k = 18
clusters = []  # contain several dense vectors that is choosen to be centroid
'''for test purpose'''
# met = np.array([[7.40287431e-07, -1.15234740e-07, -3.16733397e-07, -1.23115312e-08],
#                 [-1.15234740e-07, 1.92350266e-06, -8.96508054e-08, 5.49038595e-09],
#                 [-3.16733397e-07, -8.96508054e-08, 6.13053227e-06, -7.91933304e-08],
#                 [-1.23115312e-08, 5.49038595e-09, -7.91933304e-08, 2.04514885e-06]])
met = np.array([[ 1.39120240528e-06, -7.11964361751e-08, 1.68554275438e-07],
                [-7.1196436173e-08, 4.18367212413e-06, -2.45888145316e-07],
                [1.6855427544e-07, -2.45888145311e-07, 1.43614586304e-06]])
row_num = vl.count()
b_met = sc.broadcast(met)  # broadcast met,access value by b_met.value
b_row = sc.broadcast(row_num)  # broadcast row numbers
populate_initial_centers()
# compute_distances()
d = compute_distances()
a = get_clusters(d)
counter = 0
while True:
    counter += 1
    previous_clusters = clusters
    print ("counter: ",counter)
    print("Previous ",previous_clusters)
    clusters = compute_new_centers(a)
    print (clusters)
    d = compute_distances()
    a = get_clusters(d)
    if counter >= max_iterations:
        break
    # elif clusters == previous_clusters:
    #     break

sse = d.map(lambda x:x[1]**2).sum()

x = a.map(lambda x: (x[0][0], float(x[0][1])))
# v = sc.textFile('hdfs:///data/test.csv') \
#     .map(lambda line: line.split(",")) \
#     .filter(lambda line: line[4] != 'NULL') \
#     .map(lambda line: (int(line[0]), line[1],))
p = v.join(x)
q = p.map(lambda x: x[1])
sqlContext = SQLContext(sc)
df = sqlContext.createDataFrame(q, ['ad_id', 'cluster'])
df.repartition(1).write.csv(path="/data/op_clu_train20", header=True)
# c = sc.parallelize(clusters).map(lambda x: str(x)[1:-1])
clusters.append(np.array([sse, 0, 0]))
t = zip(range(k+1), clusters)
text = sc.parallelize(list(t))
text.repartition(1).saveAsTextFile("/data/clu_result_train20")
#cen = DataFrame.from_items(t,range(k+1),'index')
#df_cen = sqlContext.createDataFrame(cen, ['campaign_id', 'customer', 'brand'])
#df_cen.repartition(1).write.csv(path="/data/op_cen2", header=True)
