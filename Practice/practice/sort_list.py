def bubble_sort(arr):
    try:
        n = len(arr)
        for i in range(n):
            print(arr[i])
            for j in range(0, n-1-i):
                if arr[j] > arr [j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    
        return arr
    except:
        return arr

            



print(bubble_sort([5, 2, 9, 1]))
