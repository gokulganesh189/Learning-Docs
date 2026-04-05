from typing import List


class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        nums1 = set(nums1)
        nums2 = set(nums2)
        result = []
        for item in nums1:
            if item in nums2:
                result.append(item)
        return result

sol = Solution()
print(sol.intersection([4,9,5],[9,4,9,8,4]))