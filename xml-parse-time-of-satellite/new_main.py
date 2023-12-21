import os
import time
import xml.etree.ElementTree as ET
import pandas
import datetime
import playsound


# запуск файла mp3
def start_sound():
    playsound.playsound('start.mp3')
#    return print('событие было')


def start_sound_3m():
    playsound.playsound('before_start.mp3')
 #   return print('событие было')

# функция проверки номера витка
def sat_turn_checker(mass):
    mass_int = [int(i) for i in mass]
    for i in range(len(mass_int)):
        for k in range(i + 1, len(mass_int)):
            if mass_int[i] == mass_int[k]:
                mass_int[k] += 1
    mass_out = [str(i) for i in mass_int]
    return mass_out

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# функция "округления" времени до секунд и приведение в виду 12.01.2022 06:04:58 для массива
def time_round_sec(mass):
    for i in range(len(mass)):
        struct = time.strptime(mass[i][:mass[i].index('.', -6)], '%Y.%m.%d %H:%M:%S')
        mass[i] = time.strftime('%d.%m.%Y %H:%M:%S', struct)
    return mass


# выяснение сколько дней в месяце
def days_in_any_month(month, year):
    days_in = 2
    if month in ['01', '03', '05', '07', '08', '10', '12']:
        days_in = 31
    elif month in ['04', '06', '09', '11']:
        days_in = 30
    elif month == '02':
        if (int(year) % 4 == 0) and (int(year) % 100 != 0) or (int(year) % 400 == 0):
            days_in = 29
        else:
            days_in = 28
    return days_in


# функция отнимания 3хминут от настоящего времени из строки представления
def time_20sec_before(el):
    date_el, time_el = el.split()
    h, m, s = time_el.split(':')
    day, month, year = date_el.split('.')
    days_in_month = days_in_any_month(month, year)
    if month == '01':
        prev_month = '12'
        prev_year = str(int(year) - 1)
    else:
        prev_month = str(int(month) - 1)
        if int(prev_month) < 10:
            prev_month = '0' + prev_month
        prev_year = year
    prev_days_in_month = days_in_any_month(prev_month, prev_year)
    # print(prev_month, 'prev_month')
    # print(prev_days_in_month, 'prev_days_in_month')
    if int(s) >= 20:
        s = str((int(s) - 20) % 60)
        if int(s) < 10:
            s = '0' + s
    else:  # s < 20
        s = str((60 + int(s) - 20) % 60)
        # m= m-1
        if int(m) >= 1:
            m = str((int(m) - 1) % 60)
        else:  # m < 3
            m = str((60 + int(m) - 1) % 60)
            if int(h) != 0:
                h = str((int(h) - 1) % 24)
                if int(h) < 10:
                    h = '0' + h
            else:  # ??? h=00
                h = str((24 - 1) % 24)
                if day != '01':
                    print(1)
                    print(days_in_month)
                    day = str((int(day) - 1) % days_in_month)
                    if int(day) < 10:
                        day = '0' + day
                else:  # day=01
                    # print(2)
                    day = str(prev_days_in_month)
                    if month != '01':
                        # print(3)
                        month = str((int(month) - 1) % 12)
                        if int(month) < 10:
                            month = '0' + month
                    else:
                        # print(4)
                        month = str(prev_month)
                        year = str(int(year) - 1)
    date_el = '.'.join([day, month, year])
    if len(m) == 1:
        m = '0' + m
    time_el = ':'.join([h, m, s])
    return ' '.join([date_el, time_el])


