from typing import List


class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        key_set = {}
        for i,item in enumerate(order):
            key_set[item] = i
        for i in range(len(words)-1):
            word1 = words[i]
            word2 = words[i+1]
            for j in range(min(len(word1), len(word2))):
                if word1[j] != word2[j]:
                    if key_set[word1[j]] > key_set[word2[j]]:
                        print(key_set[word1[j]], key_set[word2[j]])
                        return False
                    break

            else:
                if len(word1) > len(word2):
                    return False
        return True                                                           

solution = Solution()
invoke = solution.isAlienSorted(["apple","app"], order = "abcdefghijklmnopqrstuvwxyz")
print(invoke)