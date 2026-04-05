class Solution:
    def majorityElement(self, nums):
        hash_map = {}
        counter = 0
        result = 0
        for num in nums:
            if num in hash_map:
                hash_map[num] += 1

            else:
                hash_map[num] =1
        for item in hash_map:
            if hash_map[item] > counter:
                counter = hash_map[item]
                result = item
        return result
        



out = Solution()
result = out.majorityElement([2,2,1,1,1,2,2])
print(result)
        
