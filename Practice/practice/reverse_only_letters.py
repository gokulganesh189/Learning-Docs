class Solution:
    def reverseOnlyLetters(self, s: str) -> str:
        ip_arr = list(s)
        i = 0
        j = len(ip_arr)-1
        while i < j:
            if not ip_arr[i].isalpha():
                i += 1
            if not ip_arr[j].isalpha():
                j -= 1
            if ip_arr[i].isalpha() and ip_arr[j].isalpha():
                ip_arr[i], ip_arr[j] = ip_arr[j], ip_arr[i]
                i+=1
                j-=1

        return ''.join(ip_arr)




solution = Solution()
print(solution.reverseOnlyLetters(s = "Test1ng-Leet=code-Q!"))