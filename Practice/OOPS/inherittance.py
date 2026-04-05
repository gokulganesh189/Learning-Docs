class User:
    def __init__(self, name):
        self.name = name

    def login(self):
        print(f"{self.name} logged in")

class Admin(User):
    def delete_user(self):
        print(f"{self.name} deleted a user")


admin = Admin("Gokul")
admin.login()
admin.delete_user()

