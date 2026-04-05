from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build_linked_list(values):
    if not values:
        return None

    head = ListNode(values[0])
    current = head

    for v in values[1:]:
        current.next = ListNode(v)
        current = current.next

    return head

def build_intersecting_lists(listA, listB, skipA, skipB):
    headA = build_linked_list(listA)
    headB = build_linked_list(listB)

    currA = headA
    for _ in range(skipA):
        if currA is None:
            raise ValueError("skipA is out of bounds")
        currA = currA.next

    currB = headB
    for _ in range(skipB):
        if currB is None:
            raise ValueError("skipB is out of bounds")
        currB = currB.next

    currB.next = currA
    return headA, headB, currA

def getIntersectionNode(headA,headB):
        head_a = headA
        head_b = headB
        if head_a or head_b:
            temp_a = head_a
            temp_b = head_b
        else:
            return None
        while temp_a:
            current = temp_b
            while current:
                if temp_a == current:
                    return True
                current = current.next
            temp_a = temp_a.next



listA = [4,1,8,4,5]
listB = [5,6,1,8,4,5]

headA, headB, intersection = build_intersecting_lists(
    listA, listB, skipA=2, skipB=3
)
getIntersectionNode(headA, headB)

print("Expected intersection value:", intersection.val)
