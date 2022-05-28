import os
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from Controller.controller import Controller
from Model.Bank import Bank
from Model.Card_account import CardAccount
from Model.Storage_of_banknotes import StorageOfBanknotes
from Model.Telephone import TelephoneBill
from Controller.controller import pin_validate, digit_validate, banknote_validate

Builder.load_file(os.path.join(os.path.dirname(__file__), "my_screen.kv"))


class PinScreen(Screen):
    def __init__(self, **kw):
        super(PinScreen, self).__init__(**kw)
        s = AnchorLayout(anchor_x='center', anchor_y='top')
        l = Button(text='Hello! Enter your pin!', size_hint=(1, .3), font_size='50sp', disabled=True)
        s.add_widget(l)
        self.add_widget(s)

    def enter_pin(self):
        count = Controller(CardAccount()).from_json_information_about_card("attempts")
        status = Controller(CardAccount()).from_json_information_about_card("status")
        password = Controller(CardAccount()).from_json_information_about_card("password")
        if pin_validate(self.ids.pin.text, password, status):
            self.manager.current = "menu"
        else:
            self.ids.pin.text = "Error!"
            count += 1
            Controller(CardAccount()).write_to_json_information_about_card("attempts", count)
        if Controller(CardAccount()).from_json_information_about_card("attempts") == 3:
            self.ids.pin.text = "Your card is blocked!"
            status = "locked"
            Controller(CardAccount()).write_to_json_information_about_card_status("status", status)
        if Controller(CardAccount()).from_json_information_about_card("status") == "locked":
            self.ids.bank.text = str(Controller(Bank()).from_json_information_about_bank("telephone"))
            self.ids.pin.text = "Call the bank!"

    def unlock_your_card(self):
        count = 0
        status = "unlocked"
        Controller(CardAccount()).write_to_json_information_about_card("attempts", count)
        Controller(CardAccount()).write_to_json_information_about_card_status("status", status)


class GeneralScreen(Screen):
    @staticmethod
    def complete_the_program():
        Controller(CardAccount()).write_to_json_information_about_card("withdrawal", 0)
        exit()


class TemplateTable(Screen):
    def __init__(self, **kw):
        super(TemplateTable, self).__init__(**kw)
        self.data = []
        self.datatable = MDDataTable(
            size_hint=(1, 0.5),
            use_pagination=True,
            rows_num=7,
            column_data=[
                ("Nominal", dp(80)),
                ("Amount", dp(80))
            ]
        )

    def read(self):
        self.datatable.row_data = []
        self.datatable.row_data = Controller(self.datatable.row_data).from_json_storage_of_banknotes()
        Controller(self.datatable).from_json_storage_of_banknotes()

    def on_enter(self):
        self.read()


class WithdrawalMoney(TemplateTable, Screen):
    def __init__(self, **kw):
        super(WithdrawalMoney, self).__init__(**kw)
        s = AnchorLayout(anchor_x='center', anchor_y='top')
        s.add_widget(self.datatable)
        self.add_widget(s)

    def amount_of_withdrawal_money(self):
        card_balance = Controller(CardAccount()).from_json_information_about_card("balance")
        if digit_validate(self.ids.withdrawal.text):
            if Controller(CardAccount()).card_balance_validate() == False or card_balance - int(
                    self.ids.withdrawal.text) < 0:
                self.ids.withdrawal.text = "You have entered an amount that is more than requested! Please, " \
                                           "enter correct data! "
            else:
                self.amount = self.ids.withdrawal.text
        else:
            self.ids.withdrawal.text = "Error!"

    def withdrawal_money(self):
        card_balance = Controller(CardAccount()).from_json_information_about_card("balance")
        summary_withdrawal_money = Controller(CardAccount()).from_json_information_about_card("withdrawal")
        self.ids.amount_of_withdrawal.text = str(self.ids.withdrawal.text)
        self.ids.remainder_amount_of_withdrawal.text = str(
            Controller(CardAccount()).from_json_information_about_card("remaining_amount_to_withdrawal"))
        if banknote_validate(self.ids.nominal.text):
            remainder_amount_of_banknotes = Controller(StorageOfBanknotes()).from_json_storage_balance(
                self.ids.nominal.text)
            amount_of_nominal_money = Controller(StorageOfBanknotes()).from_json_storage_balance(self.ids.nominal.text)
            if digit_validate(self.ids.amount.text) and digit_validate(self.ids.nominal.text):
                if Controller(StorageOfBanknotes()).from_json_storage_balance(self.ids.nominal.text) - int(
                        self.ids.amount.text) >= 0 and int(self.ids.withdrawal.text) - (
                        int(self.ids.nominal.text) * int(self.ids.amount.text)) >= 0:
                    Controller(CardAccount()).withdrawal(int(card_balance), int(self.amount), int(self.ids.nominal.text),
                                                        int(self.ids.amount.text), int(summary_withdrawal_money),
                                                        int(remainder_amount_of_banknotes))
                    self.ids.remainder_amount_of_withdrawal.text = str(
                        Controller(CardAccount()).from_json_information_about_card("remaining_amount_to_withdrawal"))
                    self.amount = Controller(CardAccount()).from_json_information_about_card(
                        "remaining_amount_to_withdrawal")
                else:
                    self.ids.amount.text = "Choose other banknotes or another amount!"
                    self.ids.amount_of_withdrawal.text = "Error!"
                    self.ids.remainder_amount_of_withdrawal.text = "Error!"

            else:
                self.ids.amount.text = "Enter correct data!"
                self.ids.nominal.text = "Enter correct data!"
                self.ids.amount_of_withdrawal.text = "Error!"
                self.ids.remainder_amount_of_withdrawal.text = "Error!"

        else:
            self.ids.amount.text = "Enter correct data!"
            self.ids.nominal.text = "Enter correct data!"
            self.ids.amount_of_withdrawal.text = "Error!"
            self.ids.remainder_amount_of_withdrawal.text = "Error!"


