from typing import List


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        p = (m+n)-1
        p1 = m-1
        p2 = n-1
        while p1>=0 and p2>=0:
            if nums1[p1] == nums2[p2]:
                nums1[p] = nums1[p1]
                p = p-1
                p1 = p1-1
            elif nums1[p1] > nums2[p2]:
                nums1[p] = nums1[p1]
                p = p-1
                p1 = p1-1
            elif nums1[p1] < nums2[p2]:
                nums1[p] = nums2[p2]
                p = p-1
                p2 = p2-1
        while p2>=0:
            nums1[p] = nums2[p2]
            p = p-1
            p2 = p2-1
        

sol = Solution()
print(sol.merge([0],0,[1],1))