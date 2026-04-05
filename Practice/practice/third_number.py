class Solution:
    """ Solution O(nlogn) because of sorting"""
    def thirdMax(self, nums: list[int]) -> int:
        unique = set(nums)
        sorted_list = sorted(unique)
        
        if len(sorted_list) > 3:
            return sorted_list[-3]

        if len(sorted_list) < 3:
            return sorted_list.pop()
        
        if len(sorted_list) == 3:
            return sorted_list[0]
        
sol = Solution()
print(sol.thirdMax([1,1,2]))