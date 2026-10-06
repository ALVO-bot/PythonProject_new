 #card_number = 7000792289606361

def get_mask_card_number(card_number: str) -> str:
    """ Функция которая принимает на вход
    номер карты и возвращает ее маску"""
    clean_number = card_number.replace(" ", "") # Удаляем пробелы
    block_1 = clean_number[:4]
    block_2 = clean_number[5:7] + "**"
    block_3 = "****"
    block_4 = clean_number[-4:]


    return f"{block_1} {block_2} {block_3} {block_4}"

if __name__ == "__main__":
    card_number = ["7000792289606361"]
    for cn in card_number:
        print(f"{get_mask_card_number(cn)}")