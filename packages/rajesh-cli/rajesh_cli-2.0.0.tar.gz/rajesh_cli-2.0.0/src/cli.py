import cmd
import requests


class CustomCLI(cmd.Cmd):
    intro = "Welcome to the Custom CLI!\nType 'ri login' to enter the RI environment.\n"
    prompt = ">> "
    environment = ""

    def precmd(self, line):
        if self.environment == "RI":
            return line
        else:
            print("Invalid command. Enter 'show usages' to list available options.")
            return ""

    def do_ri(self, args):
        """Enter the RI environment"""
        if not self.environment == "RI":
            if args.strip() == "login":
                username = input("Username: ")
                password = input("Password: ")
                if self.authenticate(username, password):
                    self.environment = "RI"
                    print("Successfully logged in. RI environment activated.")
                    self.prompt = "RI > "
                else:
                    print("Invalid credentials.")
            else:
                print("Invalid command. Usage: ri login")

    def do_add(self, args):
        """Add two numbers"""
        if self.environment != "RI":
            print("Please log in to the RI environment first.")
        else:
            numbers = args.split(",")
            if len(numbers) != 2:
                print("Invalid number of arguments. Usage: add <num1>, <num2>")
            else:
                try:
                    num1 = int(numbers[0].strip())
                    num2 = int(numbers[1].strip())
                    result = num1 + num2
                    print(f"Result: {result}")
                except ValueError:
                    print("Invalid numbers provided.")

    def do_get_feeds(self, args):
        """Get your feeds"""
        if self.environment != "RI":
            print("Please log in to the RI environment first.")
        else:
            api_url = "https://api.example.com/feeds"  # Replace with your API endpoint
            headers = {
                "Authorization": "Bearer your-access-token"  # Replace with your access token or authentication header
            }
            try:
                response = requests.get(api_url, headers=headers)
                if response.status_code == 200:
                    feeds = response.json()
                    print("Feeds:")
                    for feed in feeds:
                        print(feed)
                else:
                    print("Error retrieving feeds.")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

    def do_usage(self, args):
        """Display available commands"""
        if self.environment != "RI":
            print("Please log in to the RI environment first.")
        else:
            print("Available commands:")
            print("- add <num1>, <num2>: Add two numbers.")
            print("- get_feeds: Retrieve your feeds.")
            print("- usage: Display available commands.")
            print("- exit: Exit the CLI.")

    def do_exit(self, args):
        """Exit the CLI"""
        print("Exiting the Custom CLI.")
        return True

    def authenticate(self, username, password):
        # Perform authentication logic here
        # You can implement your own authentication mechanism or connect to an authentication system
        # For simplicity, this example uses a hardcoded username and password
        if username == "user" and password == "pass":
            return True
        else:
            return False


def activate_cli():
    CustomCLI().cmdloop()
