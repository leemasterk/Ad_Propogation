#!/usr/bin/env python
import subprocess


#subprocess.run(["ls", "-l"])
#subprocess.call(["ls", "-l"])
#subprocess.call(["ls", "-a"])
subprocess.call(["ssh", "-t", "hduser@student22-x1", "sudo sysctl -w vm.drop_caches=3"])
subprocess.call(["ssh", "-t", "hduser@student22-x2", "sudo sysctl -w vm.drop_caches=3"])
subprocess.call(["ssh", "-t", "hduser@student21-x1", "sudo sysctl -w vm.drop_caches=3"])
subprocess.call(["ssh", "-t", "hduser@student23-x1", "sudo sysctl -w vm.drop_caches=3"])
subprocess.call(["ssh", "-t", "hduser@student23-x2", "sudo sysctl -w vm.drop_caches=3"])
subprocess.call(["ssh", "-t", "hduser@student50-x1", "sudo sysctl -w vm.drop_caches=3"])
subprocess.call(["ssh", "-t", "hduser@student50-x2", "sudo sysctl -w vm.drop_caches=3"])
subprocess.call(["ssh", "-t", "hduser@student21-x2", "sudo sysctl -w vm.drop_caches=3"])
#subprocess.run(["sudo sysctl -w vm.drop_caches=3"])
subprocess.call(["sudo", "sysctl", "-w", "vm.drop_caches=3"])




