from src.database import *

def get_user_input():
    contract_number = input("Введите номер договора: ")
    location = input("Введите место проведения работ: ")
    doc_date = input("Введите дату (дд.мм.гггг): ")
    work_list = []
    while True:
        work = input("Введите  работы: ")
        if work == "":
            break
        work_list.append(work)

        # Ввод стоимости
    while True:
        try:
            total_cost = float(input("Введите стоимость работ (в рублях): "))
            break
        except ValueError:
            print("Пожалуйста, введите числовое значение.")

    return contract_number, location, doc_date, work_list, total_cost


def choose_payment_term():
    payment_terms = fetch_all_payment_terms()
    if not payment_terms:
        print("Не удалось загрузить условия оплаты.")
        return None

    print("Выберите условия оплаты:")
    for idx, term in enumerate(payment_terms, 1):
        print(f"{idx}. {term[1]}")

    while True:
        try:
            choice = int(input("Введите номер выбранного условия оплаты: "))
            if 1 <= choice <= len(payment_terms):
                return payment_terms[choice - 1]
            else:
                print(f"Пожалуйста, введите число от 1 до {len(payment_terms)}.")
        except ValueError:
            print("Пожалуйста, введите числовое значение.")