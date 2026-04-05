from itertools import zip_longest


class Solution:
    def addStrings(self, num1: str, num2: str) -> str:
        carry = 0
        result = ""
        for i in zip_longest(num1[::-1], num2[::-1]):
            if i[0] is not None and i[1] is not None:
                added = int(i[0]) + int(i[1]) + carry
                if added > 9:
                    carry = 1
                
            elif i[0] is None and i[1] is not None:
                added = int(i[1]) + carry
                if added > 9:
                    carry = 1
            elif i[0] is not None and i[1] is None:
                added = int(i[0]) + carry
                if added > 9:
                    carry = 1
            added_str = str(added)
            added_str = added_str[::-1][0]
            result += added_str
        return result[::-1]


solution = Solution()
print(solution.addStrings(num1 = "456", num2 = "77"))
