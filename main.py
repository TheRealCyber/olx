from getpass import getpass
import time

import re
from getpass import getpass

class Register:
    def __init__(self, *args):
        self.data = {}
        self.get_user_input(args)

    def get_user_input(self, variables):
        for variable in variables:
            if variable.lower() == "acc_type":
                while True:
                    acc_type = input(f"Enter {variable} (buyer/seller): ").lower()
                    if acc_type in ["buyer", "seller"]:
                        self.data[variable] = acc_type
                        break
                    else:
                        print("Invalid input. Please enter 'buyer' or 'seller'.")
            elif variable.lower() == "password":
                self.data[variable] = getpass(f"Enter {variable}: ")
            elif variable.lower() == "ph_no":
                while True:
                    ph_no = input(f"Enter {variable}: ")
                    if ph_no.isdigit() and len(ph_no) == 10:
                        self.data[variable] = ph_no
                        break
                    else:
                        print("Invalid phone number. Please enter 10 digits.")
            elif variable.lower() == "email":
                while True:
                    email = input(f"Enter {variable}: ")
                    if re.match(r"[^@]+@[^@]+\.[^@]+", email) and email.endswith('.com'):
                        self.data[variable] = email
                        break
                    else:
                        print("Invalid email format. Please enter a valid email.")
            elif variable.lower() == "username":
                while True:
                    username = input(f"Enter {variable}: ")
                    if username.isalpha():
                        self.data[variable] = username
                        break
                    else:
                        print("Invalid username. Please enter only alphabetic characters.")
            elif variable.lower() == "address":
                while True:
                    address = input(f"Enter {variable}: ")
                    if len(address) <= 50:
                        self.data[variable] = address
                        break
                    else:
                        print("Address exceeds 50 characters. Please enter a shorter address.")
            else:
                self.data[variable] = input(f"Enter {variable}: ")



class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_authentication(self, register_instance):
        if (
                self.username == register_instance.data.get("username")
                and self.password == register_instance.data.get("password")
        ):
            return True
        else:
            return False


class Mainmenu:
    def __init__(self, acc_type):
        self.acc_type = acc_type

    def menu(self):
        if self.acc_type == 'buyer':
            Buyer_Interface().menu()
        elif self.acc_type == 'seller':
            Seller_Interface().menu()


class Buyer_Interface:
    def __init__(self):
        self.exit = 1
        self.cart = set()
        self.item_list = {"0": "Couch", "1": "Table", "2": "TV", "3": "Xbox", "4": "Bed"}

    def menu(self):
        while self.exit == 1:
            menu_input = input('\nBuyer Interface navigator\n0 - View all items\n1 - Add item to cart\n2 - View cart\n3 - Purchase item\n')
            match menu_input:
                case '0':
                    self.print_items()
                case '1':
                    self.add_to_cart()
                case '2':
                    self.view_cart()
                case '3':
                    self.purchase_items()
                case '4':
                    self.chat()

    def print_items(self):
        print("\nList of all items:\n")
        for x in self.item_list.keys():
            print(x + " > " + self.item_list[x])

    def add_to_cart(self):
        self.print_items()
        item_index = input("\nEnter the index of the item to add to cart: ")
        if item_index in self.item_list:
            self.cart.add(item_index)
            print(f"\n{self.item_list[item_index]} added to your cart.")
        else:
            print("Invalid item index.")

    def view_cart(self):
        if not self.cart:
            print("\nCart is empty")
        else:
            print("\nItems in your cart:")
            for item_index in self.cart:
                print(self.item_list[item_index])

    def purchase_items(self):
        menu_input = input("\nWould you like to purchase one item from global market\nOr purchase the entire cart\n0 - Purchase one item\n1 - Purchase entire cart\n")
        match menu_input:
            case '0':
                self.print_items()
                item_index = input("\nEnter the index of the item to purchase directly: ")
                if item_index in self.item_list:
                    print(f"{self.item_list[item_index]} successfully purchased! Thank you!")
                else:
                    print("Invalid item index.")
            case '1':
                if not self.cart:
                    print("\nCart is empty. Add items before purchasing.")
                    return
                print("\nItems in your cart:")
                for item_index in self.cart:
                    print(self.item_list[item_index])
                print("\nPurchase successful. Thank you for shopping!")
                self.cart.clear()
            case _:
                print("Invalid menu item")

    def chat(self):
        self.print_items()
        item_index = input("Which product do you wish to start a chat regarding?: ")
        print(f"Starting chat with product owner of {self.item_list[item_index]}\nType EXIT to exit from the chat and return to menu\n")


class Seller_Interface:
    def __init__(self):
        self.exit = 1
        self.listing = {}
        self.key = 0
        self.auction = {}

    def menu(self):
        while self.exit == 1:
            menu_input = input("Seller interface navigator\n0 - Check listing\n1 - List item\n2 - Start auction\n3 - Chat\n4 - Update listing \n5 - Quit application \n")
            match menu_input:
                case '0':
                    if len(self.listing) > 0:
                        n = len(self.listing)
                        print("Items listed are as follows:\n")
                        for i in range(n):
                            print(f"{i} - {self.listing[i]}\n")
                    else:
                        print("\nList is empty\n")
                case '1':
                    items = input("Enter the Name Category and Price of product separated by space: ").split()
                    self.listing[self.key] = items
                    self.key = self.key + 1
                case '2':
                    print("Starting an auction...\n")
                    key = 0
                    duration = float(input("Enter the duration of the auction: \n"))
                    start_time = time.time()
                    while time.time() - start_time < duration:
                        bid = input("Enter the amount name of bidder and their location separated by space: \n").split()
                        self.auction[key] = bid
                        key = key + 1
                        if key >= 1:
                            sorted_keys = sorted(self.auction, key=lambda k: -float(self.auction[k][0]))
                            for i, k in enumerate(sorted_keys):
                                v = self.auction[k]
                                print(f"{i}: Bid Amount - {v[0]}, Bidder - {v[1]}, Location - {v[2]}")
                case '3':
                    print("Chatting...")
                case '4':
                    print("Updating a listing...")
                case '5':
                    self.exit = 0
                case _:
                    print("Invalid input. Please choose a valid option.")


if __name__ == "__main__":
    exit = 1
    while exit == 1:
        menu_input = input('Enter the option you wish to execute\n0 - Register new user\n1 - Log in for an existing user\n2 - Exit\n3 - Admin testing\n')
        match menu_input:
            case '0':
                registration = Register("username", "password", "email", "ph_no", "address", "acc_type")
                obfuscated_data = registration.data.copy()
                obfuscated_data["password"] = "*" * len(registration.data["password"])
                print("Registered Data:", obfuscated_data)
            case '1':
                login_attempt = Login(
                    input("Login Username: "), input("Login Password: ")
                )
                if login_attempt.check_authentication(registration):
                    print("Valid authentication")
                    menu = Mainmenu(registration.data['acc_type'])
                    menu.menu()
                    exit = 0
                else:
                    print("Invalid authentication")
            case '2':
                exit = 0
                print("The program is exiting now")
            case '3':
                print("Admin testing functionality\nEnter acc type\n")
                acc_type = input()
                menu = Mainmenu(acc_type)
                menu.menu()
                exit = 0
            case _:
                print("Invalid menu item")
