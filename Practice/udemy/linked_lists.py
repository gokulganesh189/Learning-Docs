class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def pop(self):
        if self.length == 0:
            return None
        temp = self.head
        pre = self.head
        while(temp.next):
            pre = temp
            temp = temp.next
        self.tail = pre
        self.tail.next = None
        self.length -= 1
        if self.length == 0:
            self.head = None
            self.tail = None
        return temp

    def print_list(self):
        temp = self.head
        while temp is not None:
            print(temp.value)
            temp = temp.next
        
    def append(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1
        return True
    
    def prepend(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.length += 1
        return True
    
    def pop_first(self):
        if self.length == 0: # linked list is empty
            return None
        temp = self.head
        self.head = self.head.next
        temp.next = None
        self.length -= 1
        if self.length == 0: #if linked list has length 1
            self.tail = None
        return temp
    
    def get(self, index):
        if index<0 or index>=self.length:
            return None
        flag = 0
        temp = self.head
        while temp.next:
            if index == flag:
                return temp
            else:
                temp = temp.next
                flag += 1
    
    def set_value(self, index, value):
        if index<0 or index>=self.length:
            return None
        temp = self.get(index)
        if temp:
            temp.value = value
            return True
        return False  

    def insert(self, index, value):
        if index<0 or index>=self.length:
            return None
        if index == 0:
            return self.prepend(value)
        if index == self.length:
            return self.append(value)
        temp = self.get(index-1)
        new_node = Node(value)
        if temp:
            next_item = temp.next
            temp.next = new_node
            new_node.next = next_item
            self.length += 1
            return True
        
    def remove(self, index):
        if index<0 or index>=self.length:
            return None
        if index ==0:
            return self.pop_first()
        if index == self.length:
            return self.pop()
        
        temp = self.get(index-1)
        to_remove = temp.next
        next_item = to_remove.next
        temp.next = next_item
        to_remove.next = None
        self.length -= 1
        return to_remove    

    def reverse_ll(self):
        temp = self.head
        self.head = self.tail
        self.tail = temp
        before = None
        after = temp.next
        for _ in range(self.length):
            after = temp.next
            temp.next = before
            before = temp
            temp = after
    
    def find_middle_node(self):
        fast = self.head
        slow = self.head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            
        return slow

    def check_loop(self):
        fast = self.head
        slow = self.head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            if fast==slow:
                return True
        return False
    
    def create_loop(self, index):
        """
        Creates a loop by connecting tail.next to the node at given index
        index is 0-based
        """
        if index < 0 or index >= self.length:
            print("Invalid index")
            return

        loop_node = self.head
        for _ in range(index):
            loop_node = loop_node.next

        # Create the loop
        self.tail.next = loop_node

    def reverse_between(self, start_index, end_index):
        diff_range = end_index-start_index
        dummy = Node(0)
        dummy.next = self.head
        prev = dummy
        for i in range(start_index):
            prev = prev.next
        current = prev.next
        for _ in range(diff_range):
            to_move = current.next
            current.next = to_move.next
            to_move.next = prev.next
            prev.next = to_move

        
        self.head = dummy.next
        return self
            
    def swap_pairs(self):
        dummy = Node(0)
        dummy.next = self.head
        prev = dummy
        first = prev.next
        while first is not None and first.next is not None:
            second = first.next
            prev.next = second
            first.next = second.next
            second.next = first
            prev = first
            first = first.next
        self.head = dummy.next
        return self
    
    def deleteDuplicates(self):
        current = self.head
        while current:
            runner = current
            while runner.next:
                if runner.value == current.next.value:
                    runner.next = runner.next.next
                else:
                    runner = runner.next
            current = current.next
        return self

def remove_duplicates(head):
    current = head
    while current:
        runner = current
        while runner.next:
            if current.value == runner.next.value:
                runner.next = runner.next.next
            else:
                runner = runner.next
        current = current.next
    return head


        


            



    

my_linked_list = LinkedList(1)
my_linked_list.append(1)
my_linked_list.append(1)
# my_linked_list.append(3)
# my_linked_list.append(3)
out = my_linked_list.deleteDuplicates()
out.print_list()
# my_linked_list.pop_first()
# my_linked_list.print_list()
# print(my_linked_list.get(2))
# print(my_linked_list.set_value(0, 22))
# my_linked_list.insert(2,100)

# my_linked_list.print_list()
# print(my_linked_list.remove(3))
# my_linked_list.reverse_ll()
# my_linked_list.create_loop(1)

