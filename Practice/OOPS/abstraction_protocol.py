from typing import Protocol


class PaymentProtocol(Protocol):
    def pay(self, amount: float) -> None:
        ...


class CashPayment:
    def pay(self, amount):
        print(f"Anount rs {amount} paid as cash payment!!")


class UPIPayment:
    def pay(self, amount):
        print(f"Anount rs {amount} paid as UPI payment!!")

class CreditCardPayment:
    def pay(self, amount):
        print(f"Amount rs {amount} paid as CreditCard payment!!")


def process_payment(payment: PaymentProtocol):
    payment.pay(1000)


payment1 = CreditCardPayment()
payment2 = UPIPayment()
payment3 = CashPayment()

process_payment(payment1)
process_payment(payment2)
process_payment(payment3)