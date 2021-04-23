import heapq

"""
    The PriorityQueue needs to hold a tuple of 2 elements.  The first element is what the queue will be sorted upon.
"""

class PriorityQueue:
    __next__ = next

    def __init__(self):
        self.queue = []
        self.current = 0

    def next(self):
        if self.current >= len(self.queue):
            raise StopIteration

        out = self.queue[self.current]
        self.current += 1

        return out

    def pop(self):
        return heapq.heappop(self.queue)
        # raise NotImplementedError

    def remove(self, node_id):
        heapq.heappop(self.queue, node_id)
        # raise NotImplementedError

    def clear(self):
        self.queue = []

    def __iter__(self):
        return self

    def __str__(self):
        return 'PQ:[%s]' % (', '.join([str(i) for i in self.queue]))

    def append(self, node):
        heapq.heappush(self.queue, node)

    def __contains__(self, key):
        self.current = 0
        return key in [n for v, n in self.queue]

    def __eq__(self, other):
        self.current = 0
        return self == other

    def top(self):
        if self.size() > 0:
            return self.queue[0]
        return None

    def size(self):
        return len(self.queue)

    def reset_iter(self):
        self.current = 0

    def has_next(self):
        if self.current < self.size():
            return True
        return False
