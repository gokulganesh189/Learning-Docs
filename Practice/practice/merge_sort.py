def merge_sort(arr):
    if len(arr)<=1:  #stop when arr length <= 1
        return arr
    left_arr = arr[:len(arr)//2]
    right_arr = arr[len(arr)//2:]

    merge_sort(left_arr)
    merge_sort(right_arr)

    i = j = k = 0
    while i < len(left_arr) and j < len(right_arr):  # loop breaks when i and j go past thier respective lengths
        if left_arr[i] < right_arr[j]:   
            arr[k] = left_arr[i]        #inplace operation
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    while i < len(left_arr):        # to populate the remaining left arr items to result
        arr[k] = left_arr[i]
        k += 1
        i += 1
    while j < len(right_arr):       # to populate the remaining right arr items to result
        arr[k] = right_arr[j]
        k += 1
        j += 1
    return arr

input_arr = [4,6,1,2,5,3,1,5,7,10]
print(merge_sort(input_arr))