# Instructions on How to Run the Demo
## Tutorial of Installation

### Installation Steps
##### 1.Xen Installation
##### 2.VM Creation
##### 3.Hadoop Installation
##### 4.Spark Installation
##### 5.Hive Installation
---
### 1.Xen Installation


First of all, enter these command to upgrade your environment.

```
sudo apt-get update

sudo apt-get upgrade
```

Then Install a 64-bit Xen-hypervisor

`sudo apt-get install xenhypervisor-amd64`

Type “Y” for confirmation if asked

 Install vim (Vi Improved, recommend). Should be installed already
 
`sudo apt-get install vim`

#### 1.1.Configure GRUB to start Xen

`sudo vim /etc/default/grub`

|Before  |         After         |
|-------|:------------------------------:|
|GRUB_DEFAULT=0 | GRUB_DEFAULT=**"Xen 4.4-amd64"**    |
| GRUB_HIDDEN_TIMEOUT=0   |  **#**GRUB_HIDDEN_TIMEOUT=0      |
|GRUB_CMDLINE_LINUX=""|GRUB_CMDLINE_LINUX=**"rebootdelay=100"**|

Save changes and update.

`sudo update-grub`

#### 1.2.Network configuration

`sudo vim /etc/network/interfaces`

|Before  |         After         |
|-------|:------------------------------:|
|iface eth0 inet dhcp|iface eth0 inet **manual**   |
Adding below. (Be carefull, the third line starts with a TAB)
```
auto xenbr0
iface xenbr0 inet dhcp
    bridge_ports eth0
```
Save changes then reboot

`sudo reboot`

After reboot, check the network.

`sudo xl list`
You should see **Domain-0** is running

Enter`ifconfig` then remember **xenbr0's inet address** 

#### 1.3.Install Xen Utilities

`sudo apt-get install xen-utils-4.4 xenwatch xen-tools xen-utils-common
xenstore-utils virtinst virt-viewer virt-manager`

Type “Y” for confirmation

#### 1.4.Hypervisor Configuration
`sudo vim /etc/xen/xend-config.sxp`

|Before  |         After         |
|-------|:------------------------------:|
|#(xend-unix-server no)|(xend-unix-server **yes**)|
Fianlize the settings
```
sudo mkdir /home/xen/
sudo chmod 777 -R /home/xen 
sudo ln -s /usr/lib/xen-4.4 /usr/lib/xen
```
---
### 2.VM Creation

#### 2.1.Set Default Virtual Machine Configuration
`sudo vim /etc/xen-tools/xen-tools.conf`

|Parameter  |         Value         |
|-------|:------------------------------:|
|dir | /home/xen    |
| size   |        50G         |
|memory| 4096MB (for 16GB Memory Machine) / 2048MB (for 8GB Memory Machine) |
|swap|8192MB|

`sudo vim /etc/xen-tools/xen-tools.conf`

|Parameter  |         Value         |
|-------|:------------------------------:|
|gateway | **10.42.0.1**    |
| netmask   |       **255.255.254.0**        |
|broadcast | **10.42.0.255** |
|dhcp|**1**|
|nameserver|**10.42.0.1**|
|bridge|**xenbr0**|
|mirror|**http://hk.archive.ubuntu.com/ubuntu**|
#### 2.2.Creating VMs
`sudo xen-create-image --hostname=studentxx-x1`
(**Replace _studentxx_ with your own host name**)

Wait a while for the creation.

When it finishes, remember the **Root Password** in the installtion Summary

#### 2.3.Configure your VM
`sudo vim /etc/xen/studentxx-x1.cfg`
(**Replace _studentxx_ with your own host name**)

|Parameter  |         Value         |
|-------|:------------------------------:|
|vif | ***The assigned MAC of your VM***  |

#### 2.4.Start your VM

`sudo xl create /etc/xen/studentxx-x1.cfg -c`

(**Replace _studentxx_ with your own host name**)

Enter your **Root Password** to login. Exit by using "Ctrl+]".

#### 2.5.Connect to your VM
`sudo xl console studentxx-x1`
(**Replace _studentxx_ with your own host name**)

Login as root with **Root Password** then change your password.

`passwd`

Add a user account “student” for your new VM and give it sudo right

