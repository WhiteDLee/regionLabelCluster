现有数据：根据轨迹数据和北京市地理信息数据得到的区域模式图结构（即单一大图）和出行模式子图结构（即从各区域出发的模式子图）
基本思路：降维采用LargeVis方法，仅考虑边信息的情况下，将图结构降维成点在平面上的二维表示，通过kmeans将点聚为k类代表k种功能区域。

代码如下：
/**
 *@brief 从图结构得到用于largevis降维的数据，仅边向量中的起点终点和权重的值。
 *@输入 所有图结构
 *图结构数据格式：（v 点id 属性1 属性2 属性3 属性4 标签）（e 边id 输入点id 输出点id 权重 边标签）
 *@输出 每个点向量表示
 */
get_graph(graph_path,graph_result)

/**
 *@brief 根据降维后的结果进行聚类
 *降维后数据格式：（点id 降成二维的坐标x y）  
 *聚类方法：kmeans
 *@输入 聚类个数k，待聚类点集toBeClusteredFile
 *@输出：每个区域对应的类型labelText
 */
def kmeans_label(k,toBeClusteredFile,labelText)


/**
 *@brief 绘制区域聚类图，输出每个类型的FD值
 *@输入 区域对应类型labelOrderedFile，区域ID（若为空则默认顺序值），北京市地图数据
 *@输出 区域聚类图，每种类型的FD值
 */
def ToIdLabel(labelText, labelOrderedFile, idText='')
def Fdandpicture(labelOrderedText, fdValueFile)

/**
 *@brief 通过FD值计算熵值，比较图嵌入方法得到聚类的效果。
 *@输入 聚类个数k，FD值文件fdValueFile
 *@输出 熵值
 */
def poi_cal(k, fdValueFile)


测试数据：
图嵌入数据(LINE-exp)：
    graph_path=r'example\vec_all.txt'
    graph_result_label=r'example\LINE_label.txt'
    verticeLabelText=r'example\vertive_label_LINE.txt'
    idLabel=r'example\vertice_label_ordered_LINE.txt'
    DF=r'example\DF_random9_vertice7_LINE.txt'
    excelResult=r'example\resultFileLINE.csv'
    kmeans_label(7,graph_path,graph_result_label)
    ToIdLabel(graph_result_label,idLabel,graph_path)
    Fdandpicture(idLabel,DF)
    poi_cal(7,DF,excelResult)

子图集数据(subgraph-exp)：
    kmeans_label(7, r'example\graph_100_dim_newlr.txt', 'example\graph_100_newlr_label.txt')
    trans_query_graph.getVerticesClass(836,r'example\graph_100_newlr_label.txt',r'example\vertice_label_matrix.txt' )
    ToIdLabel(r'example\vertice_label_matrix.txt', r'example\vertice_label_ordered_matrix.txt')
    Fdandpicture(r'example\vertice_label_ordered_matrix.txt', r'example\DF_random9_vertice7_newlr.txt')
    poi_cal(7, r'example\DF_random9_vertice7_newlr.txt',r'example\resultFileSubgraph.csv')
