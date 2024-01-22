######################## This is the 'Augmented AVL Tree' implementation with runtime O(log(N)) #######################
# This is a great way to store an unlimited number of intervals
# It enables us to determine the intersection of some of those intevals with a point in time complexity of O(log(N))
# Being that an AVL Tree is a self balancing tree

# The node class
class Node():
    def __init__(self, range, data):
        self.low = range[0]
        self.high = range[1]
        self.data = data
        self.dupl_nodes = []
        self.left = None
        self.right = None
        self.max = 0
        self.height = 0


# The Augmented AVL Tree class
class AugTree():
    
    # The class constructor
    def __init__(self):
        self.root = None
        self.size = 0


    # This is a method that determines the hight of the subtree starting from 'node' 
    def height(self,node):
        if node is None:
            return -1
        
        return node.height
    

    # This is a method that updates the hight of a given node
    def update_height(self,node):
        if node is not None:
            node.height = 1 + max(self.height(node.left),self.height(node.right))
    

    # This is a method that updates the max at root depending on 
    # either the max of its left or right subtree
    # or the upper bound of its right or left child
    def update_max(self, root):
        if root is None:
            return
    
        root.max = max(
            self.get_max(root.left), 
            self.get_max(root.right),
            self.get_high(root.left),
            self.get_high(root.right)
        )

    # This is a method that gets the max of a given node
    def get_max(self,node):
        if node is None:
            return 0
        
        return node.max

    # This is a method that gets the upper bound of a given node
    def get_high(self, node):
        if node is None:
            return 0
        
        return node.high
        

    # This is a method that calculates the hight difference/ the balance factor
    def height_diff(self, node):
        # If left is taller than right, then this will return a positive number
        # If right is taller than left, then this will return a negative number
        if node is not None:
            return self.height(node.left) - self.height(node.right)
        

    # This is a method that rotates the subtree with root 'node' to the right
    def rotate_right(self, node):
        temp1 = node.left
        temp2 = temp1.right

        temp1.right = node
        node.left = temp2

        self.update_height(node)
        self.update_height(temp1)

        self.update_max(temp2)
        self.update_max(node)
        self.update_max(temp1)
        
        return temp1


    # This is a method that rotates the subtree with root 'node' to the left
    def rotate_left(self, node):
        temp1 = node.right
        temp2 = temp1.left

        temp1.left = node
        node.right = temp2

        self.update_height(node)
        self.update_height(temp1)

        self.update_max(temp2)
        self.update_max(node)
        self.update_max(temp1)

        return temp1


    # This is a method that balances the subtree with root 'node' by rotating it
    def balance(self,node, balance,low):
        # Left Heavy
        if balance > 1:
            if low < node.left.low: # right-right rotation
                return self.rotate_right(node)
            else: # left-right rotation
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        # Right Heavy
        if balance < -1:
            if low > node.right.low: # left-left rotation
                return self.rotate_left(node) 
            else: # right-left rotation
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)
                    
        return node

    # This is the insert recurssive helper method that inserts a new node(range, data) to the AVL tree based on the lower bound
    def __insert(self, root, range, data):
        if root is None:
            return Node(range,data)
        
        low = range[0]
        high = range[1]

        if low < root.low: 
            # Insert to the left
            root.left = self.__insert(root.left,range,data)

        elif low > root.low: 
            # Insert to the right
            root.right = self.__insert(root.right,range,data)

        else:
            # If the low values match, add the new node to the array pointed to by the same node 'root'
            root.dupl_nodes.append(Node(range,data))
            return root

        self.update_height(root)
        self.update_max(root)

        balanceFactor = self.height_diff(root)

        root = self.balance(root, balanceFactor,low)
        
        return root


    # This is a method that calls the __insert method
    def insert(self, range,data):
        self.root = self.__insert(self.root,range,data)


    # This is the get recurssive helper method that gets a list of ranges that the 'key' belongs to
    def __get(self, root, key, ret):

        if root is None:
            return

        if root.low <= key:

            if key < root.high:
                ret.append(root.data)

            for node in root.dupl_nodes:
                if key < node.high:
                    ret.append(node.data)

        if key >= root.max:
            return
        
        if key >= root.low:
            self.__get(root.right, key, ret)

        self.__get(root.left, key, ret)

        return
        
    # This is a method that calls the __get method
    def get(self, key):
        ret = []
        self.__get(self.root, key, ret)
        return ret
    
    # This is a helper method that stores the ranges and the data in an array
    def __toarr(self,root,arr):
        if root is None:
            return
        
        self.__toarr(root.left,arr)

        arr.append((root.low, root.high, root.data))
        for node in root.dupl_nodes:
            arr.append((node.low, node.high, node.data))

        self.__toarr(root.right,arr)


    # This is a method that calls the __toarr method
    def to_array(self):
        arr = []
        self.__toarr(self.root,arr)
        return arr
    