class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        

class Solution:
    def inorderTraversal(self, root):
        result = []

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            result.append(node.val)
            dfs(node.right)

        dfs(root)
        return result
    def inorderTraversalStack(self, root):
        result = []
        stack = []
        current = root

        while current or stack:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()
            result.append(current.val)
            current = current.right

        return result


def construct_tree(input_list):
    if not input_list:
        return None
    nodes = [TreeNode(v) if v else None for v in input_list]
    print(nodes)
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node:
            if kids:
                node.left = kids.pop()
            if kids:
                node.right = kids.pop()

    return root

root = construct_tree([1,2,3,4,5,None,8,None,None,6,7,9])
solution = Solution()
invoke = solution.inorderTraversal(root)

print(invoke)
invoke = solution.inorderTraversalStack(root)

print(invoke)



