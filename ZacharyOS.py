import webbrowser
import datetime
import os
import shutil
import socket

def greet():
    """Greets the user with a message."""
    name = input("Enter name: ")
    print(f"Hello, {name}!")

def add():
    """Adds two numbers."""
    while True:
        try:
            num1 = int(input("Enter first number: "))
            num2 = int(input("Enter second number: "))
            result = num1 + num2
            print(f"{num1} + {num2} = {result}")
            break  # Exit the loop if input is valid
        except ValueError:
            print("Invalid input. Please enter integers only.")

def time():
    """Displays the current time."""
    now = datetime.datetime.now()
    print(now.strftime("%H:%M:%S"))

def date():
    """Displays the current date."""
    today = datetime.date.today()
    print(today.strftime("%Y-%m-%d"))

def multiply():
    """Multiplies two numbers."""
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))
    result = num1 * num2
    print(f"{num1} * {num2} = {result}")

def open_store():
    """Opens the Microsoft Store."""
    webbrowser.open_new_tab("ms-windows-store:")

def open_tab():
    """Opens a new browser tab."""
    url = input("Enter URL: ")
    webbrowser.open_new_tab(url)

def open_file_explorer():
    """Opens the File Explorer."""
    os.startfile("explorer.exe")  # For Windows

def help_command():
    """Displays a list of available commands."""
    print("Available commands:")
    print("  greet  - Greets the user by name")
    print("  add  - Adds two numbers")
    print("  time  - Displays the current time")
    print("  date  - Displays the current date")
    print("  multiply  - Multiplies two numbers")
    print("  store  - Opens the Microsoft Store")
    print("  tab  - Opens a new browser tab")
    print("  explorer  - Opens the File Explorer")
    print("  youtube  - Opens YouTube")
    print("  storage  - Shows available storage")
    print("  ip  - Displays your IP address")
    print("  images  - Opens Google Images")
    print("  music  - Opens Chrome Music Lab")
    print("  help  - Displays this help message")
    print("  exit  - Exits the program")

def open_youtube():
    """Opens YouTube in a new browser tab."""
    webbrowser.open_new_tab("https://www.youtube.com")

def check_storage():
    """Displays available storage information."""
    total, used, free = shutil.disk_usage("/")
    print(f"Total storage: {total // (2**30)} GB")  # Convert to GB
    print(f"Used storage: {used // (2**30)} GB")
    print(f"Free storage: {free // (2**30)} GB")

def get_ip():
    """Displays the user's public IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        print(f"Your IP address is: {ip}")
        s.close()
    except Exception as e:
        print(f"Error getting IP address: {e}")

def open_google_images():
    """Opens Google Images in a new browser tab."""
    webbrowser.open_new_tab("https://images.google.com/")

def open_music_lab():
    """Opens Chrome Music Lab in a new browser tab."""
    webbrowser.open_new_tab("https://musiclab.chromeexperiments.com/")

def main():
    """Parses command-line arguments and executes the corresponding function."""
    print("Welcome to ZacharyOS")
    while True:
        try:
            command = input("> ")
            if command.strip() == "exit":
                break

            if command.strip() == "greet":
                greet()
            elif command.strip() == "add":
                add()
            elif command.strip() == "time":
                time()
            elif command.strip() == "date":
                date()
            elif command.strip() == "multiply":
                multiply()
            elif command.strip() == "store":
                open_store()
            elif command.strip() == "tab":
                open_tab()
            elif command.strip() == "explorer":
                open_file_explorer()
            elif command.strip() == "youtube":
                open_youtube()
            elif command.strip() == "storage":
                check_storage()
            elif command.strip() == "ip":
                get_ip()
            elif command.strip() == "images":
                open_google_images()
            elif command.strip() == "music":
                open_music_lab()
            elif command.strip() == "help":
                help_command()
            else:
                print("Invalid command.")

        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
