# def strStr(heystack, needle):
#     check = len(needle)
#     start = 0
#     while heystack:
#         try:
#             check_needle = heystack[start:check]
#             if len(heystack) < len(needle):
#                 return -1
#             if check_needle == needle:
#                 return start
#             else:
#                 start +=1
#                 check +=1
#                 if check == len(heystack)+1:
#                     return -1                                                    
#         except:
#             return -1

def strStr(haystack, needle):
    if needle == "":
        return -1
    for i in range(len(haystack) - len(needle) + 1):
        if heystack[i: i+len(needle)] == needle:
            return i
    return -1


heystack="leetcode"
needle = "leeto"

# heystack="sadbutsad"
# needle = "sad"

index = strStr(heystack, needle)
print(index)
