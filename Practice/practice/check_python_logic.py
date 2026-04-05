## Late binding 

funcs = []
for i in range(3):
    funcs.append(lambda: i)

# i is calculated only on function call at that time i is already 2
for f in funcs:
    print(f.__closure__)
    print(f())


#Proper way
funcs = []
for i in range(3):
    funcs.append(lambda i=i:i)

for f in funcs:
    print(f.__closure__)
    print(f())