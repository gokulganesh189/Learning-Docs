from collections import Counter


class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        ransom_hash = Counter(ransomNote)
        magazine_hash = Counter(magazine)
        for item in ransom_hash:
            count = ransom_hash[item]
            if count <= magazine_hash[item]:
                pass
            else:
                return False
        return True
        
sol = Solution()
print(sol.canConstruct("aa", "ad"))