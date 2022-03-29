import xlsxwriter
from pprint import pprint


def create_teacher_results(data: dict, filename: str) -> str:
    workbook = xlsxwriter.Workbook(f'downloads/{filename}')
    form = workbook.add_format()
    form.set_font('Arial')
    form.set_font_size(12)
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 35)
    worksheet.set_column(1, 1, 25)
    count = 1
    for contest in data:
        title = ('ДДТ "Юность"', contest['teacher'])
        header = (contest['union'], '', 'уровень', 'номинация', 'дистанционный', 'коллектив',
                  'дата проведения', 'ФИО')
        contest['distant'] = 'Да' if contest['distant'] else 'Нет'
        contest['collective'] = 'Да' if contest['distant'] else 'Нет'
        body = (contest['level'], contest['nomination'], contest['distant'], contest['collective'],
                contest['date'], 'Место, степень, участие')
        parts_names = (name for name in contest['participants'])
        parts_positions = (pos for pos in contest['participants'].values())
        if count == 1:
            worksheet.write_column('A1', title)
            worksheet.write_column('A3', header)
            header_size = len(title) + len(header) + 1
            worksheet.write_column(f'B{header_size / 2}', body)
            worksheet.write_column(f'A{header_size}', parts_names)
            worksheet.write_column(f'B{header_size}', parts_positions)
            count += 1
            prev_size = len(contest['participants']) + header_size + 2
        else:
            header_size = len(header) + 1
            worksheet.write_column(f'A{prev_size}', header)
            worksheet.write_column(f'B{prev_size + 2}', body)
            worksheet.write_column(f'A{prev_size + header_size}', parts_names)
            worksheet.write_column(f'B{prev_size + header_size}', parts_positions)
            prev_size = len(contest['participants']) + header_size + 2
    workbook.close()
    return f'downloads/{filename}'


def create_all_teachers(data: dict, filename: str) -> str:
    workbook = xlsxwriter.Workbook(f'downloads/{filename}')
    header_format = workbook.add_format()
    header_format.set_font('Arial')
    header_format.set_font_size(12)
    header_format.set_bg_color('#4285F4')
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 15)
    worksheet.set_column(1, 1, 10)
    worksheet.set_column(2, 2, 20)
    worksheet.set_column(3, 3, 7)
    worksheet.set_column(4, 4, 25)
    worksheet.set_column(5, 5, 30)
    worksheet.set_column(6, 6, 30)
    worksheet.set_column(7, 7, 20)
    worksheet.set_column(8, 8, 15)
    header = ('Педагог', 'Уровень', 'Место проведения', 'Дистанционный',
              'Объединение', 'ФИО участника', 'Итог', 'Дата проведения')
    worksheet.write_row('A1', header, header_format)
    for idx, teacher in enumerate(data):
        worksheet.write(f'A{idx + 2}', teacher)
        body = [data[teacher]['level'],
                data[teacher]['place'],
                'Да' if data[teacher]['distant'] else 'Нет',
                data[teacher]['nomination']]
                
    workbook.close()
    return f'downloads/{filename}'
