def get_mask_account(account_number: str) -> str:
    """ Функция которая принимает на вход
    номер счета и возвращает его маску """
    first_mask = "**"
    last_mask = account_number[-4:]

    return f"{first_mask}{last_mask}"

if __name__ == "__main__":
    account_number = ["73654108430135874305"]
    for an in account_number:
        print(f"{get_mask_account(an)}")