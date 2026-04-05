from collections import Counter
from typing import List

class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        c1 = Counter(nums1)
        c2 = Counter(nums2)
        result = []
        for key in c1:
            if key in c2.keys():
                number_count = min(c1[key], c2[key])
                for i in range(number_count):
                    result.append(key)
        print(result)


solution = Solution()
invoke = solution.intersect(nums1 = [4,9], nums2 = [9,4,9,8,4])