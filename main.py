total_balance = 0.0
correct_pin = "0000"
is_running = True
pin = input("Please insert your card and enter your pin_code: ")

def login():
    if pin == correct_pin:
        print("Welcome Account User")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Exit options")
    else:
        print("Incorrect pin.\nPlease try again.")
        login()


def check_balance():
    print(f'Your Balance is {total_balance:.2f} HUF')

def deposit_money():
    deposit= float(input("Enter the amount you'll like to deposit: "))
    if deposit < 0:
        print("Invalid amount!")
        return 0
    else:
        return deposit

def withdraw_money():
    withdrawal = float(input("Enter the amount you'll like to withdraw: "))
    if withdrawal > total_balance:
        print("Insufficient funds!")
        return 0
    elif withdrawal < 0:
        print("Invalid amount!")
        return 0
    else:
        return withdrawal

login()
while is_running:
    choice = input("Enter your choice(1-4): ")

    if choice == "1":
        check_balance()


    elif choice == "2":
        total_balance += deposit_money()
        print(f"Deposit successful. New balance: {total_balance:.2f} HUF")


    elif choice == "3":
        total_balance -= withdraw_money()


    elif choice == "4":
        is_running = False

    else:
        print("Invalid option")


print("Thank you for banking with us.")

