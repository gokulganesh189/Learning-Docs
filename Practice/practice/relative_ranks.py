from typing import List


class Solution:
    def findRelativeRanks(self, score: List[int]) -> List[str]:
        score_hash = {}
        sorted_score = sorted(score, reverse=True)
        for i in range(len(sorted_score)):
            if i == 0:
                score_hash[sorted_score[i]] = "Gold Medal"
            elif i == 1:
                score_hash[sorted_score[i]] = "Silver Medal"
            elif i == 2:
                score_hash[sorted_score[i]] = "Bronze Medal"
            else:
                score_hash[sorted_score[i]] = str(i + 1)
        return [score_hash[i] for i in score]

        


sol = Solution()
print(sol.findRelativeRanks(score = [10,3,8,9,4]))
            