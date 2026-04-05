from collections import Counter

class Solution:
    def firstUniqChar(self, s: str) -> int:
        count_dict = Counter(s)
        for item in count_dict:
            if count_dict[item] == 1:
                return s.find(item)
        return -1
out = Solution()
result = out.firstUniqChar("dddccdbba")
print(result)