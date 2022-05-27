import json


class StorageOfBanknotes:
    def __init__(self):
        self.amount_storage = {}

    def from_json_read_storage_balance(self, nominal):
        with open("Utility/storage_of_banknotes.json", "r") as read_file:
            self.storage_information = read_file.read()
        storage = json.loads(self.storage_information)
        self.amount_storage = storage[str(nominal)]
        return self.amount_storage

    def to_json_write_storage_balance(self, nominal, update_banknote):
        with open("Utility/storage_of_banknotes.json", "r") as file:
            self.storage_information = file.read()
        storage = json.loads(self.storage_information)
        storage = json.load(open("Utility/storage_of_banknotes.json"))
        storage.pop(str(nominal), None)
        storage.update({str(nominal): int(update_banknote), })
        self.storage_information = json.dumps(storage)
        json.dump(storage, open("Utility/storage_of_banknotes.json", 'w'))

    def add_new_banknotes(self, nominal, amount):
        with open("Utility/storage_of_banknotes.json", "r") as file:
            self.storage_information = file.read()
        storage = json.loads(self.storage_information)
        storage = json.load(open("Utility/storage_of_banknotes.json"))
        storage[str(nominal)] = amount
        self.storage_information = json.dumps(storage)
        json.dump(storage, open("Utility/storage_of_banknotes.json", 'w'))



