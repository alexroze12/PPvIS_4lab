import json


class Bank:
    def __init__(self):
        self.bank_telephone = self.from_json_read_information_about_bank("telephone")

    def from_json_read_information_about_bank(self, pattern_to_search):
        with open("Utility/bank.json", "r") as read_file:
            self.bank_information = read_file.read()
        bank = json.loads(self.bank_information)
        self.information_about_bank = bank[str(pattern_to_search)]
        return self.information_about_bank
