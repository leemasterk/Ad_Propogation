# GroupH Proposal
## Advertisement Propogation System

### Topic Description
In our project, we decide to **Predict** the target customers for Ad propagation by buliding an recommendation system which would employ Item-based **collaboratIve filtering**. The data we use is provided by Tianchi Big Data Competition, which covers 1.1 million users 8 days clicking behaviors under Ad propagation, and Ad & User basic information. How to recommend a specific Ad to potential target customers groups for better customers’ response is a question remained to be solved. Therefore, we propose this project to identify the potential target customers groups for advertisement, which is the actual requirement from business.

###Methodology
Since the size of the entire dataset after decompression is near 23GB, we decide to utilize Spark with Yarn and Hadoop. On the consideration of algorithm of recommenddation system, we proposed to use Item-based **collaboratIve filtering**. Specifically, we plan to calculate user-item utility matrix first and using **Clustering algorithm** to find the similar Ad. The recommended Ad will be mapped to users who have similar preference on commodities.

###Demo Plan 
The demo will be a web app recommendation system. User can input an ad info:

```
Input
* Target commodity name: 
* Target commodity brand:  
* Target commodity price:  
* Target target commodity brand:  
```
Then, recommended user info will be shown on web page with forcasting Click-through Rate (CTR) possibililty.

```
Output
* Ad is recommended to user with userID1 
* Ad is recommended to user with userID2  
* Ad is recommended to ...  
```

#### Reference 

[Mining of Massive Datasets ](http://i.stanford.edu/~ullman/mmds/book0n.pdf)by Jure Leskovec, Anand Rajaraman, and Jeff Ullman

Datasets could be found [here](https://tianchi.aliyun.com/datalab/dataSet.htm?spm=5176.100073.888.26.24d733d89cH58d&id=19).