```
adduser student
sermod –a –G sudo student
```
Now you can use ssh to connect
`ssh student@studentxx-x1`(**Replace _studentxx_ with your own host name**)

### Repeat 2.2-2.5 to create studentxx-x2
#### 2.6.Cluster environment

Do it on all 4 machines of your group

Project Requirement:

• 2 VMs per physical machine (studentN-x1 + studentN-x2)

• 8 VMs in total to form a Hadoop cluster

---

### 3.Hadoop Installation

We will build a cluster on 4 machines, with 1 Master Node (on Dom0, RM + NN) + 8 Salve Nodes (on VMs, NM + DN)

|VM  |         Role         |
|-------|:------------------------------:|
|Dom0 on leader machine | Master Node, NameNode+ResourceManager   |
| All x1,x2   |       Slave Node, DataNode+NodeMageger         |

#### 3.1.Pre-requisites
 
• Disabling IPv6

`sudo vim /etc/sysctl.conf`

Adding at the end of the file: 
```
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
```
**Need to do this step on all vms.**
Then reboot your machine.

• Set up all VMs
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install nano
```
• Install utilities: software-properties-common etc. **(on All VMs)**

`sudo apt-get install software-properties-common python-software-properties`

• Install Java on all VMs
```
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
```

• Setup working environment on all VMs: e.g., JAVA_HOME variable set
to the path where JDK is installed

`sudo nano /etc/profile`

Adding to the end of file:
```
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=$CLASSPATH:$JAVA_HOME/lib:$JAVA_HOME/jre/lib
export PATH=$PATH:$JAVA_HOME/bin:$JAVA_HOME/jre/bin

```

• Create a Hadoop user “hduser”, and user group “hadoop” on all VMs
```
sudo addgroup hadoop
sudo adduser --ingroup hadoop hduser    
```
• Grant root access on all VMs for “hduser” as all the steps should ideally be performed by root user

`sudo usermod -a -G sudo hduser`

• Configuring SSH (allow access remote VMs without
password)

**Do on Only the Master Node machine (Dom0)**

Login as hduser.

First, generate key pair
`ssh-keygen -t rsa -P ""`

Add key to **All** nodes
```
ssh-copy-id hduser@studentX(Dom0)
ssh-copy-id hduser@studentX-x1
ssh-copy-id hduser@studentX-x2
ssh-copy-id hduser@studentY-x1
ssh-copy-id hduser@studentY-x2
ssh-copy-id hduser@studentZ-x1
ssh-copy-id hduser@studentZ-x2
ssh-copy-id hduser@studentN-x1
ssh-copy-id hduser@studentN-x2
```

• Test SSH connection
Try to connect to all slaves once
```
ssh studentX
ssh studentX-x1
ssh studentX-x2
ssh studentY-x1
ssh studentY-x2
ssh studentZ-x1
ssh studentZ-x2
ssh studentN-x1
ssh studentN-x2

