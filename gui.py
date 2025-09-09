import tkinter as tk
from tkinter import messagebox
total_balance = 0.0
correct_pin = "0000"


def check_pin():
    entered_pin = pin_entry.get()
    if entered_pin == correct_pin:
        pin_frame.pack_forget()
        show_menu()
    else:
        messagebox.showerror("Error","Incorrect PIN. Try again.")

def show_menu():
    menu_frame.pack(pady=20)

def gui_check_balance():
    message_label.config(text=f"Your Balance is {total_balance:.2f} HUF", fg="yellow")

def gui_deposit_money():
    global total_balance
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            message_label.config(text="Invalid amount!", fg="red")
        else:
            total_balance += amount
            message_label.config(text=f"Deposited {amount:.2f} HUF.", fg="lightgreen")
    except ValueError:
        message_label.config(text="Please enter a valid number!", fg="red")


def gui_withdrawal_money():
    global  total_balance
    try:
        amount = float(amount_entry.get())
        if amount > total_balance:
             message_label.config(text="Insufficient funds!", fg="red")
        elif amount <= 0:
            message_label.config(text="Invalid amount!", fg="red")
        else:
            total_balance -= amount
            message_label.config(text=f"Withdrawal {amount:.2f} HUF.", fg="lightgreen")
    except ValueError:
        message_label.config(text="Please enter a valid number.", fg="red")


def exit_app():
    root.destroy()


root = tk.Tk()
root.title("ATM Machine")
root.geometry("400x400")
root.configure(bg="#2c3e50")

pin_frame = tk.Frame(root, bg="#2c3e50")
tk.Label(pin_frame, text="Enter PIN:", font=("Helvetica", 14), fg="white", bg="#2c3e50").pack(pady=10)
pin_entry = tk.Entry(pin_frame, show="*",font=("Helvetica", 14))
pin_entry.pack(pady=5)
tk.Button(pin_frame, text="Submit", command=check_pin, width=15, bg="#1abc9c", relief="flat", highlightthickness=0).pack(pady=10)
pin_frame.pack(pady=50)

menu_frame = tk.Frame(root, bg="#2c3e50")
tk.Label(menu_frame, text="ATM Menu", font=("Helvetica", 16, "bold"), fg="white", bg="#2c3e50").pack(pady=10)
tk.Button(menu_frame, text="Check Balance", command=gui_check_balance, width=20, bg="#1abc9c", relief="flat",highlightthickness=0).pack(pady=5)
tk.Button(menu_frame, text="Deposit Money", command=gui_deposit_money, width=20, bg="#1abc9c", relief="flat",highlightthickness=0).pack(pady=5)
tk.Button(menu_frame, text="Withdraw Money", command=gui_withdrawal_money, width=20, bg="#1abc9c", relief="flat",highlightthickness=0).pack(pady=5)
tk.Button(menu_frame, text="Exit", command=exit_app, width=20, bg="#1abc9c", relief="flat",highlightthickness=0).pack(pady=5)

amount_entry = tk.Entry(menu_frame, font=("Helvetica", 14))
amount_entry.pack(pady=10)

message_label = tk.Label(menu_frame, text="", font=("Helvetica", 12), fg="white", bg="#2c3e50")
message_label.pack(pady=10)

root.mainloop()