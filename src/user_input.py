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