```
Make sure you can connect to all the VMs
without entering a password
#### 3.2.Configure Hadoop on Matser Node
##### 3.2.1. Download Hadoop

We will install Hadoop at folder /opt

`cd /opt`

 Download hadoop-2.7.5. Extract the file, then change the owner of the extracted files

```
sudo wget https://archive.apache.org/dist/hadoop/core/hadoop-2.7.5/hadoop-2.7.5.tar.gz
sudo tar zxvf hadoop-2.7.5.tar.gz
sudo chown -R hduser:hadoop hadoop-2.7.5
```
####Remember all the Hadoop installation steps should be done under "hduser"
##### 3.2.2. Setup environment
**Modify hadoop-env.sh**

`nano /opt/hadoop-2.7.5/etc/hadoop/hadoop-env.sh`

Modify
```
# The java implementation to use.
export JAVA_HOME=${JAVA_HOME}
```

to
```
# The java implementation to use.
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export HADOOP_HOME=/opt/hadoop-2.7.5
export HADOOP_CONF_DIR=/opt/hadoop-2.7.5/etc/hadoop
```

**Modify core-site.xml**

`nano /opt/hadoop-2.7.5/etc/hadoop/core-site.xml`

Modify
```
<configuration>
</configuration>
```

to **(Change "studentX" to your master node)**
```
<configuration>
<property>
<name>fs.defaultFS</name>
<value>hdfs://studentX:9000</value>
</property>
<property>
<name>hadoop.tmp.dir</name>
<value>/var/hadoop/hadoop-${user.name}</value>
</property>
</configuration>
```


**Modify hdfs-site.xml**

`nano /opt/hadoop-2.7.5/etc/hadoop/hdfs-site.xml`

Modify
```
<configuration>
</configuration>
```

to
```
<configuration>
<property>
<name>dfs.replication</name>
<value>2</value>
</property>
<property>
<name>dfs.blocksize</name>
<value>64m</value>
</property>
</configuration>
```
**Modify mapred-site.xml**

Create mapred-site.xml from template then edit it.
```
cp /opt/hadoop-2.7.5/etc/hadoop/mapred-site.xml.template /opt/hadoop-2.7.5/etc/hadoop/mapred-site.xml
nano /opt/hadoop-2.7.5/etc/hadoop/mapred-site.xml
```

Modify
```
<configuration>
</configuration>
```

to
```
<configuration>
<property>
<name>mapreduce.framework.name</name>
<value>yarn</value>
</property>
<property>
<name>mapreduce.map.memory.mb</name>
<value>200</value>
</property>
<property>
<name>mapreduce.reduce.memory.mb</name>
<value>300</value>
</property>
</config
```
**Modify yarn-site.xml**

`nano /opt/hadoop-2.7.5/etc/hadoop/yarn-site.xml`

Modify
```
<configuration>
</configuration>
```

to **(Change "studentX" to your master node)**
```
<configuration>
<property>
<name>yarn.resourcemanager.hostname</name>
<value>studentX</value>
</property>
<property>
<name>yarn.nodemanager.aux-services</name>
<value>mapreduce_shuffle</value>
</property>
</configuration>
```
#### 3.3.Install Hadoop (Do it on Master Node)
##### 3.3.1. Configure Master Node and Slave Nodes

Master Node: `nano /opt/hadoop-2.7.5/etc/hadoop/masters`

Modify to:

`studentX`

Slave Node: `nano /opt/hadoop-2.7.5/etc/hadoop/slaves`

Modify to (Replace the content by the names of
your VMs):
```
studentX-x1
studentX-x2
studentY-x1
studentY-x2
studentZ-x1
studentZ-x2
studentN-x1
studentN-x2
```
**Zip the Hadoop folder**
```
cd /opt
tar cvf ~/hadoop-7305.tar.gz hadoop-2.7.5
```
##### 3.3.2. Copy Hadoop package to all slave nodes

SSH to one of the slave nodes

`ssh studentX-x1`

 Copy Hadoop configuration files from the master node

`sudo scp hduser@studentX:hadoop-7305.tar.gz /opt`

Unzip Hadoop
```
cd /opt
sudo tar xvf hadoop-7305.tar.gz
```
Change owner

`sudo chown -R hduser:hadoop /opt/hadoop-2.7.5`



Setting up environment 
**(Still inside the slave node!)**

Edit /etc/profile

`sudo nano /etc/profile`

Add these at the end of the file:
```
export HADOOP_HOME=/opt/hadoop-2.7.5
export CLASSPATH=$CLASSPATH:$HADOOP_HOME/lib
export PATH=$PATH:$HADOOP_HOME/bin
export PATH=$PATH:$HADOOP_HOME/sbin
```
Create working directory

`sudo mkdir /var/hadoop`

Change owner

`sudo chown -R hduser:hadoop /var/hadoop`

**Repeat 3.3.2 steps on all slave nodes**

##### 3.3.3.Setting up environment for the master node

Now back to the master node.

**Edit /etc/profile in the same way as described in 3.3.2.**

Enforce change

`source /etc/profile`

Create working directory

`sudo mkdir /var/hadoop`

Change owner

`sudo chown -R hduser:hadoop /var/hadoop`

#### 3.4.Start Hadoop (All steps in Master Node)

Before starting the HDFS, we need to format the NameNode. Use the following command only on master node:

`hdfs namenode -format`

**Be careful !** If this command is executed again after
Hadoop has been used, your data previously
stored in HDFS will be gone (can not be found).

Starting the cluster
```
start-dfs.sh
start-yarn.sh
mr-jobhistory-daemon.sh start historyserver
```
Monitoring Hadoop by `jps`. You should see NodeNode+RecourseManager running on Master Node
and NodeManager+DataNode running on Slave Nodes.

Stopping cluster
```
stop-dfs.sh
stop-yarn.sh
mr-jobhistory-daemon.sh stop historyserver
```


---

### 4.Spark Installation

#### 4.1.Download and Configure Spark on Master Node
Download spark to /opt
```
cd /opt
wget https://www.apache.org/dyn/closer.lua/spark/spark-2.2.1/spark-2.2.1-bin-hadoop2.7.tgz

