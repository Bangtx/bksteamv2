import numpy as np
import pandas as pd
from models.home_work_file import HomeWorkFile


def to_csv_by_class(classrooms, students, roll_call):
    header = ['', 'Lớp học', 'Họ và tên', 'Trình độ', 'Số buổi\nhọc trong tháng', 'Ngày', 'Tình trạng điểm danh',
              'Tình trạng làm bài tập về nhà', 'Kết quả kiểm tra đánh giá', 'Nhận Xét']
    dates = list(set(list(map(lambda x: x['date'], roll_call))))
    exel_rows = [header]
    for c_index, classroom in enumerate(classrooms):
        for s_index, student in enumerate(students):
            for d_index, date in enumerate(dates):
                exel_row = ['', '', '', '', '', '', '', '', '', '']

                roll_call_student = list(filter(
                    lambda x: x['student']['id'] == student['id'], roll_call
                ))

                roll_call_student_this_day = list(filter(lambda x: x['date'] == date, roll_call_student))

                if c_index == 0 and s_index == 0 and d_index == 0:
                    exel_row[1] = classroom['name']
                if d_index == 0:
                    exel_row[2] = student['name']
                    exel_row[4] = f"""{len(
                        list(
                            filter(
                                lambda x: x['absent_type'] == 1, roll_call_student
                            )
                        )
                    )} / {len(roll_call_student)}
                    """
                    exel_row[3] = classroom['room'] if classroom['room'] else ''

                exel_row[5] = str(date)
                exel_row[6] = (
                    to_absent(roll_call_student_this_day[0]['absent_type']) if roll_call_student_this_day else None
                )
                home_work_file = HomeWorkFile.get_or_none(
                    classroom=classroom['id'],
                    date=date
                )
                if home_work_file:
                    exel_row[7] = f"""{home_work_file.description if home_work_file.description else ''} {home_work_file.file_url if home_work_file.file_url else ''}"""
                exel_rows.append(exel_row)
    # print(exel_rows)
    arr = np.asarray(exel_rows)
    pd.DataFrame(arr).to_csv('sample.csv', header=False, index=False)


def to_absent(absent):
    if absent == 1:
        return 'Đúng giờ'
    if absent == 2:
        return 'Nghỉ có phép'
    if absent == 3:
        return 'Nghỉ không phép'
    if absent == 4:
        return 'Muộn có phép'
    if absent == 5:
        return 'Muộn không phép'
    return 'Không điểm danh'
