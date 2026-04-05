# --------------------------
# Definition for a Tree Node
# --------------------------
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# --------------------------
# Solution Class
# --------------------------
class Solution:
    def isSymmetric(self, root):
        # The tree is symmetric if left and right subtree are mirror images
        return self.isMirror(root.left, root.right)

    def isMirror(self, left, right):
        # If both empty → they match
        if not left and not right:
            return True

        # If one empty and other not → not mirror
        if not left or not right:
            return False

        # Check 3 things:
        # 1. values match
        # 2. left.left  vs right.right
        # 3. left.right vs right.left
        return (left.val == right.val and
                self.isMirror(left.left, right.right) and
                self.isMirror(left.right, right.left))
# Build the tree manually
root = TreeNode(1)

root.left = TreeNode(2)
root.right = TreeNode(2)

root.left.left = TreeNode(3)
root.left.right = TreeNode(4)

root.right.left = TreeNode(4)
root.right.right = TreeNode(3)

# # Call the solution
sol = Solution()
print(sol.isSymmetric(root))   # True
