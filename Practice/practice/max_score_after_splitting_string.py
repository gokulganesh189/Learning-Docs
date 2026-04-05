class Solution:
    def maxScore(self, s: str) -> int:
        result = 0
        for i in range(1, len(s)):
            zero_count = 0
            one_count = 0
            left_arr = s[:i]
            right_arr = s[i:]
            zero_count += sum(1 for item in left_arr if item == "0")
            one_count += sum(1 for item in right_arr if item == "1")
            current = zero_count + one_count
            if current > result:
                result = current
        return result


solution = Solution()
invoke = solution.maxScore(s = "1111")
print(invoke)