# -*- coding: utf-8 -*-
#本函数主要是完成对聚类之后区域的涂色

from pylab import *
import matplotlib.pyplot as plt
from PIL import Image
import glob, os,csv

all_edge_vertice = []
all_bbox = []  #第一个区域的bbox不用存
all_convex = []#第一个区域的vertex不用存
picture_region_id = [] #存放每个像素点属于哪个区域


def default(bbox_path,convex_path):
    bbox_f = open(bbox_path,'r')
    convex_f = open(convex_path,'r')
    bbox_line = bbox_f.readline()
    convex_line = convex_f.readline()[:-2]
    lines = convex_line.split(',')
    #print len(lines),len(lines[0])
    x_matrix = len(lines)
    y_matrix = len(lines[0])
    for i in range(x_matrix):
        temp = []#picture_region_id.append([])
        for j in range(y_matrix):
            temp.append(0)
        picture_region_id.append(temp)
            
    #picture_region_id = [[0]*C.y_matrix]*C.x_matrix
    #print len(picture_region_id),len(picture_region_id[0])
    #区域0的点不是边界点
    '''for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == '1':
                #all_edge_vertice.append((i,j))
    '''
    print('generate all_edge_vertice complete')
    bbox_line = bbox_f.readline()
    convex_line = convex_f.readline()[:-2]
    i=1 #区域编号是从1开始编码的，这样就可以表示
    while bbox_line:
        bbox_line = bbox_line.replace('L','').replace('(','').replace(')','')
        bbox = bbox_line.split(',')
        all_bbox.append(bbox) #每个bbox用数组表示，如：【2,2,13,234】
        all_convex.append(get_bit_convex(convex_line,i,int(bbox[0]),int(bbox[1])))  #x,y表示该区域的起点，为了直接找到像素点，记录该点所属区域
        bbox_line = bbox_f.readline()
        convex_line = convex_f.readline()[:-2]
        i=i+1
    print('generate all_bbox and all_convex and picture_region_id complete')



#返回bit类型的convex数组(双重数组)
def get_bit_convex(convex_line,index,x,y):
    convex_bit = []
    lines = convex_line.split(',')
    #print len(picture_region_id),len(picture_region_id[0])
    #for line in lines:
    for i in range(len(lines)):
        bit = []
        #for i in line:
        for j in range(len(lines[0])):
            if lines[i][j] == '1':
                #print i,j,x+i,y+j,picture_region_id
                bit.append(True)
                picture_region_id[x+i][y+j] = index
            else:
                bit.append(False)
        convex_bit.append(bit)
    return convex_bit


def draw_new_picture(region_file_path):
    image = Image.open('ske.png')
    im_ar = array(image)
    width = len(im_ar[0])
    height = len(im_ar)
    #print width,height
    new_image = Image.new('RGB', (width,height), color=0)
    colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255),(255,255,255),(100,100,100),(200,0,100)]
    cluster_f = open(region_file_path,'r')
    region_dic = {} #存放文件里的区域与类别{region_id:cluster_id}
    #文件内容为344 (5, 1)，区域id (区域类型，数目)
    all_lines = cluster_f.readlines()
    for line in all_lines:
        line = line.strip()
        lines = line.split(' ')
        region_num = int(lines[0])
        cluster_id = int(lines[1].replace('(','').split(',')[0])
        if region_num not in region_dic:
            region_dic[region_num] = cluster_id

    for i in range(len(picture_region_id[0])):
        for j in range(len(picture_region_id)):
            if picture_region_id[j][i] not in region_dic:
                continue
            new_image.putpixel((i,j),colors[region_dic[picture_region_id[j][i]]-1])
    new_image.save('ske_coloredrandom9_new7.png','png')
    im_ar1 = array(new_image)
    width1 = len(im_ar[0])
    height1 = len(im_ar)
    #print width,height
    color_bar = Image.new('RGB',(200,1000),color=0)
    for i in range(200):
        for j in range(1000):
            index = int(j/120)
            if index>5:
                break
            color_bar.putpixel((i,j),colors[5-index])
    color_bar.save('color_bar_new7.png','png')

