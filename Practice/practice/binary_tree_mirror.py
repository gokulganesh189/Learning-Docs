class TreeNode:
    def __init__(self, val=0, left=None,right=None):
        self.val = val
        self.left = left
        self.right = right

def isMirror(left, right):
    if not left and not right:
        return True
    if not left or not right:
        return False
    
    return (left.val == right.val and isMirror(left.left, right.right) and isMirror(left.right, right.left))

def check_mirror(root):
    if not root:
        return True
    return isMirror(root.left, root.right)

def getLength(node):
    if node is None:
        return 0
    return 1 + max(getLength(node.left), getLength(node.right))
    

def check_length(root):
    if root is None:
        return 0
    left_length = getLength(root.left)
    right_length = getLength(root.right)
    return left_length, right_length

    

def construct_tree(input_list):
    nodes = [TreeNode(item) if item else None for item in input_list]
    kids = nodes[::-1]
    #first item
    root = kids.pop()
    for node in nodes:
        if node:
            if kids:
                # attaching first non root item to left new node
                node.left = kids.pop()
            if kids:
                node.right = kids.pop()

    return root

input_list = [1,2,2,3,4,4,3,1]
root = construct_tree(input_list)
is_mirror = check_mirror(root)
length = check_length(root)
print(is_mirror)
print(length)