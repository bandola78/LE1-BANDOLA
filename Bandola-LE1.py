import os
import time

game_inventory = {
    "Donkey Kong": {"stock": 3, "price": 2},
    "Super Mario Bros": {"stock": 5, "price": 3},
    "Tetris": {"stock": 2, "price": 1},
    "Pac-Man": {"stock": 4, "price": 2},
}

user_profiles = {}

admin_user = "admin"
admin_pass = "adminpass"

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_available_games():
    print("Available Games \n")
    for idx, (game, info) in enumerate(game_inventory.items(), start=1):
        print(f"{idx}. {game}:")
        print(f"\tStock - {info['stock']}")
        print(f"\tRental Price - ${info['price']}")
    print()

def show_user_inventory(username):
    clear_console()
    try:
        if not user_profiles[username]["library"]:
            print("Your inventory is empty.")
            return
        print("Your Inventory: \n")
        inventory = user_profiles[username]["library"]
        unique_games = set(inventory)
        for game in unique_games:
            print(game)
            print(f"Quantity: {inventory.count(game)} pc/s")
            print()
    except KeyError:
        print("An error occurred while displaying inventory. Please try again.")
    input("Please press enter to return to the Main Menu...")

def sign_up():
    clear_console()
    print("Sign up \n")
    username = input("Please enter your username: ").strip().capitalize()
    if username in user_profiles:
        print("\nUsername already exists. Please choose another username.")
        input("Press Enter to continue to Login...")
        return
    password = input("Enter a password: ")
    for existing_user, details in user_profiles.items():
        if details["password"] == password:
            print("\nA user with this password is already registered. Please log in.")
            input("Press Enter to continue to the main menu...")
            return
    try:
        balance = float(input("Enter initial balance (minimum $5): $"))
        if balance < 5:
            print("\nInitial balance must be at least $5.")
            input("Press Enter to continue to the main menu...")
            return
        user_profiles[username] = {"password": password, "balance": balance, "points": 0.0, "library": []}
        print("\nUser registration successful.")
    except ValueError:
        print("\nInvalid balance amount. Please enter a valid number.")
    input("Press Enter to continue to the main menu...")

def validate_credentials(username, password):
    return username in user_profiles and user_profiles[username]["password"] == password

def  main_menu():
    while True:
        clear_console()
        print("Welcome to Good Gaming Rentals! \n")
        print("1. Login")
        print("2. Register")
        print("3. Admin Login")
        print("4. Quit")
        choice = input("Select an option: ")

        if choice == "1":
            user_login()
        elif choice == "2":
            sign_up()
        elif choice == "3":
            admin_login()
        elif choice == "4":
            print("Thank you for visiting the Good Gaming Rentals. Goodbye!")
            time.sleep(1)
            exit()
        else:
            print("Invalid option. Please try again.")

def user_login():
    while True:
        clear_console()
        print("Login \n")
        username = input("Enter your username (leave blank to return to main menu): ").strip().capitalize()
        if not username:
            main_menu()
            return

        password = input("Enter your password: ")
        if not password:
            main_menu()
            return

        if validate_credentials(username, password):
            print("Login successful.")
            user_dashboard(username)
            break
        else:
            print("\nInvalid username or password. Please try again or sign up if you don't have an account.")
            choice = input("Do you want to sign up? (yes/no): ").strip().lower()
            if choice == "yes":
                sign_up()
                break
            else:
                input("Press Enter to continue...")

def user_dashboard(username):
    while True:
        clear_console()
        print(f"Welcome to Good Gaming Rentals, {username}! \n")
        print("Main Menu \n")
        print("1. Display Available Games")
        print("2. Rent a game")
        print("3. Return a game")
        print("4. Top up account")
        print("5. Check inventory")
        print("6. Check balance and points")
        print("7. Redeem free game rental")
        print("8. Logout")
        option = input("Select an option: ")
        if option == "1":
            show_available_games()
            input("Please press ENTER to return to the Main Menu...")
        elif option == "2":
            rent_game(username)
        elif option == "3":
            return_game(username)
        elif option == "4":
            add_funds(username)
        elif option == "5":
            show_user_inventory(username)
        elif option == "6":
            show_balance_and_points(username)
        elif option == "7":
            redeem_free_rental(username)
        elif option == "8":
            print("Logging out...")
            time.sleep(1)
            exit()
        else:
            print("Invalid option. Please try again.")

