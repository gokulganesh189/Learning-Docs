class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        result = 0
        for c in s + t:
            result ^= ord(c)
            print(result)
        return chr(result)



out = Solution()
result = out.findTheDifference("aa", "aa")
print(result)