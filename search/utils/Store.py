from utils import func
from utils import priority_queue as pq
from utils import node
class OPEN:
    def __init__(self, func):
        self.pq = pq.PriorityQueue()
        self.nums = 0
        self.func = func
        
    def get_pq(self):
        return self.pq
    
    def add_node(self, node):
        if node is not None:
            assessment = self.assess_node(node)
            self.pq.push(assessment, node)
            self.nums = self.nums + 1
            
    # 评估 node 
    def assess_node(self, node):
        nodeGOAL = self.func.nodeGOAL
        return self.func.h(node, nodeGOAL) + self.func.g(node)
        
    # 返回 OPEN 中assessment 最小的一个node
    def get_node(self):
        self.nums = self.nums - 1
        return self.pq.pop()
    
    def peek(self):
        return self.pq.peek()
    
class CLOSED:
    def __init__(self, func):
        self.pq = pq.PriorityQueue()
        self.nums = 0
        self.func = func
    
    def get_pq(self):
        return self.pq
    
    def add_node(self, node):
        if node is not None:
            assessment = self.assess_node(node)
            self.pq.push(assessment, node)
            self.nums = self.nums + 1
            
    # 评估 node 
    def assess_node(self, node):
        return self.func.h(node) + self.func.g(node)
        
    # 返回 OPEN 中assessment 最小的键
    def get_node(self):
        self.nums = self.nums - 1
        return self.pq.pop()
    
    def peek(self):
        return self.pq.peek()
    
    