import json
import os
from cryptography.fernet import Fernet
from getpass import getpass

# File for storing encrypted passwords
PASSWORDS_FILE = 'passwords.json'
# File for storing encryption key
KEY_FILE = 'secret.key'

# Generate and store the key if it doesn't exist
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    return key

# Initialize encryption
key = load_key()
cipher = Fernet(key)

# Load passwords from the file
def load_passwords():
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, 'r') as file:
            encrypted_data = json.load(file)
        # Decrypt passwords
        return {k: cipher.decrypt(v.encode()).decode() for k, v in encrypted_data.items()}
    return {}

# Save encrypted passwords to the file
def save_passwords(passwords):
    encrypted_data = {k: cipher.encrypt(v.encode()).decode() for k, v in passwords.items()}
    with open(PASSWORDS_FILE, 'w') as file:
        json.dump(encrypted_data, file, indent=4)

# Add a new password
def add_password(passwords, account):
    password = getpass(f"Enter the password for '{account}': ")
    passwords[account] = password
    save_passwords(passwords)
    print(f"Password for '{account}' added.")

# View a password
def view_password(passwords, account):
    if account in passwords:
        print(f"Password for '{account}': {passwords[account]}")
    else:
        print(f"No password found for '{account}'.")

# Delete a password
def delete_password(passwords, account):
    if account in passwords:
        del passwords[account]
        save_passwords(passwords)
        print(f"Password for '{account}' deleted.")
    else:
        print(f"No password found for '{account}'.")

# Command line interface
def main():
    passwords = load_passwords()

    while True:
        print("\n--- Password Manager ---")
        print("1. Add a new password")
        print("2. View a password")
        print("3. Delete a password")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ")

        if choice == '1':
            account = input("Enter the account name (e.g., 'email', 'bank'): ")
            add_password(passwords, account)

        elif choice == '2':
            account = input("Enter the account name to view its password: ")
            view_password(passwords, account)

        elif choice == '3':
            account = input("Enter the account name to delete its password: ")
            delete_password(passwords, account)

        elif choice == '4':
            print("Goodbye! Stay secure.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