# функция отнимания 3хминут от настоящего времени из строки представления
def time_3m_before(el):
    date_el, time_el = el.split()
    h, m, s = time_el.split(':')
    day, month, year = date_el.split('.')
    days_in_month = days_in_any_month(month, year)
    if month == '01':
        prev_month = '12'
        prev_year = str(int(year) - 1)
    else:
        prev_month = str(int(month) - 1)
        if int(prev_month) < 10:
            prev_month = '0' + prev_month
        prev_year = year
    prev_days_in_month = days_in_any_month(prev_month, prev_year)
    # print(prev_month, 'prev_month')
    # print(prev_days_in_month, 'prev_days_in_month')
    if int(s) >= 20:
        s = str((int(s) - 20) % 60)
        if int(s) < 10:
            s = '0' + s
    else:  # s < 20
        s = str((60 + int(s) - 20) % 60)
        # m= m-1
        if int(m) >= 1:
            m = str((int(m) - 1) % 60)
        else:  # m < 3
            m = str((60 + int(m) - 1) % 60)
            if int(h) != 0:
                h = str((int(h) - 1) % 24)
                if int(h) < 10:
                    h = '0' + h
            else:  # ??? h=00
                h = str((24 - 1) % 24)
                if day != '01':
                    print(1)
                    print(days_in_month)
                    day = str((int(day) - 1) % days_in_month)
                    if int(day) < 10:
                        day = '0' + day
                else:  # day=01
                    # print(2)
                    day = str(prev_days_in_month)
                    if month != '01':
                        # print(3)
                        month = str((int(month) - 1) % 12)
                        if int(month) < 10:
                            month = '0' + month
                    else:
                        # print(4)
                        month = str(prev_month)
                        year = str(int(year) - 1)
    if int(m) >= 3:
        m = str((int(m) - 3) % 60)
    else:  # m < 3
        m = str((60 + int(m) - 3) % 60)
        if int(h) != 0:
            h = str((int(h) - 1) % 24)
            if int(h) < 10:
                h = '0' + h
        else:  # ??? h=00
            h = str((24 - 1) % 24)
            if day != '01':
                print(1)
                print(days_in_month)
                day = str((int(day) - 1) % days_in_month)
                if int(day) < 10:
                    day = '0' + day
            else:  # day=01
                day = str(prev_days_in_month)
                if month != '01':
                    month = str((int(month) - 1) % 12)
                    if int(month) < 10:
                        month = '0' + month
                else:
                    month = str(prev_month)
                    year = str(int(year) - 1)
    date_el = '.'.join([day, month, year])
    if len(m) == 1:
        m = '0' + m
    time_el = ':'.join([h, m, s])
    return ' '.join([date_el, time_el])


# функция "округления" времени до секунд и приведение к виду 12.01.2022 06:04:58 +3hours для элемента
def time_round_el(el):  # добавить переход суток
    date_el, time_el = el.split()
    h, m, s = time_el.split(':')
    s = s.split('.')[0]
    day, month, year = date_el.split('.')
    days_in_month = days_in_any_month(month, year)
    if h < '21':
        h = str((int(h) + 3) % 24)
    else:
        if day != str(days_in_month):
            day = str((int(day) + 1) % days_in_month)
        else:
            day = str((int(day) + 1) % days_in_month)
            if month != '12':
                month = str((int(month) + 1) % 12)
            else:
                month = str((int(month) + 1) % 12)
                year = str(int(year) + 1)
        h = str((int(h) + 3) % 24)  # добавить строку на комп!!! добавлено
    date_el = '.'.join([day, month, year])
    time_el = ':'.join([h, m, s])
    return ' '.join([date_el, time_el])


# функция добавелния 3х часов поэлементно для массива
def time_3h_plus(el):  # для элемента
    date_el, time_el = el.split()
    h, m, s = time_el.split(':')
    day, month, year = date_el.split('.')
    days_in_month = days_in_any_month(month, year)
    # print(month)
    # print(days_in_month)
    if h < '21':
        h = str((int(h) + 3) % 24)
        if int(h) < 10:
            h = '0' + h
    else:
        if day != str(days_in_month):
            day = str((int(day) + 1) % days_in_month)
            if int(day) < 10:
                day = '0' + day
            # print(1)
        else:
            day = str((int(day) + 1) % days_in_month)
            if int(day) < 10:
                day = '0' + day
            # print(2)
            if month != '12':
                month = str((int(month) + 1) % 12)
                if int(month) < 10:
                    month = '0' + month
                # print(3)
            else:
                month = str((int(month) + 1) % 12)
                if int(month) < 10:
                    month = '0' + month
                year = str(int(year) + 1)
                # print(4)
        h = str((int(h) + 3) % 24)
        if int(h) < 10:
            h = '0' + h
    date_el = '.'.join([day, month, year])
    time_el = ':'.join([h, m, s])
    return ' '.join([date_el, time_el])


def time_3h_plus_mass(mass):  # применение к массиву
    return list(map(time_3h_plus, mass))


# Проверка на ночное время для мчс
def check_time_night(el):
    date_el, time_el = el.split()
    h, m, s = time_el.split(':')
    #    print(h)
    if int(h) >= 20 or int(h) <= 8:
        #        print(el)
        return True
    else:
        return False


def date_time_go_in_time_el(el):
    date_el, time_el = el.split()
    h, m, s = time_el.split(':')
    time_el = ':'.join([h, m])
    return (time_el)


