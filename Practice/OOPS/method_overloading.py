"""
Method Overloading:
Defining multiple methods with the same name but different parameters.
Python does not support traditional method overloading.
It can be simulated using default arguments or *args.
"""

class Test:
    def add(self, a, b, c=0): # using kwargs or args for methof overloading 
        return a + b + c

t = Test()
print(t.add(1, 2))      # 3
print(t.add(1, 2, 3))   # 6
