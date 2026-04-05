class Solution:
    def reverseVowels(self, s: str) -> str:
        vowels = set('aeiouAEIOU')
        string_list = list(s)
        left = 0
        right = len(string_list) - 1

        while left < right:
            if string_list[left] not in vowels:
                left +=1
                continue
            if string_list[right] not in vowels:
                right -=1
                continue

            string_list[left], string_list[right] = string_list[right], string_list[left]
            left += 1
            right -= 1

        return "".join(string_list)
            
    
solution = Solution()
invoke = solution.reverseVowels(s = "IceCreAm")
print(invoke)