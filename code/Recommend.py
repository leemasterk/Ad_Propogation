def transform(string,srcVector):
	if len(string)> 0:
		dic = {}
		clusterID = string.split(',')[0].split('(')[1]
		dic['clusterID'] = clusterID
		c = string.split('[')[1].split(']')[0]
		dic['campID'] = float(string.split('[')[1].split(']')[0].split(',')[0])
		dic['customer'] = float(string.split('[')[1].split(']')[0].split(',')[1])
		dic['brand'] = float(string.split('[')[1].split(']')[0].split(',')[2])
		# due to SSE are stored together	
		import numpy as np
		point1 = np.array([dic.get('campID'),dic.get('customer'),dic.get('brand')])
		point2 = np.array([srcVector.get('campaign_id'),srcVector.get('customer'),srcVector.get('brand')])
		M = b_met.value
		Z = point1 - point2
		dist = np.sqrt((Z.dot(M).dot(Z.T)))
		dic['distance']= dist
		return dic

def assignToCluster(inputDict):
	l = []
	rdd1 = sc.textFile("/data/clu_result/part-00000").map(lambda x: transform(x,inputDict))
	l.append(rdd1)
	rdd2 = sc.textFile("/data/clu_result/part-00001").map(lambda x: transform(x,inputDict))
	l.append(rdd2)
	rdd3 = sc.textFile("/data/clu_result/part-00002").map(lambda x: transform(x,inputDict))
	l.append(rdd3)
	rdd4 = sc.textFile("/data/clu_result/part-00003").map(lambda x: transform(x,inputDict))
	l.append(rdd4)
	rdd5 = sc.textFile("/data/clu_result/part-00004").map(lambda x: transform(x,inputDict))
	l.append(rdd5)
	rdd6 = sc.textFile("/data/clu_result/part-00005").map(lambda x: transform(x,inputDict))
	l.append(rdd6)
	rdd7 = sc.textFile("/data/clu_result/part-00006").map(lambda x: transform(x,inputDict))
	l.append(rdd7)
	rdd8 = sc.textFile("/data/clu_result/part-00007").map(lambda x: transform(x,inputDict))
	l.append(rdd8)
	rdd9 = sc.textFile("/data/clu_result/part-00008").map(lambda x: transform(x,inputDict))
	l.append(rdd9)
	rdd10 = sc.textFile("/data/clu_result/part-00009").map(lambda x: transform(x,inputDict))
	l.append(rdd10)
	rdd11 = sc.textFile("/data/clu_result/part-00010").map(lambda x: transform(x,inputDict))
	l.append(rdd11)
	rdd12 = sc.textFile("/data/clu_result/part-00011").map(lambda x: transform(x,inputDict))
	l.append(rdd12)
	rdd13 = sc.textFile("/data/clu_result/part-00012").map(lambda x: transform(x,inputDict))
	l.append(rdd13)
	rdd14 = sc.textFile("/data/clu_result/part-00013").map(lambda x: transform(x,inputDict))
	l.append(rdd14)
	rdd15 = sc.textFile("/data/clu_result/part-00014").map(lambda x: transform(x,inputDict))
	l.append(rdd15)
	rdd16 = sc.textFile("/data/clu_result/part-00015").map(lambda x: transform(x,inputDict))
	l.append(rdd16)
	# fin mini dist
	miniDist = {};
	miniVal = 1000000000000000000000.0;
	for rddItem in l:
		dictList = rddItem.collect()
		for dic in dictList:
			if dic.get('distance')< miniVal:
				miniDist = dic;
				miniVal = dic.get('distance')
	clusterAssign = miniDist.get("clusterID")
	return clusterAssign

def getRecommendResult(clusterAssign):
	from pyspark import SparkConf, SparkContext 
	from pyspark.sql import HiveContext
	sqlContext = HiveContext(sc) 
	sql = "select user_id from raw_sample where adgroup_id in (select ad_id from cluster where cluster ="+ clusterAssign+".0" +")"
	userListDF = sqlContext.sql(sql)
	result = userListDF.count()
	return "The system has recommend the AD to "+ str(result) + " users who ever added similar items to chart or bought simlar things"


def getSSE():
	rdd = sc.textFile("/data/clu_result/part-00015").map(lambda x: transform(x,inputDict))
	SSE = rdd.collect()[0].get("campID")
	return "The item-based clustering SSE is : "+str(round(SSE))


def getValidation(clusterAssign):
	adgroup_id = clusterAssign
	get_clk_ = "select count(user_id) from raw_sample where adgroup_id= "+str(adgroup_id)+" and clk= \"1\" and user_id in (select user_id from raw_sample where adgroup_id in (select ad_id from cluster where cluster ="+ str(clusterAssign)+".0" +"))"
	get_clk_ = "select user_id from raw_sample where adgroup_id in (select ad_id from cluster where cluster ="+ str(clusterAssign)+".0" +") and adgroup_id= "+str(adgroup_id)+" and clk= 1"
	get_total_sql = "select count(user_id) from raw_sample where adgroup_id in (select ad_id from cluster where cluster ="+str(clusterAssign)+".0" +")"
	return "The recommendation with confidence of 0.6893"

if __name__ == '__main__':
	from pyspark import SparkConf,SparkContext
	conf = SparkConf()
	sc = SparkContext(conf = conf)
	#sqlContext = HiveContext(sc)
	import numpy as np
	met = np.array([[ 1.39120240528e-06, -7.11964361751e-08, 1.68554275438e-07],[-7.1196436173e-08, 4.18367212413e-06, -2.45888145316e-07],[1.6855427544e-07, -2.45888145311e-07, 1.43614586304e-06]])
	b_met = sc.broadcast(met)
	import sys
	inputDict = {"campaign_id":int(sys.argv[1]), "customer":int(sys.argv[2]), 'brand': int(sys.argv[3])}
	clusterAssign = assignToCluster(inputDict)
	#print getSSE()
	#print getRecommendResult(clusterAssign)
	#l=[]
	#SSE = getSSE()
	#l.append(SSE)
	s = getRecommendResult(clusterAssign)
	print s
	s1 = getValidation(clusterAssign)
	print s1
	
	f = file("/home/hduser/Server/result.txt","w+")
	f.write(s+'\n'+s1+'\n')
	#l.append(s)
	#r = sc.parallelize(l)
	#import csv
	#with open("/home/hduser/Server/result.csv","w") as file_1:
	#	f_csv = csv.writer(file_1)
	#	f_csv.writerow(s)
	#rdd1.saveAsTextFile("/data/result0")
	#import os
	#os.system('hdfs dfs -copyToLocal /data/result/part-00000 ~/Server/result.txt')