def date_time_go_in_time_mass(mass):
    return list(map(date_time_go_in_time_el, mass))


def round_el(mass):
    return list(map(lambda x: x.split('.')[0], mass))


# функция добавления 3х часов для МЧС
def time_zone_checker(mass):
    for i in range(len(mass)):
        mass[i] = time_round_el(mass[i])
    return mass


# функция сравнения времени в нашем виде
def compare_time_lower_than_now(time1):
    date_el1, time_el1 = time1.split()
    h1, m1, s1 = time_el1.split(':')
    day1, month1, year1 = date_el1.split('.')
    date_el, time_el = (time.strftime('%d.%m.%Y %H:%M:%S')).split()
    h, m, s = time_el.split(':')
    day, month, year = date_el.split('.')
    date_arr = list(map(int, [year, month, day, h, m, s]))
    date1_arr = list(map(int, [year1, month1, day1, h1, m1, s1]))
    for i in range(6):
        return date_arr > date1_arr


# формируем имя файла для мчс
def name_gen(text):
    date_in, time_in, text_in = text.split()
    year, month, day = date_in.split('_')
    return ('Расписание сеансов ' + '.'.join([day, month, year]))


# функция работы с одним .xml-файлом. проверяет витки и создает файл для мчс
# функция работы с одним .xml-файлом. проверяет витки и создает файл для мчс
def one_xml_work(name_file):
    tree = ET.parse(name_file)
    root = tree.getroot()
    date_time_end_array = []
    sat_turn_in = []
    date_time_start_array = []
    sat_name_mchs = []
    culm_el = []
    # Парсим содержисое тегов из .xml
    for el in root.findall('session'):
        t_start = el.find('date_time_start').text
        date_time_start_array.append(t_start)
        t_end = el.find('date_time_end').text
        date_time_end_array.append(t_end)
        sat_turn_in.append(el.find('sat_turn').text)
        sat_name_mchs.append(el.find('sat_name').text)
        culm_el.append(el.find('el_culm').text)
    # записываем правильные витки в файл
    temp = 0
    sat_turn_out = sat_turn_checker(sat_turn_in)
    for el in root.iter('sat_turn'):
        el.text = sat_turn_out[temp]
        temp += 1
    tree.write(name_file)

    date_time_start_array1 = date_time_start_array.copy()
    res_time_start = time_round_sec(date_time_start_array1)

    # добавление 3х часов к времени
    date_time_st_rcurchs = time_zone_checker(date_time_start_array)
    date_time_end_rcurchs = time_zone_checker(date_time_end_array)

    # редактирование списков(удаление ненужных сеансов при условиях)
    index = []
    for i in range(len(sat_name_mchs)):
        if sat_name_mchs[i] == 'FENGYUN-3D':
            index.append(i)
        elif sat_name_mchs[i] == 'METOP-B' or sat_name_mchs[i] == 'METOP-C':
            if not check_time_night(date_time_st_rcurchs[i]):
                index.append(i)

    for el in index[::-1]:
        sat_name_mchs.pop(el)
        date_time_st_rcurchs.pop(el)
        date_time_end_rcurchs.pop(el)
        culm_el.pop(el)

    # Часть pandas
    name_excel_file = name_gen(name_file[:-4]) + '.xls'
    df = pandas.DataFrame({'sat_name': sat_name_mchs, 'time_start': date_time_go_in_time_mass(date_time_st_rcurchs),
                           'time_end': date_time_go_in_time_mass(date_time_end_rcurchs), 'el_culm': round_el(culm_el)})
    writer = pandas.ExcelWriter(name_excel_file, engine='xlwt')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return res_time_start


start_sound()
time.sleep(1)
start_sound_3m()
time.sleep(1)
# print(time_round_el('20.01.2022 23:13:08.123'))

start_time = time.time()

date_time_start_array_all_files = []
# print(date_time_start_array_all_files)
# часть работы с файлами. собирает xml из папки в список
dirname = 'D:/Планировщик/plan/sess_plans/'  # путь к директории с планами
dirname_main = 'D:/Kazak/xml-parse'  # путь к файлу мэйн.ексе
os.chdir(dirname)
files = os.listdir()  # собирает список всех файлов и папок
true_files = []  # содержит только имена .xml
for el in files:
    if 'sess_plan.xml' in el:
        true_files.append(el)

print(true_files)
for file in true_files:
    date_time_start_array_all_files += one_xml_work(file)
os.chdir('D:/Kazak/xml-parse')