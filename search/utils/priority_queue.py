import heapq

class PriorityQueue:
    def __init__(self):
        self._heap = []
        self._index = 0  # 处理相同优先级元素的插入顺序

    def push(self, assessment, node):
        """将 Task 对象插入优先队列，根据其 priority 属性排序"""
        # 堆元素为元组 (priority, index, object)
        heapq.heappush(self._heap, (assessment, self._index, node))
        self._index += 1

    def pop(self):
        """弹出优先级最高的 Task 对象"""
        if not self._heap:
            raise IndexError("优先队列为空")
        return heapq.heappop(self._heap)[-1]  # 返回 Task 对象

    def is_empty(self):
        return len(self._heap) == 0

    def peek(self):
        """查看最高优先级的 Task 对象"""
        return self._heap[0][-1] if self._heap else None