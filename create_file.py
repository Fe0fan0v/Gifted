import xlsxwriter


def create_teacher_results(data, filename):
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
