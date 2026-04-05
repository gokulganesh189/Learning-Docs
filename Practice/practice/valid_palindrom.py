class Solution:
    def isPalindrome(self, s: str) -> bool:
        converted = s.lower()
        result = ''
        for char in converted:
            if char.isalnum():
                result += char
        rev = result[::-1]
        if rev == result:
            return True
        return False

        

sol = Solution()
print(sol.isPalindrome("A man, a plan, a canal: Panama"))