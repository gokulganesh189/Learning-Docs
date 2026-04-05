digits = [1,2,3]

for i in range(len(digits)-1, -1, -1):
    if digits[i] < 9:
        digits[i] += 1
        break
    else:
        digits[i] = 0
[1]+digits 