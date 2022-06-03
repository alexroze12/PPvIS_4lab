import json
from Model.Card_account import CardAccount


class TelephoneBill:
    def __init__(self):
        pass

    @staticmethod
    def get_information_about_telephone():
        with open("Utility/bank_data.json", "r") as read_file:
            data = json.load(read_file)
            return data["telephone_balance"]

    @staticmethod
    def pay_telephone_account(amount_of_money):
        card_balance = CardAccount.get_information_about_card("balance")
        if int(amount_of_money) > card_balance:
            return "You have entered an amount that is more than requested! Please, enter correct data!"
        CardAccount.set_information_about_card("balance", card_balance - int(amount_of_money), True)
        with open("Utility/bank_data.json", "r") as read_file:
            new_balance = TelephoneBill.get_information_about_telephone() + int(amount_of_money)
            bank_data = json.load(read_file)
        bank_data["telephone_balance"] = new_balance
        with open("Utility/bank_data.json", "w") as write_file:
            json.dump(bank_data, write_file, indent=5)
        return "Correct"
