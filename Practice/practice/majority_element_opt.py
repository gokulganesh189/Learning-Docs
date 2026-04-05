class Solution:
    def majorityElement(self, nums):
        candidate = None
        count = 0
        for num in nums:
            if count == 0:
                candidate = num
            if num == candidate:
                count += 1
            if num  != candidate:
                count -= 1

        return candidate
            






out = Solution()
result = out.majorityElement([2,2,1,1,1,2,2,1,1])
print(result)
        