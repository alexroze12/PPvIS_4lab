from Model.Bank import Bank
from Model.Telephone import TelephoneBill
from Model.Card_account import CardAccount
from Model.Storage_of_banknotes import StorageOfBanknotes


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def get_information_about_card_balance():
        return CardAccount.get_information_about_card("balance")

    @staticmethod
    def get_information_about_card_status():
        return CardAccount.get_information_about_card("status")

    @staticmethod
    def get_information_about_card_attempts():
        return CardAccount.get_information_about_card("attempts")

    @staticmethod
    def get_information_about_card_withdrawal():
        return CardAccount.get_information_about_card("withdrawal")

    @staticmethod
    def get_information_about_card_number():
        return CardAccount.get_information_about_card("card_number")

    @staticmethod
    def get_information_about_remaining_amount_to_withdrawal():
        return CardAccount.get_information_about_card("remaining_amount_to_withdrawal")

    @staticmethod
    def get_information_about_bank_telephone():
        return Bank.get_information_about_bank()

    @staticmethod
    def get_information_about_telephone_balance():
        return TelephoneBill.get_information_about_telephone()

    @staticmethod
    def get_information_about_storage_of_banknotes():
        return StorageOfBanknotes.get_storage_balance()

    @staticmethod
    def set_information_about_card_status(status):
        return CardAccount.set_information_about_card("status", status, False)

    @staticmethod
    def set_information_about_card_attempts(attempts):
        return CardAccount.set_information_about_card("attempts", attempts, True)

    @staticmethod
    def set_information_about_card_withdrawal(withdrawal):
        return CardAccount.set_information_about_card("withdrawal", withdrawal, True)

    @staticmethod
    def pin_validate(pin: str):
        password = CardAccount.get_information_about_card("password")
        status = CardAccount.get_information_about_card("status")
        if len(pin) == 4 and pin.isdigit() and pin == str(password) and status == "unlocked":
            return True
        return False

    @staticmethod
    def banknote_validate(banknote: str):
        storage = CardAccount.get_information_about_card("storage")
        if banknote in list(storage.keys()):
            return True
        return False

    @staticmethod
    def digit_validate(amount: str):
        if amount.isdigit():
            return True
        return False

    @staticmethod
    def amount_of_withdrawal_money(amount_to_withdrawal):
        if Controller.digit_validate(amount_to_withdrawal):
            return CardAccount.amount_of_withdrawal_money(amount_to_withdrawal)
        return "Error"

    @staticmethod
    def withdrawal_money(nominal, amount):
        if Controller.banknote_validate(nominal) and Controller.digit_validate(nominal) and Controller.digit_validate(
                amount):
            return CardAccount.withdrawal_money(nominal, amount)
        return "Error"

    @staticmethod
    def pay_telephone_account(amount_of_money):
        if Controller.digit_validate(amount_of_money):
            return TelephoneBill.pay_telephone_account(amount_of_money)
        return "Error"

    @staticmethod
    def add_new_banknote(nominal, amount):
        if Controller.digit_validate(nominal) and Controller.digit_validate(amount):
            StorageOfBanknotes.set_nominal_storage_balance(nominal, int(amount))
            return "Correct"
        return "Error"

    @staticmethod
    def unlock_your_card():
        CardAccount.set_information_about_card("attempts", 0, True)
        CardAccount.set_information_about_card("status", "unlocked", False)
