class TreeNode:
    def __init__(self, val=0, left=None,right=None):
        self.val = val
        self.left = left
        self.right = right

    def get_tree(self, list_1, list_2):
        root_1 = construct_tree(list_1)
        root_2 = construct_tree(list_2)
        print(f'{root_1.left.val} <-- {root_1.val} --> {root_1.right.val}')
        print(f'{root_2.left.val} <-- {root_2.val} --> {root_2.right.val}')
        return root_1, root_2

def construct_tree(input_list):
    # nodes = [TreeNode(value) if value else None for value in input_list]
    nodes = [TreeNode(item) if item else None for item in input_list]
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node:
            if kids:
                node.left = kids.pop()
            if kids:
                node.right = kids.pop()
    return root

def is_same_tree(p, q):
    if not p  and not q:
        return True
    if not p or not q:
        return False
    
    if p.val != q.val:
        return False
    
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)

# root1 = construct_tree([1,2,3])
# root2 = construct_tree([1,2,3])

res = TreeNode()
root1, root2 = res.get_tree([1,2,3], [1,2,3])
print(is_same_tree(root1, root2)) 