import json
from Model.Storage_of_banknotes import StorageOfBanknotes


class CardAccount:
    def __init__(self):
        self.balance = self.from_json_read_information_about_card("balance")
        self.password = self.from_json_read_information_about_card("password")
        self.withdrawal = self.from_json_read_information_about_card("withdrawal")
        self.remaining_withdrawal = self.from_json_read_information_about_card("remaining_amount_to_withdrawal")

    def from_json_read_information_about_card(self, pattern_to_search):
        with open("Utility/cards.json", "r") as read_file:
            self.card_information = read_file.read()
        card = json.loads(self.card_information)
        self.information_about_card = card[str(pattern_to_search)]
        return self.information_about_card

    def to_json_write_information_about_card(self, pattern_to_search, component):
        with open("Utility/cards.json", "r") as file:
            self.card_information = file.read()
        card = json.loads(self.card_information)
        card = json.load(open("Utility/cards.json"))
        card.pop(str(pattern_to_search), None)
        card.update({str(pattern_to_search): int(component), })
        self.card_information = json.dumps(card)
        json.dump(card, open("Utility/cards.json", 'w'))

    def write_to_json_storage_balance(self, nominal, update_banknote):
        StorageOfBanknotes().to_json_write_storage_balance(nominal, update_banknote)

    def to_json_write_information_about_card_status(self, pattern_to_search, component):
        with open("Utility/cards.json", "r") as file:
            self.card_information = file.read()
        card = json.loads(self.card_information)
        card = json.load(open("Utility/cards.json"))
        card.pop(str(pattern_to_search), None)
        card.update({str(pattern_to_search): str(component), })
        self.card_information = json.dumps(card)
        json.dump(card, open("Utility/cards.json", 'w'))

    def withdrawal_amount_of_money(self, balance_of_card, withdrawal_amount_of_money, nominal, amount_of_banknotes,
                                       summary_withdrawal_money, remainder_amount_in_storage_of_banknotes):
        summary_withdrawal_money = withdrawal_amount_of_money + summary_withdrawal_money
        while withdrawal_amount_of_money != 0:
            if remainder_amount_in_storage_of_banknotes - amount_of_banknotes >= 0 and withdrawal_amount_of_money - (
                    amount_of_banknotes * nominal) >= 0:
                final_amount_to_send_to_storage = remainder_amount_in_storage_of_banknotes-amount_of_banknotes
                self.write_to_json_storage_balance(nominal, final_amount_to_send_to_storage)
            elif remainder_amount_in_storage_of_banknotes - amount_of_banknotes < 0:
                continue
            balance_of_card = balance_of_card - (amount_of_banknotes * nominal)
            if withdrawal_amount_of_money - (amount_of_banknotes * nominal) < 0:
                pass
            else:
                withdrawal_amount_of_money = withdrawal_amount_of_money - (amount_of_banknotes * nominal)
            print("The remaining amount to be withdrawn: "+str(withdrawal_amount_of_money))
            self.to_json_write_information_about_card("remaining_amount_to_withdrawal", withdrawal_amount_of_money)
            self.to_json_write_information_about_card("balance", balance_of_card)
            self.to_json_write_information_about_card("withdrawal", summary_withdrawal_money)
            break

