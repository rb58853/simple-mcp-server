from dotenv import load_dotenv

load_dotenv()

from use_cases.client import run as client_test
from use_cases.auth_client import run as auth_client_test
import os


def clear_console():
    if os.name == "nt":  # Windows
        _ = os.system("cls")
    else:  # Unix/Linux
        _ = os.system("clear")


def main():
    clear_console()
    client_test()
    print(
        "\n____________________________________________________________________________________________________\n"
    )
    auth_client_test()


if __name__ == "__main__":
    main()
