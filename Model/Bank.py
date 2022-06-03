import json


class Bank:
    def __init__(self):
        pass

    @staticmethod
    def get_information_about_bank():
        with open("Utility/bank_data.json", "r") as read_file:
            bank_data = json.load(read_file)
            return bank_data["bank_telephone"]
