from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from num2words import num2words
import os



def generate_docx(customer, work_list, payment_term, completion, contract_number, location,
                  doc_date, total_cost):
    doc = Document()

    # Apply styles and margins
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Courier New'
    font.size = Pt(12)
    for section in doc.sections:
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.5)

    # Header
    p = doc.add_paragraph(f'ДОГОВОР № {contract_number}', style='Normal')
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = p.runs[0]
    run.font.size = Pt(12)
    run.font.bold = True

    # Date
    table = doc.add_table(rows=1, cols=2)
    cell1 = table.cell(0, 0)
    cell1.text = 'г. Минск'
    cell1.paragraphs[0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    cell1.paragraphs[0].runs[0].font.size = Pt(10)

    cell2 = table.cell(0, 1)
    cell2.text = doc_date
    cell2.paragraphs[0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    cell2.paragraphs[0].runs[0].font.size = Pt(10)

    # Main text
    p = doc.add_paragraph()
    p.add_run(
        f"{customer[1]}, в лице {customer[9]} {customer[2]}, действующего на основании {customer[3]}, именуемое в дальнейшем ЗАКАЗЧИК, с одной стороны, и индивидуальный предприниматель Панченко Константин Александрович, действующий в качестве индивидуального предпринимателя на основании регистрационного свидетельства 0157617, выданного МГИК «04» декабря 2008г., именуемый в дальнейшем ИСПОЛНИТЕЛЬ, с другой стороны, заключили настоящий договор о нижеследующем:\n\n"
    ).font.size = Pt(12)

    # Section 1
    doc.add_paragraph('1. ЗАКАЗЧИК поручает, а ИСПОЛНИТЕЛЬ принимает на себя выполнение следующих работ:', style='Normal').runs[0].font.bold = True
    for idx, work in enumerate(work_list, 1):
        doc.add_paragraph(f"1.{idx}. {work}", style='Normal')

    # Section 2
    doc.add_paragraph(f'2. Место проведения работ: {location}.', style='Normal')

    # Section 3
    rubles, kopecks = divmod(total_cost, 1)
    rubles = int(rubles)
    kopecks = round(kopecks * 100)  # Округление до целых копеек
    sum_in_words = num2words(rubles, lang='ru', to='cardinal')

    doc.add_paragraph(
        f'3. Стоимость работ, согласно Приложению 1 к настоящему договору, составляет {total_cost:.2f} '
        f'({sum_in_words.capitalize()} белорусских рублей 00 коп.). Без НДС.',
        style='Normal'
    )

    # Section 4
    days_in_words = num2words(30, lang='ru', to='cardinal')  # Пример для 30 дней
    doc.add_paragraph(
        f'4. Условия оплаты: Заказчик производит  {completion} Работ в течение {days_in_words} банковских дней после подписания сторонами Акта сдачи-приемки работ, являющимся Приложением 2 к настоящему договору. Заказчик по своему усмотрению может произвести полную или частичную предоплату работ.',
        style='Normal'
    )

    # Section 5
    doc.add_paragraph(f'5. Окончание Работ: ......', style='Normal')

    # Section 6
    doc.add_paragraph(
        '6. Заказчик в день получения акта сдачи-приемки работ обязан вернуть Исполнителю подписанный акт сдачи-приемки работ или мотивированный отказ от приемки работ.',
        style='Normal'
    )

    # Section 7
    doc.add_paragraph(
        '7. По всем остальным вопросам стороны руководствуются действующим законодательством Республики Беларусь.',
        style='Normal'
    )

    # Party details in a table
    doc.add_paragraph('Реквизиты сторон:', style='Normal').runs[0].font.bold = True
    table = doc.add_table(rows=2, cols=2)
    table.columns[0].width = Pt(200)
    table.columns[1].width = Pt(200)

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Исполнитель'
    hdr_cells[1].text = 'Заказчик'
    for cell in hdr_cells:
        cell.paragraphs[0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)

    # Fill in table
    row_cells = table.rows[1].cells
    text_ispolnitel = (
        'ИП Панченко К.А.\n'
        '220007 г.Минск, ул.Жуковского 9/2-6\n'
        'IBAN: BY47MTBK30130001093300064929\n'
        'ЗАО «МТБанк», BIC MTBKBY22,\n'
        'г.Минск, ул.Толстого, 10\n'
        'УНП 191085820'
    )
    text_zakazchik = (
        f'{customer[1]}\n'
        f'{customer[5]}\n'
        f'УНП: {customer[6]}\n'
        f'ОКПО: {customer[7]}\n'
        f'Р/С: {customer[8]}'
    )

    # Set text and font size for the first cell
    p_ispolnitel = row_cells[0].paragraphs[0]
    p_ispolnitel.add_run(text_ispolnitel).font.size = Pt(9)

    # Set text and font size for the second cell
    p_zakazchik = row_cells[1].paragraphs[0]
    p_zakazchik.add_run(text_zakazchik).font.size = Pt(9)


    # Signatures
    table = doc.add_table(rows=1, cols=2)
    table.autofit = True

    cell1 = table.cell(0, 0)
    cell1.text = 'Исполнитель_________(К.А. Панченко)'
    cell1.paragraphs[0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    cell1.paragraphs[0].runs[0].font.size = Pt(9)

    cell2 = table.cell(0, 1)
    cell2.text = f'Заказчик___________({customer[2]})'
    cell2.paragraphs[0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    cell2.paragraphs[0].runs[0].font.size = Pt(9)

    p = doc.add_paragraph()
    p = doc.add_paragraph()

    # Appendix 1
    p = doc.add_paragraph(f'Приложение 1 к ДОГОВОРУ № {contract_number} от {doc_date}', style='Normal')
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = p.runs[0]
    run.bold = True
    run.font.size = Pt(12)

    doc.add_paragraph('Протокол согласования договорной цены', style='Normal').alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # Appendix 1 Table
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'

    table.columns[0].width = Pt(50)
    table.columns[1].width = Pt(350)
    table.columns[2].width = Pt(100)

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '№'
    hdr_cells[1].text = 'Наименование работ'
    hdr_cells[2].text = 'Стоимость, руб.'

    for cell in hdr_cells:
        cell.paragraphs[0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(12)

    # Add data to the table
    num_works = len(work_list)
    price_per_work = total_cost / num_works  # Рассчитываем стоимость на каждую работу

    for idx, work in enumerate(work_list, 1):
        row_cells = table.add_row().cells
        row_cells[0].text = str(idx)
        row_cells[1].text = work
        row_cells[2].text = f'{price_per_work:.2f}'  # Записываем рассчитанную стоимость
        row_cells[2].paragraphs[0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

    # Total row
    row_cells = table.add_row().cells
    row_cells[0].text = 'Итого:'
    cell = row_cells[1]
    cell.merge(row_cells[2])
    cell.text = f'{total_cost:.2f}'
    cell.paragraphs[0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    for run in cell.paragraphs[0].runs:
        run.font.bold = True
        run.font.size = Pt(12)

    # Total sum
    sum_total = total_cost
    doc.add_paragraph(f'Итого стоимость работ: {total_cost:.2f} ({sum_in_words.capitalize()} белорусских рублей 00 коп.). Без НДС.', style='Normal')

    # Signatures
    table = doc.add_table(rows=1, cols=2)
    table.autofit = True

    cell1 = table.cell(0, 0)
    cell1.text = 'Исполнитель_________(К.А. Панченко)'
    cell1.paragraphs[0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    cell1.paragraphs[0].runs[0].font.size = Pt(9)

    cell2 = table.cell(0, 1)
    cell2.text = f'Заказчик___________({customer[2]})'
    cell2.paragraphs[0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    cell2.paragraphs[0].runs[0].font.size = Pt(9)

    # Create output directory if it does not exist
    os.makedirs('docs_out', exist_ok=True)

    # Save document with contract number
    file_name = f'docs_out/contract_{contract_number}.docx'
    doc.save(file_name)
    print(f'Документ сохранен как {file_name}')
