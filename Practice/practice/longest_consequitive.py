def longest_consecutive(nums):
    longest = []
    nums = sorted(nums)
    for num in nums:
        current = num
        sequence = [current]
        while current+1 in nums:
            current += 1
            sequence.append(current)
        if len(sequence) >len(longest):
            longest = sequence

    return longest



nums = [100, 4, 200, 1, 3, 2, 201, 202, 203, 204]
result = longest_consecutive(nums)
print("Longest sequence:", result)
print("Length:", len(result))
