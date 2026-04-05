class Solution:
    def reverseWords(self, s: str) -> str:
        s = s.split()
        out = []
        for i in s:
            out.append(i[::-1])
        ' '.join(out)
        return out


solution = Solution()
print(solution.reverseWords(s = "Let's take LeetCode contest"))