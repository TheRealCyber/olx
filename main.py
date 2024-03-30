from getpass import getpass
import time
import datetime
import re
import sqlite3
from getpass import getpass
import hashlib

class Register:
    def __init__(self, *args):
        self.conn = sqlite3.connect('olx.db')
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
                    ph_no = input(f"Enter {variable} (10 digits): ")
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
                    username = input(f"Enter {variable} (alphanumeric): ")
                    if username.isalnum():
                        self.data[variable] = username
                        break
                    else:
                        print("Invalid username. Please enter alphanumeric characters only.")
            elif variable.lower() == "address":
                while True:
                    address = input(f"Enter {variable} (max 50 characters): ")
                    if len(address) <= 50:
                        self.data[variable] = address
                        break
                    else:
                        print("Address exceeds 50 characters. Please enter a shorter address.")
            else:
                self.data[variable] = input(f"Enter {variable}: ")
                
    def register_user(self):
        try:
            hashed_password = hashlib.sha256(self.data['password'].encode()).hexdigest()
            cursor = self.conn.cursor()
            username = self.data['username']
            email = self.data['email']
            phone_number = self.data['ph_no']
            user_type = self.data['acc_type']
            registration_date = datetime.datetime.now()
            cursor.execute("""
                INSERT INTO Users (username, password, email, phone_number, user_type, registration_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, hashed_password, email, phone_number, user_type, registration_date))
            self.conn.commit()
            print("Registration successful!")
        except sqlite3.Error as e:
            print("Registration failed:", e)
        finally:
            self.conn.close()

class Login:
    def __init__(self, username, password, conn=None):
        self.username = username
        self.password = password
        self.conn = conn

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_authentication(self):
        try:
            hashed_password = self.hash_password(self.password)
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE username = ?", (self.username,))
            user_data = cursor.fetchone()
            if user_data:
                stored_password_hash = user_data[2]
                if hashed_password == stored_password_hash:
                    return user_data[5], True
                else:
                    print("Invalid password.")
                    return None, False
            else:
                print("User not found.")
                return None, False
        except sqlite3.Error as e:
            print("Authentication failed:", e)
            return None, False

class Mainmenu:
    def __init__(self, acc_type):
        self.acc_type = acc_type

    def menu(self):
        print("User type:", self.acc_type)
        if self.acc_type == 'buyer':
            Buyer_Interface().menu()
        elif self.acc_type == 'seller':
            Seller_Interface().menu()
        else:
            print("Invalid account type:", self.acc_type)

    def clear_data(self):
        try:
            conn = sqlite3.connect('olx.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Users")
            conn.commit()
            print("Data cleared successfully.")
        except sqlite3.Error as e:
            print("Error clearing data:", e)
        finally:
            conn.close()

class Buyer_Interface:
    def __init__(self):
        self.exit = 1
        self.cart = set()
        self.item_list = {"0": "Couch", "1": "Table", "2": "TV", "3": "Xbox", "4": "Bed"}

    def goto_menu(self):
        menu = Mainmenu('buyer')
        menu.menu()

    def menu(self):
        while self.exit == 1:
            menu_input = input('\nBuyer Interface navigator\n0 - View all items\n1 - Add item to cart\n2 - View cart\n3 - Purchase item\n4 - Start chat for item\n5 - Logout & Exit\n')
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
                case '5':
                    print("Goodbye.")
                    break
                case _:
                    print("Invalid menu item")

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
        menu_input=input("\nWould you like to purchase one item from global market\nOr purchase the entire cart\n0 - Purchase one item\n1 - Purchase entire cart\n")
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
        print(f"Starting chat with product owner of {self.item_list[item_index]}\n")
        print("The listed price for this product is Rupees 250, you may attempt to negotiate by entering prices you deem fit")
        print("Enter 0 if you wish to return to menu and end the chat")
        target_price = 250
        user_bid = float(input("Enter your initial bid: "))
        print(int(user_bid))
        if (int(user_bid!='0')):
            for _ in range(3):
                target_price = (target_price-(target_price-user_bid)/3)
                print(f"I would offer: {target_price}")
                user_bid = float(input("Enter your new bid: "))
                if (int(user_bid)==int(target_price)):
                    break
            target_price = (target_price-(target_price-user_bid)/3)
            print(f"The final price I'll offer is {target_price}, if you're okay with the price then type yes, else type no")
            choice=input()
            if (choice.lower()=='yes'):
                choice=input(f"Are you sure you want to add {self.item_list[item_index]} to your cart?")
                if (choice.lower()=='yes'):
                    self.cart.add(item_index)
                    print(f"\n{self.item_list[item_index]} added to your cart.")
                else:
                    self.goto_menu()
            else:
                self.goto_menu()
        else:
            self.goto_menu()

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
                    self.chat()
                case '4':
                    print("Updating a listing...")
                case '5':
                    self.exit = 0
                case _:
                    print("Invalid input. Please choose a valid option.")

    def chat(self):
        if not self.listing:
            print("There are no items listed to start a chat.")
            return

        print("\nItems available for chat:")
        for index, item_info in self.listing.items():
            print(f"{index}: {item_info[0]} - Rs. {item_info[2]}")

        try:
            item_index = int(input("Select an item to start a chat: "))
            if item_index not in self.listing:
                print("Invalid item index.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid integer item index.")
            return

        print(f"Starting chat as seller for product: {self.listing[item_index][0]}")
        print(f"The listed price for this product is Rs. {self.listing[item_index][2]}.")

        buyer_offer = float(input("Enter the initial offer from the buyer: "))
        if buyer_offer <= 0:
            print("Invalid offer. Offer must be greater than 0.")
            return

        negotiation_round = 1
        seller_price = 0
        while negotiation_round <= 3:
            if negotiation_round > 1:
                print(f"\nNegotiation Round {negotiation_round}:")
                buyer_offer = float(input("Enter the new offer from the buyer: "))
                if buyer_offer <= 0:
                    print("Invalid offer. Offer must be greater than 0.")
                    return

            seller_price = float(input("Enter your counteroffer price: "))
            if seller_price <= buyer_offer:
                print("Invalid counteroffer. Counteroffer price must be greater than the buyer's offer.")
                return

            print(f"Your counteroffer price is Rs. {seller_price}.")

            choice = input("Do you want to continue negotiation? (yes/no): ")
            if choice.lower() == 'no':
                break

            negotiation_round += 1

        if negotiation_round > 3:
            print("\nMaximum negotiation rounds reached. Negotiation failed.")
            return

        choice = input("Do you want to accept this offer? (yes/no): ")
        if choice.lower() == 'yes':
            print(f"\nProduct '{self.listing[item_index][0]}' sold at negotiated price of Rs. {seller_price}.")
            del self.listing[item_index]
        else:
            print("Negotiation failed. Returning to menu...")

if __name__ == "__main__":
    exit_program = False

    while not exit_program:
        menu_input = input('Enter the option you wish to execute\n0 - Register new user\n1 - Log in for an existing user\n2 - Exit\n3 - Admin testing\n4 - Clear data from database\n')

        if menu_input == '0':
            registration = Register("username", "password", "email", "ph_no", "address", "acc_type")
            registration.register_user()
            obfuscated_data = registration.data.copy()
            obfuscated_data["password"] = "*" * len(registration.data["password"])
            print("Registered Data:", obfuscated_data)
        elif menu_input == '1':
            username = input("Login Username: ")
            password = input("Login Password: ")
            conn = sqlite3.connect('olx.db')
            login_attempt = Login(username, password, conn)
            user_type, authenticated = login_attempt.check_authentication()
            if authenticated:
                print("Valid authentication")
                if user_type == 'buyer':
                    print("User type is 'buyer'. Proceeding to buyer menu.")
                    buyer_menu = Buyer_Interface()
                    buyer_menu.menu()
                elif user_type == 'seller':
                    print("User type is 'seller'. Proceeding to seller menu.")
                    seller_menu = Seller_Interface()
                    seller_menu.menu()
                else:
                    print("Invalid account type:", user_type)
            else:
                print("Invalid authentication")
            conn.close()

        elif menu_input == '2':
            exit_program = True
            print("The program is exiting now")
        elif menu_input == '3':
            print("Admin testing functionality\nEnter acc type\n")
            acc_type = input()
            if acc_type == 'buyer' or acc_type == 'seller':
                if acc_type == 'buyer':
                    buyer_menu = Buyer_Interface()
                    buyer_menu.menu()
                elif acc_type == 'seller':
                    seller_menu = Seller_Interface()
                    seller_menu.menu()
            else:
                print("Invalid account type")
        elif menu_input == '4':
            menu = Mainmenu(None)
            menu.clear_data()
