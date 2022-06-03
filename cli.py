import argparse
import shutil
from datetime import datetime
from Controller.controller import Controller

balance_on_telephone = Controller.get_information_about_telephone_balance()
balance_on_your_card = Controller.get_information_about_card_balance()
cash_for_withdrawal = Controller.get_information_about_remaining_amount_to_withdrawal()
status_of_card = Controller.get_information_about_card_status()

parser = argparse.ArgumentParser(description="This program is about ATM simulation")
parser.add_argument("p", type=str, help="Hello! Please, enter your pin:")
parser.add_argument("sp", type=str, help="Hello! Please, enter your pin:")
parser.add_argument("tp", type=str, help="Hello! Please, enter your pin:")
parser.add_argument("-b", "--balance", help="View catd balance", nargs="?", const=balance_on_your_card)
parser.add_argument("-tb", "--telephone_balance", help="View telephone balance", nargs="?", const=balance_on_telephone)
parser.add_argument("-w", "--withdrawal", help="Amount of withdrawal money and write check about operation", nargs="?", const=cash_for_withdrawal)
parser.add_argument("-sw", "--sum_withdrawal", type=str, help="Summary amount of withdrawal money during the operation",
                   nargs="?")
parser.add_argument("-u", "--unlock", help="Unlock card", nargs="?", const='locked')
parser.add_argument("-n", "--nominal", type=str, help="Necessary nominal of money to withdrawal money")
parser.add_argument("-a", "--amount",  type=str, help="Necessary amount of money to withdrawal money")
parser.add_argument("-nb", "--new_banknote", help="Add new banknote", nargs="?", const='status')
parser.add_argument("-ann", "--add_new_nominal", type=str, help="Add new banknote (nominal)", nargs="?")
parser.add_argument("-ana", "--add_new_amount", type=str, help="Add new banknote (amount)", nargs="?")
parser.add_argument("-t", "--telephone_pay", type=str, help="Pay the telephone bill and write check about operation")
args = parser.parse_args()

if status_of_card == "locked":
    if args.unlock:
        Controller.set_information_about_card_status("unlocked")
        print("Card is unlocked!")
    else:
        exit()
if Controller.pin_validate(str(args.p)) == False and Controller.pin_validate(str(args.sp)) == False and Controller.pin_validate(str(args.tp)) == False:
    print("Error! Your card is blocked! You have 0 attempts!")
    Controller.set_information_about_card_status("locked")
else:
    if args.balance:
        print("Your card balance: "+str(args.balance))
    if args.telephone_balance:
        print("Your telephone balance: "+str(args.telephone_balance))
    if args.sum_withdrawal:
        message = Controller.amount_of_withdrawal_money(args.sum_withdrawal)
    if args.withdrawal:
        withdrawal_message = Controller.withdrawal_money(args.nominal, args.amount)
        if withdrawal_message == "Correct":
            if Controller.get_information_about_remaining_amount_to_withdrawal() == 0:
                shutil.copyfile("Checks/Check_pattern.txt", "D:\\Python\\ppvis4\\Checks\\Check_withdrawal.txt")
                with open("Checks/Check_withdrawal.txt", "a") as document:
                    current_date = datetime.now().date()
                    document.write("DATE: " + str(current_date))
                    current_time = datetime.now().time()
                    document.write("\nTIME: " + str(current_time))
                    document.write(
                        "\nCARD ACCOUNT: " + str(Controller.get_information_about_card_number()))
                    document.write("\nCASH WITHDRAWAL: " + str(Controller.get_information_about_card_withdrawal()))
                    document.write("\n\nBANK APPROVED. CODE:000")
                    document.write("\n\n      THANK YOU!\n\n")
                Controller.set_information_about_card_withdrawal(0)
            print("Remaining amount of money to withdrawal: " + str(
                Controller.get_information_about_remaining_amount_to_withdrawal()))
        else:
            print("Enter correct data!")
    if args.telephone_pay:
        print("Your telephone balance before payment: " + str(balance_on_telephone))
        print("Your card balance before payment: " + str(balance_on_your_card))
        message = Controller.pay_telephone_account(args.telephone_pay)
        if message == "Correct":
            print("Your current telephone balance: " + str(Controller.get_information_about_telephone_balance()))
            print("Your current card balance: " + str(Controller.get_information_about_card_balance()))
            shutil.copyfile("Checks/Check_mobile_pattern.txt", "D:\\Python\\ppvis4\\Checks\\Check_telephone_bill.txt")
            with open("Checks/Check_telephone_bill.txt", "a") as material:
                current_date_mobile = datetime.now().date()
                material.write("DATE: " + str(current_date_mobile))
                current_time_mobile = datetime.now().time()
                material.write("\nTIME: " + str(current_time_mobile))
                material.write(
                    "\nCARD ACCOUNT: " + str(Controller.get_information_about_card_number()))
                material.write("\nMONEY TRANSFER TO PHONE: " + str(args.telephone_pay))
                material.write("\n\nBANK APPROVED. CODE:000")
                material.write("\n\n      THANK YOU!\n\n")
        else:
            print("Enter correct data!")
    if args.new_banknote:
        message = Controller.add_new_banknote(str(args.add_new_nominal), str(args.add_new_amount))
        if message != "Correct":
            print("Enter correct data!")
