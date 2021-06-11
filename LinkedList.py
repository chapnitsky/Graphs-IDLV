

class LinkedList:
    def __init__(self, head):
        self.head = head
        self.neighbors = []

    def get_head(self):
        return self.head

    def get_neighbors(self):
        return self.neighbors

    def add(self, neighbor):
        self.neighbors.append(neighbor)
