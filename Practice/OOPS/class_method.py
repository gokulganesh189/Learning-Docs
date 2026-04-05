class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    @classmethod
    def from_string(cls, data_str):
        name,age = data_str.split(",")
        return cls(name, int(age))
    
    def __str__(self):
        return f"""The user name is {self.name} and age is {self.age}"""

user = User.from_string("Gokul,21")
user2 = User.from_string("Arjun,23")
print(user)
print(user2)