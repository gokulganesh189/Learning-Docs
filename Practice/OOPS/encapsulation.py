class User:
    def __init__(self, name, age, phone, sex):
        self.name = name
        self.age = age
        self._phone = phone # non mangling
        self.__sex = sex # python convertes to _User__sex if it is __ double underscore


    def __str__(self):
        return f"""The user name is {self.name} and age is {self.age} and phone is {self._phone} sex {self._User__sex}|{self.__sex}"""  
        #both will work {self._User__sex}|{self.__sex}
    

new_user = User("Gokul", "28", "3245", "Male")
print(new_user)
print(new_user._phone)
print(new_user._User__sex)