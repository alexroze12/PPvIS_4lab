import argparse
import shutil
from datetime import datetime
from Model.Card_account import CardAccount
from Model.Telephone import TelephoneBill
from Model.Storage_of_banknotes import StorageOfBanknotes
from Controller.controller import pin_validate, digit_validate, Controller

balance_on_telephone = Controller(TelephoneBill()).from_json_information_about_telephone("balance")
balance_on_your_card = Controller(CardAccount()).from_json_information_about_card("balance")
cash_for_withdrawal = Controller(CardAccount()).from_json_information_about_card("withdrawal")
status_of_card = Controller(CardAccount()).from_json_information_about_card("status")
password = Controller(CardAccount()).from_json_information_about_card("password")

parser = argparse.ArgumentParser(description="This program is about ATM simulation")
parser.add_argument("p", type=int, help="Hello! Please, enter your pin:")
parser.add_argument("sp", type=int, help="Hello! Please, enter your pin:")
parser.add_argument("tp", type=int, help="Hello! Please, enter your pin:")
parser.add_argument("-b", "--balance", help="View catd balance", nargs="?", const=balance_on_your_card)
parser.add_argument("-tb", "--telephone_balance", help="View telephone balance", nargs="?", const=balance_on_telephone)
parser.add_argument("-w", "--withdrawal", type=int, help="Amount of withdrawal money and write check about operation", nargs="?")
parser.add_argument("-sw", "--sum_withdrawal", help="Summary amount of withdrawal money during the operation",
                    nargs="?", const=cash_for_withdrawal)
parser.add_argument("-u", "--unlock", help="Unlock card", nargs="?", const='locked')
parser.add_argument("-n", "--nominal", type=str, help="Necessary nominal of money to withdrawal money")
parser.add_argument("-a", "--amount",  type=str, help="Necessary amount of money to withdrawal money")
parser.add_argument("-nb", "--new_banknote", help="Add new banknote", nargs="?", const='status')
parser.add_argument("-ann", "--add_new_nominal", type=int, help="Add new banknote (nominal)", nargs="?")
parser.add_argument("-ana", "--add_new_amount", type=int, help="Add new banknote (amount)", nargs="?")
parser.add_argument("-t", "--telephone_pay", type=str, help="Pay the telephone bill and write check about operation")
args = parser.parse_args()

if status_of_card == "locked":
    if args.unlock:
        Controller(CardAccount()).write_to_json_information_about_card_status("status", "unlocked")
        print("Card is unlocked!")
    else:
        exit()
if pin_validate(str(args.p), password, Controller(CardAccount()).from_json_information_about_card("status")) == False and pin_validate(str(args.sp), password, Controller(CardAccount()).from_json_information_about_card("status")) == False and pin_validate(str(args.tp), password, Controller(CardAccount()).from_json_information_about_card("status")) == False:
    print("Error! Your card is blocked! You have 0 attempts!")
    Controller(CardAccount()).write_to_json_information_about_card_status("status", "locked")
else:
    if args.balance:
        print("Your card balance: "+str(args.balance))
    if args.telephone_balance:
        print("Your telephone balance: "+str(args.telephone_balance))
    if args.withdrawal:
        card_balance = Controller(CardAccount()).from_json_information_about_card("balance")
        summary_withdrawal_money = Controller(CardAccount()).from_json_information_about_card("withdrawal")
        remainder_amount_in_storage_of_banknotes = Controller(StorageOfBanknotes()).from_json_storage_balance(
            str(args.nominal))
        if digit_validate(args.nominal) and digit_validate(args.amount):
            if card_balance - args.withdrawal >= 0 and remainder_amount_in_storage_of_banknotes - int(args.amount) >= 0:
                Controller(CardAccount()).withdrawal(card_balance, args.withdrawal, int(args.nominal), int(args.amount),
                                                     summary_withdrawal_money, remainder_amount_in_storage_of_banknotes)
                shutil.copyfile("Utility/Check_pattern.txt", "D:\\Python\\ppvis4\\Check_withdrawal.txt")
                with open("Check_withdrawal.txt", "a") as document:
                    current_date = datetime.now().date()
                    document.write("DATE: " + str(current_date))
                    current_time = datetime.now().time()
                    document.write("\nTIME: " + str(current_time))
                    document.write(
                        "\nCARD ACCOUNT: " + str(Controller(CardAccount()).from_json_information_about_card("card_number")))
                    document.write("\nCASH WITHDRAWAL: " + str(
                        Controller(CardAccount()).from_json_information_about_card("withdrawal")))
                    document.write("\n\nBANK APPROVED. CODE:000")
                    document.write("\n\n      THANK YOU!\n\n")
                Controller(CardAccount()).write_to_json_information_about_card("withdrawal", 0)
            else:
                print("Enter correct data!")
        else:
            print("Enter correct data!")
    if args.sum_withdrawal:
        print(args.sum_withdrawal)
    if args.telephone_pay:
        if digit_validate(args.telephone_pay):
            if args.balance - int(args.telephone_pay) >= 0:
                telephone_balance = Controller(TelephoneBill()).pay_telephone(args.telephone_pay)
                print("Your telephone balance before payment: " + str(telephone_balance))
                Controller(TelephoneBill()).write_to_json_telephone_balance("balance", telephone_balance)
                card_balance = Controller(CardAccount()).from_json_information_about_card("balance")
                final_card_balance = card_balance - int(args.telephone_pay)
                Controller(CardAccount()).write_to_json_information_about_card("balance", final_card_balance)
                telephone_balance_after_payment = telephone_balance + int(args.telephone_pay)
                Controller(TelephoneBill()).write_to_json_telephone_balance("balance", telephone_balance_after_payment)
                print("Your current telephone balance: "+str(telephone_balance_after_payment))
                print("Your current card balance: " + str(final_card_balance))
                shutil.copyfile("Utility/Check_mobile_pattern.txt", "D:\\Python\\ppvis4\\Check_telephone_bill.txt")
                with open("Check_telephone_bill.txt", "a") as material:
                    current_date_mobile = datetime.now().date()
                    material.write("DATE: " + str(current_date_mobile))
                    current_time_mobile = datetime.now().time()
                    material.write("\nTIME: " + str(current_time_mobile))
                    material.write(
                        "\nCARD ACCOUNT: " + str(Controller(CardAccount()).from_json_information_about_card("card_number")))
                    material.write("\nMONEY TRANSFER TO PHONE: " + str(args.telephone_pay))
                    material.write("\n\nBANK APPROVED. CODE:000")
                    material.write("\n\n      THANK YOU!\n\n")
            else:
                print("Enter correct data!")
        else:
            print("Enter correct data!")

    if args.new_banknote:
        if digit_validate(str(args.add_new_nominal)) and digit_validate(str(args.add_new_amount)):
            Controller(StorageOfBanknotes()).add_banknotes(str(args.add_new_nominal), int(args.add_new_amount))
        else:
            print("Enter correct data!")

