import os
import ast
import random
import string

# Password Validator Class
class PasswordValidator:
    def __init__(self, password):
        self.password = password

    def is_valid(self):
        if len(self.password) < 8:
            return False
        if not any(char.isupper() for char in self.password):
            return False
        if not any(char.isdigit() for char in self.password):
            return False
        if not any(char in "!@#$%^&*()_+" for char in self.password):
            return False
        return True

# Password Generator
def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    while True:
        password = ''.join(random.choice(chars) for _ in range(10))
        if PasswordValidator(password).is_valid():
            return password

# Account Class
class Account:
    def __init__(self, name, username, password, category):
        self.name = name
        self.username = username
        self.password = password
        self.category = category

# Storage
DB_FILE = "password_manager_db.txt"

def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as file:
        try:
            content = file.read()
            return ast.literal_eval(content) if content else {}
        except Exception:
            return {}

def save_data(data):
    with open(DB_FILE, 'w') as file:
        file.write(str(data))

# Registration and Login
def register():
    data = load_data()
    username = input("Create username: ")
    if username in data:
        print("User already exists.")
        return None
    while True:
        password = input("Create password: ")
        if PasswordValidator(password).is_valid():
            break
        print("Password must have at least 1 uppercase letter, 1 number, 1 special character, and be at least 8 characters long.")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    data[username] = {"password": password, "first_name": first_name, "last_name": last_name, "accounts": []}
    save_data(data)
    print("Registration successful. Please log in.")
    return username

def login():
    data = load_data()
    attempts = 0
    while attempts < 3:
        username = input("Username: ")
        password = input("Password: ")
        if username in data and data[username]['password'] == password:
            print(f"Welcome {data[username]['first_name']}!")
            return username
        else:
            attempts += 1
            print(f"Incorrect login. Attempts remaining: {3 - attempts}")
    print("Too many failed attempts. Program shutting down.")
    exit()

# Main Menu
def main_menu(username):
    data = load_data()
    while True:
        print("\n1. Add Account\n2. View Accounts by Category\n3. Delete Account\n4. Modify Account\n5. Generate Password\n6. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Account name: ")
            acc_username = input("Account username: ")
            acc_password = input("Account password: ")
            category = input("Category: ")
            account = Account(name, acc_username, acc_password, category)
            data[username]['accounts'].append(account.__dict__)
            save_data(data)

        elif choice == "2":
            categories = set(acc['category'] for acc in data[username]['accounts'])
            print("Categories:", ', '.join(categories))
            cat = input("Enter category to view: ")
            for acc in data[username]['accounts']:
                if acc['category'] == cat:
                    print(f"\nThe account: {acc['name']}\nThe username: {acc['username']}\nThe password: {acc['password']}")

        elif choice == "3":
            name = input("Enter the name of the account to delete: ")
            data[username]['accounts'] = [acc for acc in data[username]['accounts'] if acc['name'] != name]
            save_data(data)

        elif choice == "4":
            name = input("Enter the name of the account to modify: ")
            for acc in data[username]['accounts']:
                if acc['name'] == name:
                    acc['username'] = input("New username: ")
                    acc['password'] = input("New password: ")
                    acc['category'] = input("New category: ")
                    break
            save_data(data)

        elif choice == "5":
            print("Generated password:", generate_password())

        elif choice == "6":
            print("Logging out...")
            break

        else:
            print("Invalid option.")

# Program Entry
def main():
    print("Welcome to the Password Manager")
    choice = input("Do you have an account? (yes/no): ").strip().lower()
    if choice == "no":
        username = register()
        if username:
            username = login()
    else:
        username = login()
    main_menu(username)

if __name__ == "__main__":
    main()