def rent_game(username):
    while True:
        clear_console()
        show_available_games()
        print("Rent a Game \n")
        try:
            game_index_input = input("Enter the number of the game you want to rent (leave blank if you want to cancel): ").strip()
            if game_index_input == "":  # Check if the input is empty
                print("Operation canceled.")
                input("Press Enter to continue...")
                return
            game_index = int(game_index_input)
            games = list(game_inventory.keys())
            if game_index < 1 or game_index > len(games):
                print("Invalid game number. Please try again.")
                input("Press Enter to continue...")
                return
            
            selected_game = games[game_index - 1]

            if game_inventory[selected_game]["stock"] == 0:
                print("Sorry, the selected game is currently out of stock.")
                input("Press Enter to continue...")
                return

            quantity = int(input(f"How many copies of '{selected_game}' do you want to rent? "))
            if quantity < 1:
                print("Invalid quantity. Please enter a positive number.")
                input("Press Enter to continue...")
                return

            rental_cost = game_inventory[selected_game]["price"] * quantity

            user_balance = user_profiles[username]["balance"]
            if user_balance < rental_cost:
                print("Insufficient balance. Please top up your account.")
                input("Press Enter to continue...")
                return

            if game_inventory[selected_game]["stock"] < quantity:
                print("Insufficient stock for the requested quantity.")
                input("Press Enter to continue...")
                return

            user_profiles[username]["balance"] -= rental_cost
            points_earned = rental_cost / 2  # Calculate points earned
            user_profiles[username]["points"] += points_earned

            for _ in range(quantity):
                user_profiles[username]["library"].append(selected_game)
                game_inventory[selected_game]["stock"] -= 1

            print("\nRental Details:")
            print(f"\tGame: '{selected_game}'")
            print(f"\tQuantity: {quantity} pc/s")
            print(f"\tRental Cost: ${rental_cost} deducted from your balance.")
            print(f"\tPoints Earned: {points_earned}")
            print(f"\nHello, {username}!")
            print(f"You rented '{selected_game}', {quantity} pc/s.")
            print(f"Take care of the rented games, {username}!")

            input("\nPlease press enter to continue...")

            # Ask if the user wants to rent more games
            choice = input("Do you want to rent more games? (yes/no): ").strip().lower()
            if choice != 'yes':
                break

        except ValueError:
            print("Invalid input. Please enter a valid number.")
            input("Press Enter to continue...")
        except IndexError:
            print("Invalid input. Please enter a valid game number.")
            input("Press Enter to continue...")
        except KeyError:
            print("An error occurred. Please try again.")
            input("Press Enter to continue...")

    print("Returning to the Main Menu...")
    input("Press Enter to continue...")


def return_game(username):
    clear_console()
    try:
        if not user_profiles[username]["library"]:
            print("Your inventory is empty.")
            input("Press Enter to continue...")
            return

        print("Your Inventory: \n")
        inventory = user_profiles[username]["library"]
        unique_games = set(inventory)
        for idx, game in enumerate(unique_games, start=1):
            print(f"{idx}. {game}: {inventory.count(game)} pc/s")

        game_index = int(input("Enter the number of the game you want to return: "))
        if game_index < 1 or game_index > len(unique_games):
            print("Invalid game number. Please try again.")
            input("Press Enter to continue...")
            return

        selected_game = list(unique_games)[game_index - 1]

        num_copies = int(input("How many copies of this game do you want to return? "))
        if num_copies < 1:
            print("Invalid number of copies. Please enter a positive number.")
            input("Press Enter to continue...")
            return

        if inventory.count(selected_game) < num_copies:
            print("You do not have enough copies of this game in your inventory.")
            input("Press Enter to continue...")
            return

        rental_cost_per_copy = game_inventory[selected_game]["price"]
        total_rental_cost = rental_cost_per_copy * num_copies

        for _ in range(num_copies):
            inventory.remove(selected_game)
            game_inventory[selected_game]["stock"] += 1

        points_earned = total_rental_cost / 2
        user_profiles[username]["points"] += points_earned

        print(f"{num_copies} copy/copies of '{selected_game}' returned successfully.")
        print(f"You earned {points_earned} point/s.")
        print(f"Total rental cost refunded: ${total_rental_cost}")
        print(f"Your current balance: ${user_profiles[username]['balance']}")

        input("\nPlease press enter to return to the Main Menu...")
    except (ValueError, KeyError, IndexError):
        print("An error occurred while processing the return. Please try again.")
        input("Press Enter to continue...")

