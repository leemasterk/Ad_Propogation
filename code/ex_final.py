import pyspark
from pyspark.mllib.linalg import *
import numpy as np
from pandas import Series,DataFrame
import random
from pyspark import SparkConf,SparkContext
from pyspark.sql import SQLContext

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
            dis = dis.mapValues(lambda x: x ** 2)
            s = dis.values().sum()
            # normalized_distances = dis / s
            normalized_distances = dis.mapValues(lambda x: x / s)
            """b = a.union(e)
            c = b.groupByKey()
            d = c.map(lambda x: (x[0], min(x[1])))"""
        weights = normalized_distances.sortByKey()
        index = np.random.choice(b_row.value, size=1, replace=False, p=weights.values().collect())
        centroid = index_vl.filter(lambda x: x[0] == index)
        clusters.append(centroid.collect()[0][1])
        '''May crash the program, may sort the array and get top 1000'''

def simply_merge(l_rdd):
    total_d = l_rdd[0]
    for i in range(1,len(l_rdd)):
        total_d = total_d.union(l_rdd[i])
    return total_d

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

def get_clusters(d):
    c = d.map(lambda x: (x[0][0], x[1])).groupByKey().map(lambda x: (x[0], min(x[1])))  # minimun distance
    p = sc.parallelize([t for t in range(k)])
    q = c.cartesian(p)
    z = q.map(lambda x: ((x[0][0], x[1]), x[0][1]))  # index with minimum distance,x[0][0] is sample
    # z = q.map(lambda x: (x[0][0], x[1]))  # only index          x[1] is the nth cluster
    a = d.intersection(z)  # index like (1,2,3.546) means sample 1 belongs to cluster 2, distance is 3.54
    return a

def compute_new_centers(a):
    x = a.map(lambda x: x[0])
    q = index_vl.join(x)
    new_cen = [0]*k
    for i in range(k):
        new_cen[i] = q.filter(lambda x:x[1][1]==i).map(lambda x:x[1][0]).mean()
    return new_cen

def main():
    conf = SparkConf()
    # conf.set("spark.executor.memory","3g")
    # conf.set("spark.speculation", "True")
    sc = SparkContext(conf = conf)
    v = sc.textFile('hdfs:///data/ad_f.csv') \
        .map(lambda line: line.split(",")) \
        .filter(lambda line: line[5] != 'NULL') \
        .map(lambda line: (int(line[0]), line[1], [line[3], line[4], line[5]]))  # .collect()
    vl = v.map(lambda i: DenseVector(i[2]))
    index_vl = v.map(lambda i: (i[0], DenseVector(i[2])))
    index_vl.cache(pyspark.storagelevel.MEMORY_AND_DISK)
    max_iterations = 33
    k = 10
    clusters = []  # contain several dense vectors that is choosen to be centroid
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

    sse = d.map(lambda x:x[1]**2).sum()

    x = a.map(lambda x: (x[0][0], float(x[0][1])))
    p = v.join(x)
    q = p.map(lambda x: x[1])
    sqlContext = SQLContext(sc)
    df = sqlContext.createDataFrame(q, ['ad_id', 'cluster'])
    df.repartition(1).write.csv(path="/data/op_clu", header=True)
    # c = sc.parallelize(clusters).map(lambda x: str(x)[1:-1])
    clusters.append(np.array([sse, 0, 0]))
    t = zip(range(k+1), clusters)
    cen = DataFrame.from_items(t,range(k),'index')
    df_cen = sqlContext.createDataFrame(cen, ['campaign_id', 'customer', 'brand'])
    df_cen.repartition(1).write.csv(path="/data/op_cen", header=True)
main()


def cluster(self):

    # self._populate_initial_centers()
    # self._compute_distances()
    # self._get_clusters()
    populate_initial_centers()
    # compute_distances()
    d = compute_distances()
    get_clusters()


    counter = 0

    while True:
        counter += 1

        self.previous_clusters = self.clusters.copy()

        self._compute_new_centers()
        self._compute_distances()
        self._get_clusters()

        if max_iterations is not None and counter >= max_iterations:
            break
        elif all(self.clusters == self.previous_clusters):
            break

    # if self.appended_column_name is not None:
    #     try:
    #         self.data_frame[self.appended_column_name] = self.clusters
    #     except:
    #         warnings.warn(
    #             "Unable to append a column named %s to your data." %
    #             self.appended_column_name)
    #         warnings.warn(
    #             "However, the clusters are available via the cluster attribute")


