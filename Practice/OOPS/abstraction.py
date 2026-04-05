"""
Abstraction:
Abstraction is the concept of hiding internal implementation details 
and showing only the essential features of an object.

It helps reduce complexity and improves code maintainability.

In Python, abstraction is commonly implemented using:
- Abstract classes
- Abstract methods
- The abc (Abstract Base Class) module

The user interacts with what an object does,
not how it does it.
"""


from abc import ABC, abstractmethod


class Payment(ABC):

    @abstractmethod
    def pay(self, amount):
        pass

class CashPayment(Payment):
    def pay(self, amount):
        print(f"Anount rs {amount} paid as cash payment!!")


class UPIPayment(Payment):
    def pay(self, amount):
        print(f"Anount rs {amount} paid as UPI payment!!")

class CreditCardPayment(Payment):
    def pay(self, amount):
        print(f"Amount rs {amount} paid as CreditCard payment!!")


payment1 = CreditCardPayment()
payment1.pay(1000)

payment2 = UPIPayment()
payment2.pay(500)

payment2 = CashPayment()
payment2.pay(500)