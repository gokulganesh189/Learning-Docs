class Solution:
    def reverseString(self, s: list[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        print(s)
        i = 0
        j =  len(s)-1
        while i < j:
            s[i], s[j] = s[j], s[i]
            i += 1
            j -=1
        return s

            
        

sol = Solution()
print(sol.reverseString(["h","e","l","l","o"]))