```
Extract files

`sudo tar xvf spark-2.2.1-bin-hadoop2.7.tgz`

Change file permission

`sudo chown -R hduser:hadoop ./spark-2.2.1-bin-hadoop2.7`

**Configure Spark – spark-env.sh**

Create the config file from the given template

`cp /opt/spark-2.2.1-bin-hadoop2.7/conf/sparkenv.sh.template /opt/spark-2.2.1-binhadoop2.7/conf/spark-env.sh`

Edit file

`sudo vim /opt/spark-2.2.1-binhadoop2.7/conf/spark-env.sh`

Adding the following lines (Depend on Hadoop)
```
HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
LD_LIBRARY_PATH=/opt/hadoop-2.7.5/lib/native:$LD_LIBRARY_PATH
```

**Configure Spark – spark-defaults.conf**

Create the config file from the given template

`cp /opt/spark-2.2.1-bin-hadoop2.7/conf/sparkdefaults.conf.template /opt/spark-2.2.1-bin-hadoop2.7/conf/spark-defaults.conf`

Edit file

`sudo vim /opt/spark-2.2.1-binhadoop2.7/conf/spark-defaults.conf`

Adding the following lines: **(Change "studentX" to your master node)**
```
spark.master spark://studentX:7077
spark.serializer org.apache.spark.serializer.KryoSerializer
spark.executor.instances 10
spark.eventLog.enabled true
spark.eventLog.dir hdfs://studentX:9000/tmp/sparkLog
spark.history.fs.logDirectory hdfs://studentX:9000/tmp/sparkLog
spark.yarn.archive hdfs://studentXX:9000/spark-archive.zip
```
Create folder for event log in HDFS

`hdfs dfs -mkdir /tmp/sparkLog`

#### 4.2.Copy Spark code to all other VMs

Zip the folder (on master)
```
cd /opt
tar cvf ~/spark-7305.tgz spark-2.2.1-bin-hadoop2.7
```

SSH to each slave nodes, and then copy the file through scp. Unzip the files then change file permission
. **(Do this in each of
the other VMs)**
```
sudo scp hduser@studentXX:spark-7305.tgz /opt
cd /opt
sudo tar xvf spark-7305.tgz
sudo chown -R hduser:hadoop /opt/spark-2.2.1-bin-hadoop2.7
```

#### 4.3.Running Spark on Master Node

`/opt/spark-2.2.1-bin-hadoop2.7/bin/spark-shell --master yarn`


---

### 5.Hive Installation

Download Hive then extract.

```
sudo wget http://apache.01link.hk/hive/hive-2.3.3/apache-hive-2.3.3-bin.tar.gz
tar zxvf apache-hive-2.3.3-bin.tar.gz
```
Copying files to /usr/local/hive directory

```
#sudo mv apache-hive-2.3.3-bin /usr/local/hive

```
Setting up environment for Hive
appending the following lines to **~/.bashrc** file:
```
export HIVE_HOME=/usr/local/hive
export PATH=$PATH:$HIVE_HOME/bin
export CLASSPATH=$CLASSPATH:/usr/local/Hadoop/lib/*:.
export CLASSPATH=$CLASSPATH:/usr/local/hive/lib/*:.
```

The following command is used to execute ~/.bashrc file.

`source ~/.bashrc`

**Configuring Hive**

To configure Hive with Hadoop, you need to edit the hive-env.sh file, which is placed in the $HIVE_HOME/conf directory. The following commands redirect to Hive config folder and copy the template file:
```
cd $HIVE_HOME/conf
cp hive-env.sh.template hive-env.sh
```
Edit the hive-env.sh file by appending the following line:

`export HADOOP_HOME=/usr/local/hadoop`

Hive installation is completed successfully. Now you require an external database server to configure Metastore. We use Apache Derby database.

---
