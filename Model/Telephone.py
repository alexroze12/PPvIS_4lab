import json


class TelephoneBill:
    def __init__(self):
        self.balance_of_telephone = self.from_json_read_information_about_telephone("balance")

    def from_json_read_information_about_telephone(self, pattern_to_search):
        with open("Utility/telephone.json", "r") as read_file:
            self.telephone_information = read_file.read()
        telephone = json.loads(self.telephone_information)
        self.information_about_telephone = telephone[str(pattern_to_search)]
        return self.information_about_telephone

    def pay_telephone_account(self, amount_of_money):
        self.balance_of_telephone = int(self.balance_of_telephone) + int(amount_of_money)
        return self.balance_of_telephone

    def to_json_write_telephone_balance(self, pattern_to_search, update_summary):
        with open("Utility/telephone.json", "r") as file:
            self.telephone_information = file.read()
        telephone = json.loads(self.telephone_information)
        telephone = json.load(open("Utility/telephone.json"))
        telephone.pop(str(pattern_to_search), None)
        telephone.update({str(pattern_to_search): int(update_summary), })
        self.telephone_information = json.dumps(telephone)
        json.dump(telephone, open("Utility/telephone.json", 'w'))

