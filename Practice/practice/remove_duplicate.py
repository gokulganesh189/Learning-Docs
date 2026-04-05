class ListNode:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

class Solution:

    def delete_duplicates(self, head:ListNode) -> ListNode:
        if not head:
            return None
        values = []
        curr = head
        while curr:
            values.append(curr.value)
            curr = curr.next

        values.sort()

        unique_values = []
        for val in values:
            if val not in unique_values:
                unique_values.append(val)
        new_head = ListNode(unique_values[0])
        curr = new_head

        for val in unique_values[1:]:
            curr.next = ListNode(val)
            curr = curr.next

        return new_head
    
def build_linked_list(values):
    if not values:
        return None
    head = ListNode(values[0])
    curr = head
    for val in values[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def print_linked_list(head):
    curr = head
    while curr:
        print(curr.value, end='->' if curr.next else "")
        curr = curr.next

    print()

head = build_linked_list([3, 1, 2, 3, 2, 1])
print("Original List:")
print_linked_list(head)

solution = Solution()
new_head = solution.delete_duplicates(head)

print("Sorted Unique List:")
print_linked_list(new_head)