import argparse


def login():
    useremail = input("Enter your email: ")
    password = input("Enter your password: ")

    # Check credentials and perform validation
    if useremail == "rajesh@netenrich.com" and password == "pass":
        print("Login successful!")
        rajesh_cli()
    else:
        print("Invalid credentials. Exiting...")


def get_tickets():
    # Implement your logic to retrieve the list of ticket IDs here
    ticket_ids = [1, 2, 3, 4, 5]
    print("Ticket IDs: ", ticket_ids)


def add_numbers(numbers):
    # Parse and calculate the sum of numbers
    result = sum(numbers)
    print("Sum: ", result)


def rajesh_cli():
    while True:
        command = input("rajesh > ")
        if command == "exit":
            break
        elif command == "get tickets":
            get_tickets()
        elif command.startswith("add "):
            numbers = list(map(int, command[4:].split(",")))
            add_numbers(numbers)
        else:
            print("Invalid command. Please try again.")


def main():
    parser = argparse.ArgumentParser(prog="rajesh_login")
    parser.set_defaults(func=login)

    args = parser.parse_args()
    args.func()


if __name__ == "__main__":
    main()
