class Solution:
    def sortedSquares(self, nums: list[int]) -> list[int]:
        i = 0
        j = len(nums)-1
        result = []
        while i <= j:
            if abs(nums[i]) > abs(nums[j]):
                result.append(nums[i]*nums[i])
                i += 1
            else:
                result.append(nums[j]*nums[j])
                j -= 1
        return result[::-1]




solution = Solution()
invoke = solution.sortedSquares(nums = [-4,-1,0,3,10])
print(invoke)