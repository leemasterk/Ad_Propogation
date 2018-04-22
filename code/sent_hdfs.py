#!/usr/bin/env python
import subprocess


#subprocess.run(["ls", "-l"])
#subprocess.call(["ls", "-l"])
#subprocess.call(["ls", "-a"])
#l = ["hduser@student50-x1","hduser@student50-x2","hduser@student50-x3"]
#l = ["hduser@student23-x1","hduser@student23-x2","hduser@student50-x1","hduser@student50-x2", "hduser@student50-x3",]
#l = ["hduser@student22-x1","hduser@student22-x2","hduser@student23-x1","hduser@student23-x2","hduser@student50-x1","hduser@student50-x2", "hduser@student50-x3",]
#l = ["hduser@student21-x2"]
l = ["hduser@student22-x1","hduser@student22-x2","hduser@student23-x1","hduser@student23-x2","hduser@student50-x1","hduser@student50-x2", "hduser@student21-x2",
"hduser@student21-x1"]
#l = ["hduser@student22-x1","hduser@student22-x2","hduser@student23-x1","hduser@student23-x2","hduser@student21-x1","hduser@student50-x1","hduser@student50-x2", "hduser@student50-x3",]
for t in l:
	#subprocess.call(["scp", "/opt/hadoop-2.7.5/etc/hadoop/mapred-site.xml", "%s:/opt/hadoop-2.7.5/etc/hadoop"%t])
	subprocess.call(["scp", "/opt/hadoop-2.7.5/etc/hadoop/yarn-site.xml", "%s:/opt/hadoop-2.7.5/etc/hadoop"%t])
	#subprocess.call(["scp", "/opt/hadoop-2.7.5/etc/hadoop/core-site.xml", "%s:/opt/hadoop-2.7.5/etc/hadoop"%t])
	#subprocess.call(["scp", "/opt/hadoop-2.7.5/etc/hadoop/hdfs-site.xml", "%s:/opt/hadoop-2.7.5/etc/hadoop"%t])
#subprocess.call(["ssh", "-t", "hduser@student50-x3", "mkdir dfs_data"])
#subprocess.call(["ssh", "-t", "hduser@student22-x1", "mkdir dfs_data"])
