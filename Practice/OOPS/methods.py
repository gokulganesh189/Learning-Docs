class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount and amount > 0:
            self.balance += amount
            print(f"Amount deposited {amount}, New balance is {self.balance}")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            print(f"{amount} withdrawn. New balance: {self.balance}")
            
        
acc = BankAccount("Gokul", 1000)
acc.deposit(500)
acc.withdraw(300)