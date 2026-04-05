digits = [1,2,3]
result = ''
for digit in digits:
    result += str(digit)

result_int = str((int(result)+1))
out = []
for item in result_int:
    out.append(int(item))
print(out)