class CheckTheCardBalance(TemplateTable, Screen):
    def __init__(self, **kw):
        super(CheckTheCardBalance, self).__init__(**kw)
        s = AnchorLayout(anchor_x='center', anchor_y='top')
        s.add_widget(self.datatable)
        self.add_widget(s)

    def view_card_balance(self):
        self.ids.card_balance.text = str(Controller(CardAccount()).from_json_information_about_card("balance"))


class PayTheTelephoneBill(Screen):
    def __init__(self, **kw):
        super(PayTheTelephoneBill, self).__init__(**kw)

    def view_telephone_balance(self):
        self.ids.telephone_balance.text = str(
            Controller(TelephoneBill()).from_json_information_about_telephone("balance"))

    def view_card_balance(self):
        self.ids.card_balance.text = str(Controller(CardAccount()).from_json_information_about_card("balance"))

    def update_telephone_balance(self):
        card_balance = Controller(CardAccount()).from_json_information_about_card("balance")
        if Controller(CardAccount()).card_balance_validate() == False or card_balance - int(
                self.ids.update_telephone_account.text) < 0:
            self.ids.update_telephone_account.text = "Error!"
        else:
            self.ids.telephone_balance.text = str(
                Controller(TelephoneBill()).pay_telephone(self.ids.update_telephone_account.text))
            Controller(TelephoneBill()).write_to_json_telephone_balance("balance", self.ids.telephone_balance.text)
            self.ids.card_balance.text = str(
                Controller(CardAccount()).update_card_balance_after_increase_telephone_account(
                    self.ids.update_telephone_account.text))
            Controller(CardAccount()).write_to_json_information_about_card("balance", self.ids.card_balance.text)


class AddBanknotes(Screen):
    def __init__(self, **kw):
        super(AddBanknotes, self).__init__(**kw)

    def add_new_banknotes_to_storage(self):
        self.datatable = MDDataTable(
            size_hint=(1, 0.5),
            use_pagination=True,
            rows_num=7,
            column_data=[
                ("Nominal", dp(80)),
                ("Amount", dp(80))
            ]
        )
        self.datatable.row_data = []
        if digit_validate(self.ids.amount.text) and digit_validate(self.ids.nominal.text):
            Controller(StorageOfBanknotes()).add_banknotes(self.ids.nominal.text, int(self.ids.amount.text))
            self.datatable.row_data = Controller(self.datatable.row_data).from_json_storage_of_banknotes()
            Controller(self.datatable).from_json_storage_of_banknotes()
            s = AnchorLayout(anchor_x='center', anchor_y='center')
            s.add_widget(self.datatable)
            self.add_widget(s)
            del self.datatable
        else:
            self.ids.amount.text = "Enter correct data!"
            self.ids.nominal.text = "Enter correct data!"


class BuildScreen(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PinScreen(name='pin'))
        sm.add_widget(GeneralScreen(name='menu'))
        sm.add_widget(WithdrawalMoney(name='withdrawal'))
        sm.add_widget(CheckTheCardBalance(name='card balance'))
        sm.add_widget(PayTheTelephoneBill(name='telephone bill'))
        sm.add_widget(AddBanknotes(name='add new banknotes'))
        return sm

