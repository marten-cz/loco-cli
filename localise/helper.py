from colorama import Fore, Style


class OperationException(Exception):
    """Raise when operation failed with an error"""


def print_error(message):
    print(Fore.RED + message + Style.RESET_ALL)


def print_success(message):
    print(Fore.RED + message + Style.RESET_ALL)
