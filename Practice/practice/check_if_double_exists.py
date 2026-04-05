class Solution:
    def checkIfExist(self, arr: list[int]) -> bool:
        num_hash = {}
        for i,num in enumerate(arr):
            num_hash[num] = i
        for i,num in enumerate(arr):
            check = num * 2
            if check in num_hash and num_hash[check] != i:
                return True
        return False


solution = Solution()
print(solution.checkIfExist(arr = [0,-2,2]))