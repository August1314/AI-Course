

class func:
    def __init__(self, h, g, nodeGOAL):
        self.h = h
        self.g = g
        self.nodeGOAL = nodeGOAL
        
    def h(self, nodeNOW, nodeGOAL):
        res = self.h(nodeNOW, nodeGOAL)
        
        return res
        
    def g(self, node):
        res = self.g(node)
        
        return self.g(node)