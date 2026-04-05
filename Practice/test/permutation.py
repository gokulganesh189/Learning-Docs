def permutations_lexicographic(s):
    s = ''.join(sorted(s))          # ensure lexicographic order
    n = len(s)
    used = [False] * n
    cur = []
    result = []

    def backtrack():
        if len(cur) == n:
            result.append(''.join(cur))
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            cur.append(s[i])
            backtrack()
            cur.pop()
            used[i] = False

    backtrack()
    return result

print(permutations_lexicographic("AB"))
# Output: ['ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA']
