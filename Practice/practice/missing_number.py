class Solution:
    def missingNumber(self, nums: list[int]) -> int:
        xor = 0
        n = len(nums)

        for i in range(n + 1):
            xor ^= i
        print(xor)
        for num in nums:
            xor ^= num
            print(xor)

        return xor

sol = Solution()
print(sol.missingNumber([1,0,3]))