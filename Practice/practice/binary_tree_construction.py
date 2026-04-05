class TreeItem:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def construct_tree(input_list):
    nodes = [TreeItem(v) if v else None for v in input_list]
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node:
            if kids:
                node.left = node
            if kids:
                node.right = node

    return root