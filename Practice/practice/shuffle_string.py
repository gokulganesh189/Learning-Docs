class Solution:
    def restoreString(self, s: str, indices: list[int]) -> str:
        result = ["" for item in s]
        for item in indices:
            result[indices[item]] = s[item]
        return ''.join(result)


solution = Solution()
print(solution.restoreString(s = "codeleet", indices = [4,5,6,7,0,2,1,3]))