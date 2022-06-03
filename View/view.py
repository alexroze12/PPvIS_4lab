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
from Model.Telephone import TelephoneBill
from Model.Card_account import CardAccount
from Model.Storage_of_banknotes import StorageOfBanknotes
Builder.load_file(os.path.join(os.path.dirname(__file__), "my_screen.kv"))


class PinScreen(Screen):
    def __init__(self, **kw):
        super(PinScreen, self).__init__(**kw)
        s = AnchorLayout(anchor_x='center', anchor_y='top')
        button = Button(text='Hello! Enter your pin!', size_hint=(1, .3), font_size='50sp', disabled=True)
        s.add_widget(button)
        self.add_widget(s)

    def enter_pin(self):
        count = Controller.get_information_about_card_attempts()
        if Controller.pin_validate(self.ids.pin.text):
            self.manager.current = "menu"
            Controller.set_information_about_card_attempts(0)
        else:
            self.ids.pin.text = "Error!"
            count += 1
            Controller.set_information_about_card_attempts(count)
        if count == 3:
            self.ids.pin.text = "Your card is blocked!"
            Controller.set_information_about_card_status("locked")
        if Controller.get_information_about_card_status() == "locked":
            self.ids.bank.text = str(Controller.get_information_about_bank_telephone())
            self.ids.pin.text = "Call the bank!"

    @staticmethod
    def unlock_your_card():
        Controller.unlock_your_card()


class GeneralScreen(Screen):
    @staticmethod
    def complete_the_program():
        Controller.set_information_about_card_withdrawal(0)
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

    def on_enter(self):
        self.datatable.row_data = Controller.get_information_about_storage_of_banknotes()


class WithdrawalMoney(TemplateTable):
    def __init__(self, **kw):
        super(WithdrawalMoney, self).__init__(**kw)
        s = AnchorLayout(anchor_x='center', anchor_y='top')
        s.add_widget(self.datatable)
        self.add_widget(s)

    def amount_of_withdrawal_money(self):
        self.ids.withdrawal.text = Controller.amount_of_withdrawal_money(self.ids.withdrawal.text)
        self.ids.remainder_amount_of_withdrawal.text = str(Controller.get_information_about_remaining_amount_to_withdrawal())
        self.ids.amount_of_withdrawal.text = str(Controller.get_information_about_remaining_amount_to_withdrawal())

    def withdrawal_money(self):
        message = Controller.withdrawal_money(self.ids.nominal.text, self.ids.amount.text)
        if message != "Correct":
            self.ids.amount.text = message
            self.ids.nominal.text = message
            return
        self.ids.remainder_amount_of_withdrawal.text = str(Controller.get_information_about_remaining_amount_to_withdrawal())
        self.on_enter()


class CheckTheCardBalance(TemplateTable):
    def __init__(self, **kw):
        super(CheckTheCardBalance, self).__init__(**kw)
        s = AnchorLayout(anchor_x='center', anchor_y='top')
        s.add_widget(self.datatable)
        self.add_widget(s)

    def on_home_press(self):
        self.ids.card_balance.text = "card_balance"
        self.manager.current = "menu"

    def view_card_balance(self):
        self.ids.card_balance.text = str(Controller.get_information_about_card_balance())


class PayTheTelephoneBill(Screen):
    def __init__(self, **kw):
        super(PayTheTelephoneBill, self).__init__(**kw)

    def view_telephone_balance(self):
        self.ids.telephone_balance.text = str(Controller.get_information_about_telephone_balance())

    def view_card_balance(self):
        self.ids.card_balance.text = str(Controller.get_information_about_card_balance())

    def update_telephone_balance(self):
        self.ids.update_telephone_account.text = Controller.pay_telephone_account(self.ids.update_telephone_account.text)


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
        message = Controller.add_new_banknote(self.ids.nominal.text, self.ids.amount.text)
        if message != "Correct":
            self.ids.amount.text = "Enter correct data!"
            self.ids.nominal.text = "Enter correct data!"
            return
        self.datatable.row_data = Controller.get_information_about_storage_of_banknotes()
        s = AnchorLayout(anchor_x='center', anchor_y='center')
        s.add_widget(self.datatable)
        self.add_widget(s)
        del self.datatable


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
