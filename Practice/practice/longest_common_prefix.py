
def longest_common_prefix(items):
    prefix = items[0]

    for item in items:
        while not item.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix
        
items = ["flower","flow","flight"]
prefix = longest_common_prefix(items)
print(prefix)