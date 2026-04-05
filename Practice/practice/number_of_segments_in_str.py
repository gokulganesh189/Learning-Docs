class Solution:
    def countSegments(self, s: str) -> int:
        splitted = s.split(' ')
        out = 0
        for i in splitted:
            i = i.strip()
            if i:
                out += 1
        return out
    

sol = Solution()
print(sol.countSegments(", , , ,        a, eaefa"))