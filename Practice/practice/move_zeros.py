# class Solution:
    # def moveZeroes(self, nums: list[int]) -> None:
    #     insert_pos = 0  # position to place next non-zero
        
    #     # Step 1: Move all non-zero elements forward
    #     for i in range(len(nums)):
    #         if nums[i] != 0:
    #             nums[insert_pos], nums[i] = nums[i], nums[insert_pos]
    #             insert_pos += 1

"""Alternate solution"""
class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        i = 0
        for j in range(len(nums)):
            if nums[i] == 0:
                nums.append(nums[i])
                nums.remove(nums[i])
            i += 1



solution = Solution()
nums = [0,1,0,3,12]
solution.moveZeroes(nums)
print(nums)