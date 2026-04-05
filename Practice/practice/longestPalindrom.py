class Solution:
    def longestPalindrome(self, s: str) -> str:
        result = ''
        for i in range(0,len(s)):
            current = s[i]
            for j in range(i+1, len(s)):
                current = current +s[j]
                rev = current[::-1]
                if current == rev and not result:
                    result = current
                elif current == rev and result and len(current) > len(result):
                    result = current
        if result == '':
            return s[0]
        return result
                

sol = Solution()
print(sol.longestPalindrome("ac"))