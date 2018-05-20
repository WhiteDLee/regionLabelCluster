#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'standared mudule'

__author__ = 'Tree'
def get_test_graph(path):
    f_w=open(path,'w')
    a=[[1,0],[0,1],[1,1],[-1,1],[-1,0],[-1,-1],[0,-1]]
    for each in a:
        for i in range(120):
            s=str(each[0])+' '+str(each[1])+'\n'
            f_w.write(s)
    f_w.close()

get_test_graph(r'example\test.txt')