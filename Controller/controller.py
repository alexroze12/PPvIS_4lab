import json


class Controller:
    def __init__(self, model):
        self.model = model

    def from_json_information_about_card(self, pattern_to_search):
        return self.model.from_json_read_information_about_card(pattern_to_search)

    def write_to_json_information_about_card(self, pattern_to_search, component):
        self.model.to_json_write_information_about_card(pattern_to_search, component)

    def write_to_json_information_about_card_status(self, pattern_to_search, component):
        self.model.to_json_write_information_about_card_status(pattern_to_search, component)

    def from_json_storage_of_banknotes(self):
        with open("Utility/storage_of_banknotes.json", "r") as read_file:
            storage_information = read_file.read()
        storage = json.loads(storage_information)
        return list(storage.items())

    def from_json_storage_balance(self, nominal):
        return self.model.from_json_read_storage_balance(nominal)

    def write_to_json_storage_balance(self, nominal, update_banknote):
        self.model.to_json_write_storage_balance(nominal, update_banknote)

    def withdrawal(self, balance_of_card, withdrawal_amount_of_money, nominal, amount_of_banknotes,
                       summary_withdrawal_money, remainder_amount_in_storage_of_banknotes):
        self.model.withdrawal_amount_of_money(balance_of_card, withdrawal_amount_of_money, nominal, amount_of_banknotes,
                                              summary_withdrawal_money, remainder_amount_in_storage_of_banknotes)

    def add_banknotes(self, nominal, amount):
        self.model.add_new_banknotes(nominal, amount)

    def pay_telephone(self, amount_of_money):
        return self.model.pay_telephone_account(amount_of_money)

    def update_card_balance_after_increase_telephone_account(self, amount_of_money):
        if self.model.balance - int(amount_of_money) >= 0:
            self.model.balance = self.model.balance - int(amount_of_money)
            return self.model.balance
        else:
            pass

    def card_balance_validate(self):
        if self.model.balance == 0:
            return False
        else:
            return True

    def from_json_information_about_telephone(self, pattern_to_search):
        return self.model.from_json_read_information_about_telephone(pattern_to_search)

    def from_json_information_about_bank(self, pattern_to_search):
        return self.model.from_json_read_information_about_bank(pattern_to_search)

    def write_to_json_telephone_balance(self, pattern_to_search, update_summary):
        self.model.to_json_write_telephone_balance(pattern_to_search, update_summary)


def pin_validate(pin: str, password, status):
    if len(pin) == 4 and pin.isdigit() and pin == str(password) and status == "unlocked":
        return True
    else:
        return False


def digit_validate(amount: str):
    if amount.isdigit():
        return True
    else:
        return False


def banknote_validate(banknote: str):
    with open("Utility/storage_of_banknotes.json", "r") as read_file:
        storage_information = read_file.read()
    storage = json.loads(storage_information)
    t = list(storage.keys())
    for i in range(0, len(t)):
        if banknote == t[i]:
            return True
        else:
            continue

