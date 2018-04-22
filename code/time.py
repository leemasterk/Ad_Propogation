#!/usr/bin/env python
import subprocess

t = subprocess.check_output(["date"])
l_time = t.split(" ")
#print("t", time[3])
#print(time)
#subprocess.run(["ls", "-l"])
#subprocess.call(["ls", "-l"])
#subprocess.call(["ls", "-a"])
time = l_time[3]
#time = "19:05:50"
subprocess.call(["ssh", "-t", "hduser@student22-x1", "sudo date --set=%s"%time])
subprocess.call(["ssh", "-t", "hduser@student22-x2", "sudo date --set=%s"%time])
subprocess.call(["ssh", "-t", "hduser@student21-x1", "sudo date --set=%s"%time])
subprocess.call(["ssh", "-t", "hduser@student23-x1", "sudo date --set=%s"%time])
subprocess.call(["ssh", "-t", "hduser@student23-x2", "sudo date --set=%s"%time])
subprocess.call(["ssh", "-t", "hduser@student50-x1", "sudo date --set=%s"%time])
subprocess.call(["ssh", "-t", "hduser@student50-x2", "sudo date --set=%s"%time])
subprocess.call(["ssh", "-t", "hduser@student21-x2", "sudo date --set=%s"%time])
#subprocess.run(["sudo sysctl -w vm.drop_caches=3"])
subprocess.call(["sudo", "date", "--set=%s"%time])