def get_FD_value(region_file_path,poi_type_file,outputFile):
    region_f = open(region_file_path) #读取存放区域所属类别的文件
    poi_f = open(poi_type_file) #读取存放区域POI分布的文件
    poi_line = poi_f.readline()#第一行是区域0，在实验中没有，所以剔除
    poi_line = poi_f.readline().strip()
    region_poi_type = {}#记录区域与该区域包含的poi类型及数量{region_id:{poi类型:数量}}
    while poi_line:
        lines = poi_line.split(' ') #存放该区域的所有POI类型及数量列表
        region_id = int(lines[0].strip())
        if region_id not in region_poi_type:
            region_poi_type[region_id] = {}
        for i in range(1,len(lines)):
            poi_type = lines[i].split(':')[0].strip()
            type_num = int(lines[i].split(':')[1].strip())
            if poi_type not in region_poi_type[region_id]:
                region_poi_type[region_id][poi_type] = type_num
        poi_line = poi_f.readline().strip()
    print('size of region_poi_type:',len(region_poi_type))
    region_lines = region_f.readlines()
    region_type_dic = {} #用来记录该区域被分到哪一类别{region_id:type_index}
    for line in region_lines:
        lines = line.strip().split(' ')
        region_id = int(lines[0])
        if region_id not in region_type_dic:
            region_type_dic[region_id] = 0
        ls = lines[1].replace('(','').split(',')
        type_index = int(ls[0].strip())
        region_type_dic[region_id] = type_index
    for key,value in region_poi_type.items():
        if key not in region_type_dic:
            region_type_dic[key] = 0
    print('size of region_type_dic:',len(region_type_dic))
    region_pixel_number = {} #存放每个区域的像素点数{region_id:pixel_number}
    region_0 = 0
    for i in range(len(picture_region_id[0])):
        for j in range(len(picture_region_id)):
            if picture_region_id[j][i]<1:
                region_0+=1
                continue
            if picture_region_id[j][i] not in region_pixel_number:
                region_pixel_number[picture_region_id[j][i]] = 1
                #continue
            else:
                region_pixel_number[picture_region_id[j][i]] += 1
    #print 'region_0 is : ',region_0
    #print 'size of region_pixel_number',len(region_pixel_number)
    type_pixel_num = {} #存放类型与像素点的对应关系{type_id:number}
    for key,value in region_pixel_number.items():
        if key not in region_type_dic:
            continue
        region_type = region_type_dic[key]
        if region_type not in type_pixel_num:
            type_pixel_num[region_type] = value
        else:
            type_pixel_num[region_type] += value
    #print 'type_pixel_num is:\n',type_pixel_num
    type_poi_dic = {} #存放每个类型的各poi类型个数 {type_index:{poi:number}}
    for key,value in region_poi_type.items():
        if key not in region_type_dic:
            continue
        region_type = region_type_dic[key]
        if region_type not in type_poi_dic:
            type_poi_dic[region_type] = {}
        for k,v in value.items():
            if k not in type_poi_dic[region_type]:
                type_poi_dic[region_type][k] = v
            else:
                type_poi_dic[region_type][k] += v
    #计算FD值  poi数/像素点个数
    #print 'type_poi_dic\n',type_poi_dic
    new_type_poi_dic = {}
    for key,value in type_pixel_num.items():
        poi_dic = type_poi_dic[key]
        new_type_poi_dic[key] = poi_dic
        for k,v in poi_dic.items():
            new_type_poi_dic[key][k] = float(v)/value
    #print 'new_type_poi_dic:\n',new_type_poi_dic
    f_r = open(r'poi_type.txt','r')
    all_lines = f_r.readlines()
    poi_types = []
    for line in all_lines:
        poi_types.append(line.strip().split(' ')[0])
    f_r.close()
    f_w = open(outputFile,'w')
    for key,value in new_type_poi_dic.items():
        f_w.write(str(key)+'\n')
        for poi_t in poi_types:
            if poi_t in value:
                f_w.write(str(poi_t)+':'+str(value[poi_t]*100)+'\n')
            else:
                f_w.write(str(poi_t)+':'+str(0)+'\n')
            #f_w.write(str(k)+':'+str(v*100)+' ')
        #f_w.write('\n')
    csvFile = open(r'example\DFvalue.csv', 'a', newline='')
    writer = csv.writer(csvFile)
    for key, value in new_type_poi_dic.items():
        writer.writerow([str(key)])
        for poi_t in poi_types:
            if poi_t in value:
                writer.writerow([str(poi_t),value[poi_t]*100])
            else:
                writer.writerow([str(poi_t),0])
    csvFile.close()
    f_w.close()


if __name__ == '__main__':
    #cluseter_region_path = r'../trajectory data/cluster_region_7-11zaonolabel6.txt'
    #cluseter_region_path = r'../trajectory data/random_cluster_region.txt'
    cluseter_region_path = r'tra_label7_ordered.txt'
    bbox_path = 'bbox_6.txt'
    convex_path = 'convex_6.txt'
    default(bbox_path,convex_path)
    draw_new_picture(cluseter_region_path)
    poi_type_file = r'region_poi.txt'
    outputFile=r'DF_random9_new7.txt'
    get_FD_value(cluseter_region_path,poi_type_file,outputFile)
    
            
