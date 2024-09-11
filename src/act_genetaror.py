# act_generator.py
from src.document_generator import generate_docx

def generate_completion_act(customer, contract_number, location, doc_date, work_list, total_cost):
    # Логика создания акта выполненных работ
    act_content = {
        "customer": customer,
        "contract_number": contract_number,
        "location": location,
        "doc_date": doc_date,
        "work_list": work_list,
        "total_cost": total_cost,
    }

    # Генерация акта в docx
    generate_docx(act_content, doc_type='completion_act')
    print(f"Акт выполненных работ для контракта {contract_number} успешно создан.")
