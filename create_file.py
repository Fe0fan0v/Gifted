import xlsxwriter


def create(data, filename):
    workbook = xlsxwriter.Workbook(f'downloads/{filename}')
    form = workbook.add_format()
    form.set_font('Arial')
    form.set_font_size(12)
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 35)
    worksheet.set_column(1, 1, 25)
    header = ('ДДТ "Юность"', data['teacher'], data['union'], '', '', '',
              'уровень', 'номинация', 'дистанционный', 'коллектив',
              'дата проведения', 'ФИО')
    data['distant'] = 'Да' if data['distant'] else 'Нет'
    data['collective'] = 'Да' if data['distant'] else 'Нет'
    body = (data['level'], data['nomination'], data['distant'], data['collective'],
            data['date'], 'Место, степень, участие')
    parts_names = (name for name in data['participants'])
    parts_positions = (pos for pos in data['participants'].values())
    worksheet.write_column('A1', header)
    worksheet.write_column('B7', body)
    worksheet.write_column('A14', parts_names)
    worksheet.write_column('B14', parts_positions)
    workbook.close()
    return f'downloads/{filename}'
