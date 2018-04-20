# -*- coding: utf-8 -*-
from SocketServer import ThreadingTCPServer, StreamRequestHandler 
import numpy as np
import traceback  
import struct
import json
import sys

class MyStreamRequestHandlerr(StreamRequestHandler): 

	
	def resolveJsonData(self,data):
		jdata = json.loads(data.decode("utf-8"))
		return jdata
	def handle(self):
		#from pyspark import SparkConf,SparkContext
		#conf = SparkConf()
		#sc = SparkContext(conf = conf)  
		while True:  
			try:
				data = self.rfile.readline().strip()
				jRequest = self.resolveJsonData(data)
				print "Data from client: ",jRequest

				inputDict = {"campaign_id":jRequest.get("campaign_id"), "customer":jRequest.get("customer"), 'brand': jRequest.get("brand")}
				#import numpy as np
				#met = np.array([[ 1.39120240528e-06, -7.11964361751e-08, 1.68554275438e-07],[-7.1196436173e-08, 4.18367212413e-06, -2.45888145316e-07],[1.6855427544e-07, -2.45888145311e-07, 1.43614586304e-06]])
				#b_met = sc.broadcast(met)
				#clusterAssign = assignToCluster(inputDict)
				#SSE = getSSE()
				#result = getRecommendResult(clusterAssign)
				import os
				os.system('/opt/spark-2.2.1-bin-hadoop2.7/bin/spark-submit --master yarn --deploy-mode client --driver-class-path /home/hduser/apache-hive-2.3.2-bin/lib/mysql-connector-java-5.1.24-bin.jar ~/Server/Recommend.py '+inputDict.get('campaign_id')+' '+inputDict.get('customer')+' '+ inputDict.get('brand'))
				file = "/home/hduser/Server/result.txt"
				with open(file,"r") as f:
    					t=f.readline()
					t1=f.readline()
				print t
				dict = {"response":" "+t+"\n "+t1+"\n"}
				dict["content"] = "Json"
				jdata = json.dumps(dict)
				self.wfile.write(str(jdata).encode())
				#print "send" 

			except:  
				traceback.print_exc()  
				break  

host = "localhost"  
port = 9999      
addr = (host, port)
server = ThreadingTCPServer(addr, MyStreamRequestHandlerr)  
print "server started at port 9999"
server.serve_forever()  
	


