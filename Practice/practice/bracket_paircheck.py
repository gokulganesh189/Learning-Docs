def is_valid(pattern):
    pair_check = {')':'(', '}':'{', ']':'['}
    stack = []
    for ch in pattern:
        if ch in pair_check.values():
            stack.append(ch)
        elif ch in pattern:
            print(stack[-1])
            print(pair_check[ch])
            if not stack or stack.pop() != pair_check[ch]:
                return False
            
    return not stack





pattern = "(({}))"
is_valid = is_valid(pattern)
if is_valid:
    print("valid")
else:
    print('Invalid')