def add_funds(username):
    clear_console()
    print ("Top Up Account \n")
    try:
        amount = float(input("Enter amount to top up (minimum $0): $"))
        if amount < 0:
            print("Invalid amount. Please enter a non-negative value.")
            input("Press Enter to continue...")
            return
        user_profiles[username]["balance"] += amount
        print(f"Account balance topped up successfully. New balance: ${user_profiles[username]['balance']}")
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
    input("Press Enter to return to the Main Menu...")

def show_balance_and_points(username):
    clear_console()
    print("Balance and Points \n")
    try:
        print(f"Your current balance: ${user_profiles[username]['balance']}")
        print(f"Your current points: {user_profiles[username]['points']}")
    except KeyError:
        print("An error occurred while fetching balance and points. Please try again later.")
    input("\nPress Enter to go back to the main menu...")

def redeem_free_rental(username):
    clear_console()
    print("Redeem Free Game Rental \n")
    try:
        points = user_profiles[username]["points"]
        if points >= 3:
            print("Congratulations! You have enough points to redeem a free game rental.")
            choice = input("Would you like to redeem a free game rental? (yes/no): ").lower()
            if choice == "yes":
                game_choices = list(game_inventory.keys())
                print("Available games for free rental:")
                for idx, game in enumerate(game_choices, start=1):
                    print(f"{idx}. {game}")
                game_index = int(input("Enter the number of the game you want to rent for free: "))
                if game_index < 1 or game_index > len(game_choices):
                    print("Invalid game number. Please try again.")
                    input("Press Enter to continue...")
                    return

                selected_game = game_choices[game_index - 1]
                user_profiles[username]["library"].append(selected_game)
                user_profiles[username]["points"] -= 3
                print(f"Congratulations! You have rented '{selected_game}' for free.")
                input("\nPlease press enter to return to the Main Menu...")
        else:
            print("You do not have enough points to redeem a free game rental.")
            input("\nPlease press enter to return to the Main Menu...")
    except ValueError:
        print("Invalid input. Please try again.")
        input("Press Enter to continue...")
    except KeyError:
        print("An error occurred. Please try again.")
        input("Press Enter to continue...")

def admin_login():
    clear_console()
    print("Admin Login \n")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    if username == admin_user and password == admin_pass:
        admin_dashboard()
    else:
        print("Invalid admin credentials. Please try again.")
        time.sleep(1)

def admin_dashboard():
    while True:
        clear_console()
        print("Admin Menu \n")
        print("1. Update game details")
        print("2. View game library")
        print("3. Logout")
        option = input("Select an option: ")
        if option == "1":
            update_game_info()
        elif option == "2":
            view_game_inventory()
        elif option == "3":
            print("Logging out...")
            break
        else:
            print("Invalid option. Please try again.")

def update_game_info():
    clear_console()
    print("Update Game Details \n")
    try:
        show_available_games()
        game_index = int(input("Enter the number of the game you want to update: "))
        games = list(game_inventory.keys())
        if game_index < 1 or game_index > len(games):
            print("Invalid game number. Please try again.")
            input("Press Enter to continue...")
            return
        
        selected_game = games[game_index - 1]

        new_stock = int(input(f"Enter the new quantity for '{selected_game}': "))
        if new_stock < 0:
            print("Quantity cannot be negative. Please try again.")
            input("Press Enter to continue...")
            return
        
        new_price = float(input(f"Enter the new rental price for '{selected_game}': $"))
        if new_price < 0:
            print("Cost cannot be negative. Please try again.")
            input("Press Enter to continue...")
            return

        game_inventory[selected_game]["stock"] = new_stock
        game_inventory[selected_game]["price"] = new_price

        print("Game details updated successfully.")
    except (ValueError, IndexError):
        print("Invalid input or selection.")
        input("Press Enter to continue...")
    except KeyError:
        print("An error occurred. Please try again.")
        input("Press Enter to continue...")

def view_game_inventory():
    clear_console()
    print("Game Library \n")
    for game, info in game_inventory.items():
        print(f"{game}:")
        print(f"\tStock - {info['stock']}")
        print(f"\tRental Price - ${info['price']}")
        print()
    input("\nPress Enter to return to the Admin Menu...")

if __name__ == "__main__":
    main_menu()