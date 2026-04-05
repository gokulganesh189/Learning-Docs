# Given an unsorted array of integers, you need to write a program to find the length of
# the longest consecutive elements sequence. [Mark 2]
# For example,
# Input: [100, 4, 200, 1, 3, 2]
# Output: 4 # The sequence [1, 2, 3, 4] is the longest consecutive sequence.
def longest_consecutive(nums):
    if not nums:
        return 0

    num_set = set(nums)
    longest_streak = 0

    for num in num_set:
        if num - 1 not in num_set:  
            current_num = num
            current_streak = 1

            while current_num + 1 in num_set:
                current_num += 1
                current_streak += 1

            longest_streak = max(longest_streak, current_streak)

    return longest_streak

input = [100, 4, 200, 1, 3, 2]
print(longest_consecutive(input)) 