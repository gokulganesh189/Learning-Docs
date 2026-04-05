def valid_pattern_check(pattern):
    stack = []
    for ch in pattern:
        if ch == "(" or ch == "[" or ch == "{":
            stack.append(ch)

        else:
            if not stack:
                return False
            top = stack.pop()
            if ch == ")" and top !="(":
                return False
            if ch == ']' and top !="[":
                return False
            if ch == "}" and top !="{":
                return False
    if len(stack) == 0:
        return True
    return False
                                                    



pattern = "(({(}))"
is_valid = valid_pattern_check(pattern)
if is_valid:
    print("valid")
else:
    print('Invalid')