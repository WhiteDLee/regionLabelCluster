#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'standared mudule'

__author__ = 'Tree'
import scipy.cluster.hierarchy as sch
from sklearn.cluster import KMeans
import numpy
from sklearn import preprocessing
def get_test_graph(path):
    f_w=open(path,'w')
    a=[[1,0],[0,1],[1,1],[-1,1],[-1,0],[-1,-1],[0,-1]]
    for each in a:
        for i in range(120):
            s=str(each[0])+' '+str(each[1])+'\n'
            f_w.write(s)
    f_w.close()

def cluster_kernel(path):
    kernel_matrix=numpy.loadtxt(path)
    a_norm = preprocessing.normalize(kernel_matrix, norm='l2')
    points = kernel_matrix
    disMat = sch.distance.pdist(points,'euclidean')
    #进行层次聚类:
    Z=sch.linkage(disMat,method='average')
    #将层级聚类结果以树状图表示出来并保存为plot_dendrogram.png
    P=sch.dendrogram(Z)
    #plt.savefig('plot_dendrogram.png')
    #根据linkage matrix Z得到聚类结果:
    cluster = sch.fcluster(Z, 1, 'inconsistent')
    print("Original cluster by hierarchy clustering:\n",max(cluster))
    print('cluster size：',len(cluster))
    #kmeans = KMeans(6)
    #cluster = kmeans.fit_predict(points)
    #return cluster

#get_test_graph(r'example\test.txt')
cluster_kernel(r"example\graph_100_dim_toPointVectorWithEdges.txt")
