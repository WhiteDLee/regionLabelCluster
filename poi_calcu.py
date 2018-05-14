#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'standared mudule'

__author__ = 'Tree'
import math
import numpy as np
def poi_calcu(k,poi_path):
    f_r = open(r'poi_type.txt','r')
    all_lines = f_r.readlines()
    poi_types = []
    f_r.close()
    count=0
    dic={}
    for line in all_lines:
        if line.strip().split()[0]!='地名地址信息':
            poi_types.append(line.strip().split(' ')[0])
            count+=1
    tables=[ [] for i in range(k)]
    f_r2 = open(poi_path, 'r')
    sums=[]
    for i in range(k):
        line=f_r2.readline()
        if line=='':
            break
        key=int(line)
        sum=0
        for j in range(count+1):
            line=f_r2.readline().split(':')
            if line[0]!='地名地址信息':
                tables[i].append(float(line[1]))
                sum+=float(line[1])
        sums.append(sum)
    results=[]
    for i in range(k):
        result=0
        for j in range(count):
            if(tables[i][j]!=0):
                tables[i][j]=-tables[i][j]/sums[i]*math.log2(tables[i][j]/sums[i])
                result+=tables[i][j]
            else:
                tables[i][j]=0
        results.append(result)
    for i in range(k):
        dic[str(i)]=results[i]
    dic["maximun"]=max(results)
    dic["minimum"]=min(results)
    dic["d"]=max(results)-min(results)
    dic["mean"]=np.mean(results)
    dic["var"]=np.var(results)
    dic["result"]=dic["mean"]+dic["var"]
    return dic













