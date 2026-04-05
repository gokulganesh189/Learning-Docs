class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None

    def add_to_linked_list(self, data):
        new_node = ListNode(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_index(self, data, index):
        if index == 0:
            self.add_to_linked_list(data)
            return
        new_node = ListNode(data)
        temp = self.head
        current_position = 0
        while temp and current_position < index-2:
            temp = temp.next
            current_position +=1
        if not temp:
            print('index out of bound')
        new_node.next = temp.next
        temp.next = new_node
        
            
            


    def remove_value(self, check_dup):

        while self.head and self.head.val == check_dup:
            self.head = self.head.next
        temp = self.head
        while temp and temp.next:
            if temp.next.val == check_dup:
                temp.next = temp.next.next

            else:
                temp = temp.next

    def insert_at_end(self, data):
        new_node = ListNode(data)
        if not self.head:
            self.head = new_node
            return
        temp = self.head
        if temp.next:
            temp = temp.next
        temp.next = new_node






    def print_list(self):
        temp = self.head
        while temp:
            print(temp.val, end=" → ")
            temp = temp.next
        print("None")


ll = LinkedList()
ll.add_to_linked_list(6)
ll.add_to_linked_list(5)
ll.add_to_linked_list(4)
ll.add_to_linked_list(6)
ll.add_to_linked_list(2)
ll.add_to_linked_list(1)

ll.print_list()
ll.remove_value(6)
ll.print_list()
ll.add_to_linked_list(7)
ll.insert_at_index(12,3)
ll.print_list()