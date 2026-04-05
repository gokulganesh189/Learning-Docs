from itertools import zip_longest

class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split(" ")
        if len(pattern) != len(words):
            return False
        char_to_word = {}
        word_to_char = {}
        print(list(zip(pattern, words)))
        print(list(zip_longest(pattern,words)))
        for p,w in zip(pattern, words):
            if p in char_to_word:
                if char_to_word[p] !=w:
                    return False
            else:
                char_to_word[p] = w

            if w in word_to_char:
                if word_to_char[w] != p:
                    return False
            else:
                word_to_char[w] = p
        return True

    
solution = Solution()
invoke = solution.wordPattern(pattern = "abab", s = "dog dog dog dog")
print(invoke)

# class Solution:
#     def wordPattern(self, pattern: str, s: str) -> bool:
#         s = s.split()
#         return (len(set(pattern))==len(set(s))==len(set(zip_longest(pattern,s))))