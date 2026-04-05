class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        s = s.strip()
        s_list = s.split(' ')
        print(s_list)
        return len(s_list[-1])



s = "   fly me   to   the moon  "
solution = Solution()
length = solution.lengthOfLastWord(s)
print(length)