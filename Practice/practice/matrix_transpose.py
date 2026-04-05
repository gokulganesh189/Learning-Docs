from typing import List


# class Solution:
#     def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
#         rows = len(matrix)
#         cols = len(matrix[0])
#         tarnspose = []

#         for j in range(cols):
#             new_list = []
#             for i in range(rows):
#                 new_list.append(matrix[i][j])
#             tarnspose.append(new_list)
#         return tarnspose
            
import numpy as np


class Solution:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        matrix = np.array(matrix)
        return matrix.T

solution = Solution()
invoke = solution.transpose([[1,2,3],[4,5,6],[7,8,9]])
print(invoke)