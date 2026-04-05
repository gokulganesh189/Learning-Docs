"""
Method Overriding:
When a child class provides a new implementation of a method 
that already exists in the parent class using the same method name.
Requires inheritance and happens at runtime.
"""

class User:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return "Hello User"
    
    def get_name(self):
        return self.name


class Admin(User):
    def __init__(self, name):
        super().__init__(name)

    def greet(self):
        user_msg = super().greet()  # method overriding
        return f"{user_msg} You are an Admin"
    
    def greet_user(self):
        user_name = super().get_name()
        return f"You are an Admin and name is {user_name}"

user = User("Gokul")
print(user.greet())

admin = Admin("Ganesh")
print(admin.greet())
print(admin.greet_user())