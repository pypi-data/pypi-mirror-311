#Used for the list of notes

class Node:
    def __init__(self, data, bits=16):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)

""" This list only use things I need"""

class CircularLinkedList:
    def __init__(self, node_class=Node):
        self.root = None

    def append(self, data):
        new_node = Node(data)

        if not self.root:
            self.root = new_node
            self.root.next = self.root

        else:
            current_node = self.root

            while current_node.next != self.root:
                current_node = current_node.next
            
            current_node.next = new_node
            new_node.next = self.root
    
    def find_one(self, data):
        current_node = self.root
        index = 0

        while current_node.data != data:
            current_node = current_node.next
            index += 1

            if current_node == self.root:
                raise StopIteration

        return [current_node, index]
    
    def __getitem__(self, steps):
        current_node = self.root
        i = 0

        while i <= steps:
            node = current_node
            current_node = current_node.next

            i += 1

        return node
    
    def __iter__(self):
        self._iter_current_node = self.root
        return self

    def __next__(self):
        if self._iter_current_node.next != self.root:
            node = self._iter_current_node
            self._iter_current_node = self._iter_current_node.next

            return node
        
        raise StopIteration

    def __repr__(self):
        object_list = []

        current_node = self.root
        while True:
            object_list.append(str(current_node))
            print(current_node)

            current_node = current_node.next
            if current_node == self.root:
                break

        return f'Circular{str(object_list)}'

