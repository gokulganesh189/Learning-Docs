from typing import List


class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        hash_map = {}
        for i, item in enumerate(nums):
            if item not in hash_map:
                hash_map[item] = i
            else:
                captured_id = hash_map[item]
                diff = i-captured_id
                if diff <= k:
                    return True
                hash_map[item] = i
        return False
    
solution = Solution()
invoke = solution.containsNearbyDuplicate([1,0,1,1], 1)

print(invoke)