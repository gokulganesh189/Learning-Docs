class Solution:
    def isPowerOfThree(self, n: int) -> bool:
        if n == 1:
            return True

        if n == 0 or n % 2 != 0:
            return False
        return self.isPowerOfThree(n//2)
        
    
        

sol = Solution()
print(sol.isPowerOfThree(n = 3))