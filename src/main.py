from src.database import fetch_customer_data, fetch_all_payment_terms, fetch_completion_of_work
from src.document_generator import generate_docx
from src.user_input import get_user_input

def main():
    # Получение данных
    customer_id = int(input("Введите ID клиента: "))
    customer = fetch_customer_data(customer_id)

    payment_term = fetch_all_payment_terms()
    if not payment_term:
        return  # Если пользователь не выбрал условия оплаты, завершить программу


    completion = fetch_completion_of_work()

    # Получение пользовательского ввода
    contract_number, location, doc_date, work_list, total_cost = get_user_input()

    # Генерация документа

    generate_docx(customer, work_list, payment_term, completion, contract_number, location, doc_date, total_cost)
    print(f"Документ сохранен в папке docs_out под именем doc_{contract_number}.docx")

if __name__ == "__main__":
    main()
