from typing import Dict, List, Tuple

from utils import delimiter

# -------------------------------------------------------

# Задание 1
# Дан список учеников, нужно посчитать количество повторений каждого имени ученика
# Пример вывода:
# Вася: 1
# Маша: 2
# Петя: 2
delimiter()
students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Петя'},
]

rv = {}
for student in students:
    name = student['first_name']
    rv[name] = rv.get(name, 0) + 1

for name, num in rv.items():
    print(f'{name}: {num}')

# -------------------------------------------------------

# Задание 2
# Дан список учеников, нужно вывести самое часто повторящееся имя
# Пример вывода:
# Самое частое имя среди учеников: Маша
delimiter()
students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Оля'},
]

def get_student_with_max_name_repeat_in_class(cls: List[Dict[str, str]]) -> Tuple:
    rv = {}
    max_student, max_num = '', 0
    for student in students:
        name = student['first_name']
        rv[name] = rv.get(name, 0) + 1

        if max_num < rv[name]:
            max_student, max_num = name, rv[name]

    return max_student, max_num

max_student, max_num = get_student_with_max_name_repeat_in_class(students)

print(f'Самое частое имя среди учеников: {max_student}')

# -------------------------------------------------------

# Задание 3
# Есть список учеников в нескольких классах, нужно вывести самое частое имя в каждом классе.
# Пример вывода:
# Самое частое имя в классе 1: Вася
# Самое частое имя в классе 2: Маша
delimiter()
school_students = [
    [  # это – первый класс
        {'first_name': 'Вася'},
        {'first_name': 'Вася'},
    ],
    [  # это – второй класс
        {'first_name': 'Маша'},
        {'first_name': 'Маша'},
        {'first_name': 'Оля'},
    ],[  # это – третий класс
        {'first_name': 'Женя'},
        {'first_name': 'Петя'},
        {'first_name': 'Женя'},
        {'first_name': 'Саша'},
    ],
]

for cls_num, students in enumerate(school_students, start=1):
    max_student, max_num = get_student_with_max_name_repeat_in_class(students)
    print(f'Самое частое имя в классе {cls_num}: {max_student}')

# -------------------------------------------------------

# Задание 4
# Для каждого класса нужно вывести количество девочек и мальчиков в нём.
# Пример вывода:
# Класс 2a: девочки 2, мальчики 0 
# Класс 2б: девочки 0, мальчики 2
delimiter()
school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '2б', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
    {'class': '2в', 'students': [{'first_name': 'Даша'}, {'first_name': 'Олег'}, {'first_name': 'Маша'}]},
]
is_male = {
    'Олег': True,
    'Маша': False,
    'Оля': False,
    'Миша': True,
    'Даша': False,
}

def get_gender_by_class_in_school(
        school: List[Dict[str, str]], is_male: Dict[str, bool], print_out: bool = False
) -> List[Dict[str, str]]:
    rv = []
    for cls in school:
        class_name = cls['class']
        students = cls['students']

        female_num, male_num = 0, 0
        for student in students:
            name = student['first_name']

            if is_male[name]:
                male_num += 1
            else:
                female_num += 1

        gender_by_class = {
            'cls_name': class_name,
            'male_num': male_num,
            'female_num': female_num
        }
        rv.append(gender_by_class)

        if print_out:
            print('Класс {cls_name}: девочки {female_num}, мальчики {male_num}'.format(**gender_by_class))

    return rv

get_gender_by_class_in_school(school, is_male, True)

# -------------------------------------------------------

# Задание 5
# По информации о учениках разных классов нужно найти класс, в котором больше всего девочек и больше всего мальчиков
# Пример вывода:
# Больше всего мальчиков в классе 3c
# Больше всего девочек в классе 2a
delimiter()
school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '3c', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
]
is_male = {
    'Маша': False,
    'Оля': False,
    'Олег': True,
    'Миша': True,
}

max_male_cls, max_male_num = '', 0
max_female_cls, max_female_num = '', 0
gender_by_class = get_gender_by_class_in_school(school, is_male)
# NOTE: more optimal way is to integrate these check into 'get_gender_by_class_in_school' function, but this
# approach is more human friendly, by my opinion (this is not BigData, right?).
for cls in gender_by_class:
    if max_male_num < cls['male_num']:
        max_male_num = cls['male_num']
        max_male_cls = cls['cls_name']

    if max_female_num < cls['female_num']:
        max_female_num = cls['female_num']
        max_female_cls = cls['cls_name']

print(f'Больше всего мальчиков в классе {max_male_cls}')
print(f'Больше всего девочек в классе {max_female_cls}')
