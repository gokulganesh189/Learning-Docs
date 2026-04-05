import re
from collections import Counter

class Solution:
    def mostCommonWord(self, paragraph: str, banned: list[str]) -> str:
        str_list:list[str] = re.findall(r'[a-z]+', paragraph.lower())
        banned_set:set = set(banned)

        count = Counter()
        for word in str_list:
            if word not in banned_set:
                count[word] +=1
        return count.most_common(1)[0][0]



            
            

        

sol = Solution()
print(sol.mostCommonWord("Bob hit a ball, the hit BALL flew far after it was hit.", ["hit"]))