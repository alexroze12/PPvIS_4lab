import json
from Model.Storage_of_banknotes import StorageOfBanknotes


class CardAccount:
    def __init__(self):
        pass

    @staticmethod
    def get_information_about_card(pattern_to_search):
        with open("Utility/bank_data.json", "r") as read_file:
            bank_data = json.load(read_file)
            return bank_data[pattern_to_search]

    @staticmethod
    def set_information_about_card(pattern_to_search, component, is_that_integer):
        with open("Utility/bank_data.json", "r") as read_file:
            bank_data = json.load(read_file)
        if is_that_integer:
            component = int(component)
        bank_data[pattern_to_search] = component
        with open("Utility/bank_data.json", "w") as write_file:
            json.dump(bank_data, write_file, indent=5)

    @staticmethod
    def amount_of_withdrawal_money(amount_to_withdrawal):
        remaining_card_balance = CardAccount.get_information_about_card("balance")
        if int(amount_to_withdrawal) > remaining_card_balance:
            return "You have entered an amount that is more than requested! Please, enter correct data!"
        CardAccount.set_information_about_card("remaining_amount_to_withdrawal", amount_to_withdrawal, True)
        return "Correct"

    @staticmethod
    def withdrawal_money(nominal, amount):
        remaining_amount_to_withdrawal = CardAccount.get_information_about_card("remaining_amount_to_withdrawal")
        summary_amount_to_withdrawal = CardAccount.get_information_about_card("withdrawal")
        remaining_card_balance = CardAccount.get_information_about_card("balance")
        remaining_amount_of_banknotes_in_storage = StorageOfBanknotes.get_nominal_storage_balance(nominal)
        addition = int(amount) * int(nominal)
        remaining_amount_to_withdrawal -= addition
        summary_amount_to_withdrawal += addition
        remaining_card_balance -= addition
        remaining_amount_of_banknotes_in_storage -= int(amount)
        if remaining_card_balance < 0 or remaining_amount_of_banknotes_in_storage < 0 or remaining_amount_to_withdrawal < 0:
            return "You have entered an amount that is more than requested! Please, enter correct data!"
        CardAccount.set_information_about_card("balance", remaining_card_balance, True)
        CardAccount.set_information_about_card("withdrawal", summary_amount_to_withdrawal, True)
        CardAccount.set_information_about_card("remaining_amount_to_withdrawal", remaining_amount_to_withdrawal, True)
        StorageOfBanknotes.set_nominal_storage_balance(nominal, remaining_amount_of_banknotes_in_storage)
        return "Correct"
