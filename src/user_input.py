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

    return contract_number, location, doc_date, work_list
