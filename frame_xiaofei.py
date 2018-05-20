#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'standared mudule'

__author__ = 'Tree'

import numpy,os,csv
from sklearn.cluster import KMeans,AgglomerativeClustering
from sklearn import preprocessing

import FDandPicture
import poi_calcu
import trans_query_graph
from sklearn.metrics import silhouette_score

def get_graph(graph_path,graph_result):#从图结构得到网络结构
    f_r=open(graph_path,'r')
    all_lines=f_r.readlines()
    f_w=open(graph_result,'w+')
    for line in all_lines:
        line=line.strip(' ')
        if(line[0]=='v'):
            continue
        else:
            f_w.write(line[2]+' '+line[3]+' '+line[4]+'\n')
    f_r.close()
    f_w.close()


def kmeans_label(k,toBeClusteredFile,labelText):#根据降维后结果进行聚类
    kmean = KMeans(k)
    #col=[1,2,3,4]
    a = numpy.loadtxt(toBeClusteredFile)#,usecols=tuple(col))
    a_norm=preprocessing.normalize(a,norm='l2')
    result = kmean.fit_predict(a)
    numpy.savetxt(labelText, result, fmt='%d')

def test_kmeans_label(toBeClusteredFile,labelText):
    range_n_clusters = [i for i in range(6,11)]# clusters range you want to select
    a = numpy.loadtxt(toBeClusteredFile)
    a_norm = preprocessing.normalize(a, norm='l2')
    dataToFit = a_norm  # sample data
    best_clusters = 0  # best cluster number which you will get
    previous_silh_avg = 0.0

    for n_clusters in range_n_clusters:
        clusterer = KMeans(n_clusters=n_clusters)
        cluster_labels = clusterer.fit_predict(dataToFit)
        silhouette_avg = silhouette_score(dataToFit, cluster_labels)
        if silhouette_avg > previous_silh_avg:
            previous_silh_avg = silhouette_avg
            best_clusters = n_clusters

    # Final Kmeans for best_clusters
    kmeans = KMeans(n_clusters=best_clusters, random_state=0).fit_predict(dataToFit)
    numpy.savetxt(labelText, kmeans, fmt='%d')
    return  best_clusters

def ToIdLabel(verticeLabelText, labelOrderedFile, idText=''):#聚类结果的点表示成标准区域形式
    if idText!='':
        f_r1=open(idText,'r')
        all_line1 = f_r1.readlines()
        f_r2=open(verticeLabelText, 'r')
        f_w=open(labelOrderedFile, 'w')
        all_line2=f_r2.readlines()
        for i in range(len(all_line2)):
            line1=all_line1[i].strip()
            line1=line1.split(' ')
            id=int(line1[0])
            line2=all_line2[i].strip()
            line2=line2.split(' ')
            label=int(line2[0])
            f_w.write(str(id)+' ('+str(label)+' 1)\n')
        f_r2.close()
        f_r1.close()
        f_w.close()
    else:
        f_r=open(verticeLabelText, 'r')
        f_w=open(labelOrderedFile, 'w')
        allLine=f_r.readlines()
        for i in range(len(allLine)):
            label=allLine[i].strip().split()
            f_w.write(str(i)+' ('+label[0]+' 1)\n')
        f_w.close()
        f_r.close()


def Fdandpicture(labelOrderedText, fdValueFile):#绘图，得出poi值
    cluseter_region_path = labelOrderedText
    bbox_path = 'bbox_6.txt'
    convex_path = 'convex_6.txt'
    FDandPicture.default(bbox_path, convex_path)
    FDandPicture.draw_new_picture(cluseter_region_path)
    poi_type_file = r'region_poi.txt'
    FDandPicture.get_FD_value(cluseter_region_path, poi_type_file, fdValueFile)

def poi_cal(k, fdValueFile,excelResult):#得到熵值
    dic=poi_calcu.poi_calcu(k, fdValueFile)
    csvFile = open(excelResult, 'a+', newline='')
    writer = csv.writer(csvFile)
    for key in dic:
        writer.writerow([key, dic[key]])
    csvFile.close()

#get_graph(r'22015-9-7-11zaolabel.txt',r'traffic_network.txt')
if __name__=="__main__":
    graph_path=r'example\test.txt'
    graph_result_label=r'example\label_test.txt'
    verticeLabelText=r'example\vertive_label_test.txt'
    idLabel=r'example\vertice_label_ordered_test.txt'
    DF=r'example\DF_random9_vertice7_test.txt'
    excelResult=r'example\resultFiletest.csv'
    bestK=test_kmeans_label(graph_path,graph_result_label)
    #kmeans_label(7,graph_path,graph_result_label)
    #trans_query_graph.getVerticesClass(836,graph_result_label,verticeLabelText)
    ToIdLabel(graph_result_label,idLabel)
    Fdandpicture(idLabel,DF)
    poi_cal(bestK,DF,excelResult)

