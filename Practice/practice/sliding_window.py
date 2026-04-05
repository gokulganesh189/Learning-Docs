nums = [1,1,1,1,1,1,1,1,1,1,1]
k = 7


left = 0
curr_sum = 0
max_length = 0

for right in range(len(nums)):
    curr_sum += nums[right]

    while curr_sum > 7:
        curr_sum -= nums[left]
        left += 1
    
    max_length = max(max_length, right-left+1)

print(max_length)

