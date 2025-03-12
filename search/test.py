import sys
import os

# 获取当前文件的绝对路径
current_file = os.path.abspath(__file__)

# 当前目录 -> 父目录逐级上溯到项目根目录（根据实际情况调整层级）
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))  # 示例：上溯3级到项目根目录

# 添加父目录同级的其他文件夹（如utils）
utils_dir = os.path.join(os.path.dirname(base_dir), 'utils')  # 假设utils与项目根目录同级
if utils_dir not in sys.path:
    sys.path.insert(0, utils_dir)  # 优先搜索

# 递归添加子文件夹（可选，通常不需要，只要父目录在sys.path即可）
# 遍历utils下的所有子目录并添加（根据需求决定是否需要）
for root, dirs, files in os.walk(utils_dir):
    if root not in sys.path:
        sys.path.append(root)

from utils import Store
from utils import graph
from utils import func
import numpy as np
import copy

# 启发函数，不在目标位置的数字个数
def h(nodeNOW,nodeGOAL):
    cnt = 0
    for i in range(nodeGOAL.graph.shape[0]):
        for j in range(nodeGOAL.graph.shape[1]):
            if nodeNOW.graph[i][j] != nodeGOAL.graph[i][j]:
                cnt += 1
                
    return cnt

# 启发函数，数字到目标位置要走的步数
def h2(nodeNOW,nodeGOAL):
    cnt = 0
    nums = nodeGOAL.graph.shape[0] * nodeGOAL.graph.shape[1]
    hash1 = np.zeros([nums,2])
    hash2 = np.zeros([nums,2])
    for i in range(nodeGOAL.graph.shape[0]):
        for j in range(nodeGOAL.graph.shape[1]):
            hash1[nodeGOAL.graph[i][j]][0] = i
            hash1[nodeGOAL.graph[i][j]][1] = j
            
            hash2[nodeNOW.graph[i][j]][0] = i
            hash2[nodeNOW.graph[i][j]][1] = j
    
    for i in range(1, nums):
        cnt += abs(hash1[i][0]-hash2[i][0]) + abs(hash1[i][1]-hash2[i][1])
    return cnt
    

def g(node):
    cnt = 0
    cur = node.father
    while cur is not None:
        cnt += 1
        cur = cur.father
    return cnt

graphGOAL = np.array([[4,5,3],
                 [1,0,2]])
graphORI = np.array([[0,5,3],
                 [1,2,4]])

# h2: 1 1 0 0 0 1 0 2 1

f = func.func(h2,g,graph.graph(graphGOAL))

OPEN = Store.OPEN(f)

node0 = graph.graph(graphORI)
node1 = graph.graph(graphGOAL)

print(h2(node0, node1))
print(h(node0, node1))
closed = []
OPEN.add_node(node0)

def check(closed, node):
    for i in closed:
        if np.array_equal(i.graph, node.graph):
            return True
        
    return False

def expand(cur_graph, closed):
    res = []
    graph_copy = copy.deepcopy(cur_graph.graph)
    drt = np.array([[1,0,-1,0],[0,1,0,-1]])
    for i in range(graph_copy.shape[0]):
        for j in range(graph_copy.shape[1]):
            if graph_copy[i][j] == 0:
                for k in range(4):
                    next_x = i + drt[0][k]
                    next_y = j + drt[1][k]
                    if next_x >=0 and next_y >= 0 and next_x < graph_copy.shape[0] and next_y < graph_copy.shape[1]:
                        graph_new = copy.deepcopy(graph_copy)
                        graph_new[i][j] = graph_new[next_x][next_y]
                        graph_new[next_x][next_y] = 0
                        add = graph.graph(graph_new)
                        if check(closed, add):
                            continue
                        add.father = cur_graph
                        res.append(add)

    return res

resultNode = None
Found = False

while OPEN.nums >0 and not Found:
    cur = OPEN.get_node()
    expand_from_cur = expand(cur, closed)
    closed.append(cur)

    for i in expand_from_cur:
        if np.array_equal(i.graph, graphGOAL):
            Found = True
            print('Found')
            resultNode = i
            break
            
        if check(closed, i):
            pass
        
           
        else:
            OPEN.add_node(i)
        
resultNode.get_path()
