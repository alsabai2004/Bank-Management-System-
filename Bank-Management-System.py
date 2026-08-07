import os
import json

# المتغيرات العامة
account_type = ""
account_id = ""
logged_in = False
accounts_data = []
service_log = []
service_earn = 0

# كلاس الحساب
class Account:
    def __init__(self, name, id, password, phone, balance, type):
        self.name = name
        self.id = id
        self.password = password
        self.phone = phone
        self.balance = balance
        self.type = type

# حفظ الحسابات في ملف JSON
def save_accounts_to_file():
    with open("accounts.txt", "w", encoding="utf-8") as f:
        data = []
        for acc in accounts_data:
            data.append({
                "name": acc.name,
                "id": acc.id,
                "password": acc.password,
                "phone": acc.phone,
                "balance": acc.balance,
                "type": acc.type
            })
        json.dump(data, f, ensure_ascii=False, indent=2)

# تحميل الحسابات من ملف JSON
def load_accounts_from_file():
    global accounts_data
    if os.path.exists("accounts.txt"):
        with open("accounts.txt", "r", encoding="utf-8") as f:
            data = json.load(f)
            accounts_data = []
            for acc in data:
                accounts_data.append(Account(
                    acc["name"], acc["id"], acc["password"],
                    acc["phone"], acc["balance"], acc["type"]
                ))

# دالة تنظيف الشاشة
def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# تسجيل الدخول
def login():
    global logged_in, account_type, account_id
    print("=== log in ===")
    account_id_input = input("enter the ID: ")
    password_input = input("enter the password: ")

    print("\nchoice account type:")
    print("1. Manager")
    print("2. Branch")
    print("3. Normal")
    account_type_input = input("choice account type (1/2/3): ")

    for account in accounts_data:
        if account.id == account_id_input and account.password == password_input:
            if account_type_input == "1" and account.type == "manager":
                account_type = "manager"
                account_id = account.id
                logged_in = True
                print(f" {account.name}, Hello, you are logged in as a manager !")
                return
            elif account_type_input == "2" and account.type == "branch":
                account_type = "branch"
                account_id = account.id
                logged_in = True
                print(f" {account.name}, Hello, you are logged in as a branch !")
                return
            elif account_type_input == "3" and account.type == "normal":
                account_type = "normal"
                account_id = account.id
                logged_in = True
                print(f" {account.name}, Hello, you are logged in as a normal !")
                return
    print("ID or password or account type is wrong.")

# تسجيل الخروج
def logout():
    global logged_in, account_type, account_id
    logged_in = False
    account_type = ""
    account_id = ""
    print("Signed out.")

# التحقق من وجود ID
def check_id(id):
    for account in accounts_data:
        if account.id == id:
            return True
    return False

# تغيير كلمة السر
def change_password():
    old_password = input("enter the old password: ")
    if old_password != get_password(account_id):
        print("the old password is wrong.")
        return
    new_password = input("enter the new password: ")
    confirm_password = input("Confirm the new password : ")
    if new_password == confirm_password:
        update_password(account_id, new_password)
        print("Password changed successfully.")
    else:
        print("the new password is wrong.")

def get_password(id):
    for account in accounts_data:
        if account.id == id:
            return account.password
    return ""

def update_password(id, new_password):
    for account in accounts_data:
        if account.id == id:
            account.password = new_password
            break
    save_accounts_to_file()

def deposit():
    global service_earn
    amount = float(input("Enter the amount to deposit: "))
    if amount > 0:
        for account in accounts_data:
            if account.id == account_id:
                account.balance += amount
                service_earn += 100
                save_accounts_to_file()
                print(f"Successfully deposited. Your current balance: {account.balance}")
                return
    print(" amount is Invalid.")

def withdraw():
    global service_earn
    amount = float(input("Enter the amount to withdraw: "))
    if amount > 0:
        for account in accounts_data:
            if account.id == account_id and account.balance >= amount:
                account.balance -= amount
                service_earn += 100
                save_accounts_to_file()
                print(f"Successfully withdrawn. Your current balance: {account.balance}")
                return
    print("balance is insufficient or amount is invalid .")

def create_branch_account():
    name = input("Branch name: ")
    id = input("account number (ID): ")
    if check_id(id):
        print("The ID already exists..")
        return
    password = input("password: ")
    phone = input("phone number: ")
    balance = float(input("Initial branch balance: "))
    new_account = Account(name, id, password, phone, balance, "branch")
    accounts_data.append(new_account)
    save_accounts_to_file()
    print(f"The account has been created. {name} is new branch.")

