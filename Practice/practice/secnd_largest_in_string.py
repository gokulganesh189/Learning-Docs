import re

class Solution:
    def secondHighest(self, s: str) -> int:
        largest = -1
        second = -1
        for ch in s:
            if ch.isdigit():
                num = int(ch)
                if num > largest:
                    second = largest
                    largest = num
                elif num < largest and num > second:
                    second = num
        return second



sol = Solution()
print(sol.secondHighest("dfa12321afd"))