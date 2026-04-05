arr =[6,0,7,0,7,5,7,8,3,4,0,7,8,1,6,8,1,1,2,4,8,1,9,5,4,3,8,5,10,8,6,6,1,0,6,10,8,2,3,4]
arr.sort()
remove = int(len(arr) * 0.05)
trimmed = arr[remove: len(arr) - remove]
print( sum(trimmed) / len(trimmed))