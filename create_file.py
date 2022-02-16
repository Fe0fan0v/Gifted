import xlsxwriter


def create_contest_result(data, count, worksheet):
    header_size = 14
    body_size = len(data['participants'])
    header = ('ДДТ "Юность"', data['teacher'], data['union'], '', '', '',
              'уровень', 'номинация', 'дистанционный', 'коллектив',
              'дата проведения', 'ФИО')
    data['distant'] = 'Да' if data['distant'] else 'Нет'
    data['collective'] = 'Да' if data['distant'] else 'Нет'
    body = (data['level'], data['nomination'], data['distant'], data['collective'],
            data['date'], 'Место, степень, участие')
    parts_names = (name for name in data['participants'])
    parts_positions = (pos for pos in data['participants'].values())
    worksheet.write_column(f'A{count}', header)
    worksheet.write_column(f'B{header_size / 2}', body)
    worksheet.write_column(f'A{header_size}', parts_names)
    worksheet.write_column(f'B{header_size}', parts_positions)
    return body_size


def create_teacher_results(data, filename):
    workbook = xlsxwriter.Workbook(f'downloads/{filename}')
    form = workbook.add_format()
    form.set_font('Arial')
    form.set_font_size(12)
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 35)
    worksheet.set_column(1, 1, 25)
    for contest in data:
        count = 1
        create_contest_result(contest, count, worksheet)
    workbook.close()
    return f'downloads/{filename}'
