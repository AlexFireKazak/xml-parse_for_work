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


# функция "округления" времени до секунд и приведение в виду 12.01.2022 06:04:58 для массива
def time_round_sec(mass):
    for i in range(len(mass)):
        struct = time.strptime(mass[i][:mass[i].index('.', -6)], '%Y.%m.%d %H:%M:%S')
        mass[i] = time.strftime('%d.%m.%Y %H:%M:%S', struct)
    return mass

# функция "округления" времени до секунд и приведение к виду object datetime 12.01.2022 06:04:58 +3hours для элемента
def time_round_el(el:str):
    date_el, time_el = el.split()
    h, m, s = time_el.split(':')
    s = s.split('.')[0]
    day, month, year = date_el.split('.')
    datetime_el = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(h), minute=int(m), second=int(s))
    delta = datetime.timedelta(hours=3)
    datetime_el += delta
    return datetime_el

def time_round_el1(el:str):
    date_el, time_el = el.split()
    h, m, s = time_el.split(':')
    s = s.split('.')[0]
    year, month, day = date_el.split('.')
    datetime_el = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(h), minute=int(m), second=int(s))
    delta = datetime.timedelta(hours=3)
    datetime_el += delta
    return datetime_el
# print(time_round_el1('2022.01.14 05:41:24.966'))
# функция добавления 3х часов для МЧС
def time_zone_checker(mass:list):
    for i in range(len(mass)):
        mass[i] = time_round_el1(mass[i])
    return mass

def in_datetime(el:str):
    date_el, time_el = el.split()
    h, m, s = time_el.split(':')
    s = s.split('.')[0]
    day, month, year = date_el.split('.')
    datetime_el = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(h), minute=int(m),
                                    second=int(s))
    return datetime_el

# Проверка на ночное время для мчс
def check_time_night(el:datetime):
    h = el.hour
    # print(h)
    if int(h) >= 20 or int(h) <= 8:
        return True
    else:
        return False

def date_time_go_in_time_mass(mass):
    return list(map(lambda x: x.strftime('%H:%M:%S'), mass))


def round_el(mass):
    return list(map(lambda x: round(float(x)), mass))


# формируем имя файла для мчс
def name_gen(text):
    date_in, time_in, text_in = text.split()
    year, month, day = date_in.split('_')
    return ('Расписание сеансов ' + '.'.join([day, month, year]))


# print(date_time_go_in_time_mass([time_round_el('12.01.2022 06:04:58.456'), time_round_el('12.01.2022 07:04:58.456')]))
# print(check_time_night(time_round_el('12.01.2022 04:04:58.456')))
# print(time_round_el('12.01.2022 04:04:58.456').strftime('%H:%M:%S'))

def time_3h_plus(mass:list):
    delta = datetime.timedelta(hours=3)
    return list(map(lambda x: x + delta, mass))

# функция сравнения времени в нашем виде
def compare_time_lower_than_now(time):
    return datetime.datetime.now() > time

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
    # print(date_time_start_array1)
    res_time_start = list(map(time_round_el1,date_time_start_array1))

    # добавление 3х часов к времени
    date_time_st_rcurchs = time_zone_checker(date_time_start_array)
    date_time_end_rcurchs = time_zone_checker(date_time_end_array)

    # редактирование списков(удаление ненужных сеансов при условиях)
    index = []
    for i in range(len(sat_name_mchs)):
        if sat_name_mchs[i] == 'METOP-B' or sat_name_mchs[i] == 'METOP-C':
            if not check_time_night(date_time_st_rcurchs[i]):
                index.append(i)
        elif sat_name_mchs[i] == 'NOAA 19' or sat_name_mchs[i] == 'NOAA 18':
            if not check_time_night(date_time_st_rcurchs[i]):
                index.append(i)
        elif sat_name_mchs[i] == 'FENGYUN-3E':
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

# Рабочая часть
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

# date_time_start_array_all_files = time_3h_plus(date_time_start_array_all_files)
# print(date_time_start_array_all_files)

# print(time_3h_plus(time.strftime('%d.%m.%Y %H:%M:%S')))

# print(time.strftime('%d.%m.%Y %H:%M:%S') == res[0])
# print(res_time_start)
# print(len(res_time_start))
# print(time.strftime('%d.%m.%Y %H:%M:%S'))
# print(time_3m_before('16.01.2022 11:07:29'))
print()

# отсекаем прошедшее время, если есть
while compare_time_lower_than_now(date_time_start_array_all_files[0]):
    date_time_start_array_all_files.pop(0)
    # print(date_time_start_array_all_files[0])
    # print(len(date_time_start_array_all_files))
    if len(date_time_start_array_all_files) == 0:
        print('Нет новых сеансов')
        time.sleep(60)
        break
# реакция на время и отсекание прошедшего пока не закончится список
res_time_3m_before = list(map(lambda x: x - datetime.timedelta(minutes=3, seconds=20), date_time_start_array_all_files.copy()))
date_time_start_array_all_files = list(map(lambda x: x - datetime.timedelta(seconds=20), date_time_start_array_all_files))
# print(date_time_start_array_all_files)
print(*date_time_start_array_all_files)
print(*res_time_3m_before)
print()
# print("---%s seconds ---" % (time.time() - start_time))
while len(date_time_start_array_all_files) > 0:
    time_now = in_datetime(time.strftime('%d.%m.%Y %H:%M:%S'))
    if len(res_time_3m_before) > 1:
        if time_now in res_time_3m_before:
            print("3 минуты до начала сеанса!")
            start_sound_3m()
            res_time_3m_before.pop(0)
            continue
        # if time_now == res_time_3m_before[1]:
        #     print('3 минуты до начала сеанса!')
        #     start_sound_3m()
        #     continue
    elif len(res_time_3m_before) == 1:
        if time_now == res_time_3m_before[0]:
            print("3 минуты до начала сеанса!")
            start_sound_3m()
            #res_time_3m_before.pop(0)
            continue
    else:
        continue

    if time_now in date_time_start_array_all_files:
        print("Сеанс начат")
        start_sound()
        date_time_start_array_all_files.pop(0)
        continue
    print(time_now)
    time.sleep(1)
print('Работа программы завершена.')
time.sleep(300)

