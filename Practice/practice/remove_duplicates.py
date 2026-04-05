def removeDuplicates(nums):
    if len(nums) == 0:
        return 0

    k = 1  # index where next unique element will be placed

    for i in range(1, len(nums)):
        if nums[i] != nums[i - 1]:  # found a new unique element
            nums[k] = nums[i]
            k += 1
    return k


nums = [0,0,1,1,1,1,2,2,2,3,3]
unique = removeDuplicates(nums)

print(unique)