def create_normal_account():
    name = input("Normal name: ")
    id = input("account number (ID): ")
    if check_id(id):
        print("The ID already exists..")
        return
    password = input("password: ")
    phone = input("phone number: ")
    balance = float(input("Initial normal balance: "))
    new_account = Account(name, id, password, phone, balance, "normal")
    accounts_data.append(new_account)
    save_accounts_to_file()
    print(f"The account has been created. {name} is new normal.")

def read_accounts():
    print("=== All accounts ===")
    for account in accounts_data:
        print(f"{account.name} (ID: {account.id}, account type: {account.type}, the balance: {account.balance})")
    input(" Click enter to continue ...")

def edit_account():
    print("=== Edit account ===")
    edit_id = input("Enter the ID to be edit: ")
    for account in accounts_data:
        if account.id == edit_id and account.type in ["branch", "normal"]:
            print(f"The account has been found : {account.name} (type: {account.type})")
            new_name = input(f"current new name (: {account.name}): ") or account.name
            new_password = input(f"current new password (: {account.password}): ") or account.password
            new_phone = input(f"current new phone number (: {account.phone}): ") or account.phone
            try:
                new_balance = input(f"current new balance (: {account.balance}): ")
                new_balance = float(new_balance) if new_balance.strip() else account.balance
            except ValueError:
                print("balance is invalid  not edited.")
                return

            account.name = new_name
            account.password = new_password
            account.phone = new_phone
            account.balance = new_balance

            save_accounts_to_file()
            print("✅ account edited successfully.")
            return
    print("❌ account is not found or cannot edited.")

def delete_account():
    print("=== delete account ===")
    del_id = input("Enter the account number to be delete: ")
    for account in accounts_data:
        if account.id == del_id and account.type in ["branch", "normal"]:
            accounts_data.remove(account)
            save_accounts_to_file()
            print("✅ account deleted successfully.")
            return
    print("❌ account is not found or cannot deleted.")

# واجهة المدير
def manager_home():
    while True:
        clear_console()
        print("=== Bank manager ===")
        print("1. change password")
        print("2. read Profits")
        print("3. Statistics")
        print("4. view accounts")
        print("5. create a branch account")
        print("6. create a normal account")
        print("7. edit branch or normal account")
        print("8. delete branch or normal account")
        print("9. log out")
        print("0. back to login")

        choice = input("choose a choice number: ")

        if choice == "1":
            change_password()
        elif choice == "2":
            print(f"Total profits: {service_earn} riyal")
            input(" Click enter to continue ...")
        elif choice == "3":
            print(f"Number of accounts: {len(accounts_data)}")
            input(" Click enter to continue ...")
        elif choice == "4":
            read_accounts()
        elif choice == "5":
            create_branch_account()
            input(" Click enter to continue ...")
        elif choice == "6":
            create_normal_account()
            input("Click enter to continue  ...")
        elif choice == "7":
            edit_account()
            input(" Click enter to continue ...")
        elif choice == "8":
            delete_account()
            input(" Click enter to continue ...")
        elif choice == "9" or choice == "0":
            logout()
            break
        else:
            print("wrong choice .")
            input(" Click enter to continue ...")

# واجهة الفرع
def branch_home():
    while True:
        clear_console()
        print("=== Branch ===")
        print("1. change password")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. log out")
        print("0. back to login")

        choice = input("choose a choice: ")

        if choice == "1":
            change_password()
        elif choice == "2":
            deposit()
            input(" Click enter to continue ...")
        elif choice == "3":
            withdraw()
            input(" Click enter to continue ...")
        elif choice == "4" or choice == "0":
            logout()
            break
        else:
            print("wrong choice .")
            input(" Click enter to continue ...")

# واجهة العميل
def normal_home():
    while True:
        clear_console()
        print("=== Normal ===")
        print("1. change password")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. log out")
        print("0. back to login")

        choice = input("choose a choice: ")

        if choice == "1":
            change_password()
        elif choice == "2":
            deposit()
            input(" Click enter to continue ...")
        elif choice == "3":
            withdraw()
            input(" Click enter to continue ...")
        elif choice == "4" or choice == "0":
            logout()
            break
        else:
            print("wrong choice .")
            input(" Click enter to continue ...")

# الشاشة الرئيسية
def home():
    global logged_in, account_id, account_type
    while True:
        while not logged_in:
            login()
        if account_type == "manager":
            manager_home()
        elif account_type == "branch":
            branch_home()
        elif account_type == "normal":
            normal_home()

# تشغيل البرنامج
load_accounts_from_file()
if not any(acc.type == "manager" for acc in accounts_data):
    accounts_data.append(Account("Admin", "admin", "1234", "0000", 1000, "manager"))
    save_accounts_to_file()

home()
    
