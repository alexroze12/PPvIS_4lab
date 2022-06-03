import json


class StorageOfBanknotes:
    def __init__(self):
        pass

    @staticmethod
    def get_nominal_storage_balance(nominal):
        with open("Utility/bank_data.json", "r") as read_file:
            bank_data = json.load(read_file)
            return bank_data["storage"][nominal]

    @staticmethod
    def set_nominal_storage_balance(nominal, amount):
        with open("Utility/bank_data.json", "r") as read_file:
            bank_data = json.load(read_file)
        bank_data["storage"][nominal] = amount
        with open("Utility/bank_data.json", "w") as write_file:
            json.dump(bank_data, write_file, indent=5)

    @staticmethod
    def get_storage_balance():
        with open("Utility/bank_data.json", "r") as read_file:
            return list(json.load(read_file)["storage"].items())
