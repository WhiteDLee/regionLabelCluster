#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'standared mudule'

from copy import deepcopy
__author__ = 'Tree'
import numpy
from numpy import *
import numpy as np

from sklearn.manifold import TSNE
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def transQueryGraph(path):
    f_r=open(path,'r')
    f_w=open('trans_query_graph.txt','w+')
    allLine=f_r.readlines()
    seq=0
    result = [0 for x in range(0, 837)]
    result[836]=-1
    while seq<len(allLine):
        line=allLine[seq].strip().split()
        if line[0]=='t':
            seq+=1
            for i in range(836):
                result[i]=0
            line2=allLine[seq].strip().split()
            while line2[0]=='v':
                result[int(line2[1])]=1
                seq+=1
                line2=allLine[seq].strip().split()
            j=0
            restr=''
            while result[j]!=-1:
                restr=restr+str(result[j])+' '
                j+=1
            restr+='\n'
            f_w.write(restr)
        seq+=1
    f_r.close()
    f_w.close()

def getVerticesClass(numOfVertices,labelText,verticeLabelText):
    f_r1 = open('trans_query_graph.txt', 'r')
    f_r2=open(labelText,'r')
    allLine1=f_r1.readlines()
    allLine2=f_r2.readlines()
    allClass={}
    for i in range(numOfVertices):
        allClass[i]={}
    for i in range(len(allLine2)):
        label=int(allLine2[i].strip())
        line=allLine1[i].strip().split()
        for k in range(len(line)):
            if(int(line[k])>0):
                if label not in allClass[k]:
                    f=deepcopy(allClass[k])
                    f.update({label:1})
                    allClass.update({k:f})
                    allClass.update()
                else:
                    allClass[k][label]+=1
    result=[0]*numOfVertices
    num=0
    for key,value in allClass.items():
        max=-1
        verticeClass=-1
        if value:
            for t,v in value.items():
                if max<v:
                    verticeClass=t
        else:
            verticeClass=6
        result[key]=verticeClass
    f_w=open(verticeLabelText,'w+')
    for i in range(numOfVertices):
        f_w.write(str(result[i])+'\n')
    f_r1.close()
    f_r2.close()
    f_w.close()

def transGraphToMatrix(path):
    f_r = open(path, 'r')
    f_w = open('trans_query_graph_to_matrix.txt', 'w+')
    allLine = f_r.readlines()
    seq = 0
    result = []
    while seq < len(allLine):
        line = allLine[seq].strip().split()
        if line[0] == 't':
            print(str(line[2]))
            seq += 1
            result = [[0 for i in range(836)] for j in range(836)]
            line2 = allLine[seq].strip().split()
            while line2[0]=='v':
                seq += 1
                line2 = allLine[seq].strip().split()
            while line2[0] == 'e':
                result[int(line2[2])][int(line2[3])]=1
                seq+=1
                if seq<len(allLine):
                    line2 = allLine[seq].strip().split()
                else:
                    break
        for i in range(836):
            restr=''
            for j in range(836):
                restr=restr+str(result[i][j])+' '
            restr+='\n'
            f_w.write(restr)
    f_w.close()
    f_r.close()
    print("end")

def transGraphToMatrixAndtSNE(path):
    f_r = open(path, 'r')
    f_w = open('trans_query_graph_to_matrix2.txt', 'w+')
    allLine = f_r.readlines()
    seq = 0
    result = []
    while seq < len(allLine):
        line = allLine[seq].strip().split()
        if line[0] == 't':
            print(str(line[2]))
            seq += 1
            result = [[0 for i in range(836)] for j in range(836)]
            line2 = allLine[seq].strip().split()
            while line2[0]=='v':
                seq += 1
                line2 = allLine[seq].strip().split()
            while line2[0] == 'e':
                result[int(line2[2])][int(line2[3])]=1
                result[int(line2[3])][int(line2[2])] = 1
                seq+=1
                if seq<len(allLine):
                    line2 = allLine[seq].strip().split()
                else:
                    break
            matrix=np.array(result)
            matrix_embedded=TSNE(n_components=1).fit_transform(matrix)
            matrix_embedded=np.hstack((matrix_embedded))
            matrix_embedded=matrix_embedded.tolist()
        restr = ''
        for i in range(836):
            restr=restr+'{:.2f}'.format(matrix_embedded[i])+' '
        restr+='\n'
        f_w.write(restr)
    f_w.close()
    f_r.close()
    print("end")

#transGraphToMatrixAndtSNE('query_graph.txt')






