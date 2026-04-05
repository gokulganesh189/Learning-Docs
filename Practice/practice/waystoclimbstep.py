n = 4
if n < 2:
    print(n)

a, b = 1, 2
for i in range(3,n+1):
    a, b = b, a+b

print(b) 