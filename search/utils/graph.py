from utils import node
import numpy as np

class graph(node.node):
    def __init__(self, graph = None):
        super().__init__()
        self.graph = np.zeros([3,3],int)
        
        if graph is not None:
            self.graph = graph
    
    def update(self, graph):
        self.graph = graph
        
    def print_graph(self):
        for i in range(self.graph.shape[0]):
            for j in range(self.graph.shape[1]):
                print(self.graph[i][j],sep=',',end=' ')
            print()

    def get_graph(self):
        return self.graph
    
    def get_path(self):
        cur = self
        cnt = 0
        while cur is not None:
            cnt+=1
            print(cur.graph)
            print()
            cur = cur.father
        print(f"path's length is {cnt}")

