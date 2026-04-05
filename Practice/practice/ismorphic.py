class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        hash_s_t = {}
        hash_t_s = {}
        for i in range(len(s)):
            key = s[i]
            mapp = t[i]
            if key in hash_s_t:
                if hash_s_t[key] != mapp:
                    return False
            else:
                hash_s_t[key]=mapp

            if mapp in hash_t_s:
                if hash_t_s[mapp] != key:
                    return False
            else:
                hash_t_s[mapp] = key
        return True



solution = Solution()
invoke = solution.isIsomorphic("badc", 'baba')
print(invoke)