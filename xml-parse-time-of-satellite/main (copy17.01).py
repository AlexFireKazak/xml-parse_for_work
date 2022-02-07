import xml.etree.ElementTree as ET
import os, time
#import datetime
from playsound import playsound


# функция проверки номера витка
def sat_turn_checker(mass):
    mass_int = [int(i) for i in mass]
    for i in range(len(mass_int)):
        for k in range(i+1, len(mass_int)):
            if mass_int[i] == mass_int[k]:
                mass_int[k] += 1
    mass_out = [str(i) for i in mass_int]
    return mass_out
# функция "округления" времени до секунд и приведение в виду 12.01.2022 06:04:58 для массива
def time_round_sec(mass):
    for i in range(len(mass)):
        struct = time.strptime(mass[i][:mass[i].index('.',-6)], '%Y.%m.%d %H:%M:%S')
        mass[i] = time.strftime('%d.%m.%Y %H:%M:%S', struct)
    return mass
#функция отнимания 3хминут от настоящего времени из строки представления
def time_3m_before(el):
    date_el, time_el = el.split()
    h, m, s = time_el.split(':')
    day, month, year = date_el.split('.')
    days_in_month = days_in_any_month(month, year)
    if int(m) >= 3:
        m = str((int(m) - 3)%60)
    else:
        if int(h) != 0:
            h = str((int(h) - 1)%24)
            m = str((int(m) - 3)%60)
        else:
            h = str((int(h) - 1)%24)
            if day != str(days_in_month):
                day = str((int(day) - 1)%days_in_month)
            else:
                day = str((int(day) - 1)%days_in_month)
                if month != '1':
                    month = str((int(month)-1)%12)
                else:
                    month = str(12)
                    year = str(int(year)-1)
    date_el = '.'.join([day, month, year])
    if len(m) == 1:
        m = '0' + m
    time_el = ':'.join([h,m,s])    
    return ' '.join([date_el, time_el])
# выяснение сколько дней в месяце
def days_in_any_month(month, year):
    days_in = 2
    if month in ['1','3','5','7','8','10','12']:
        days_in = 31
    elif month in ['4','6','9','11']:
        days_in = 30
    elif month == '2':
        if (int(year) % 4 == 0) and (int(year) % 100 != 0) or (int(year) % 400 == 0):
            days_in = 29
        else:
            days_in = 28  
    return days_in
# функция "округления" времени до секунд и приведение в виду 12.01.2022 06:04:58 +3hours для элемента
def time_round_el(el):#добавить переход суток
    date_el, time_el = el.split()
    h, m, s = time_el.split(':')
    s = s.split('.')[0]
    day, month, year = date_el.split('.')
    days_in_month = days_in_any_month(month, year)
    if h < '21':
        h = str((int(h) + 3)%24)
    else:
        if day != str(days_in_month):
            day = str((int(day) + 1)%days_in_month)
        else:
            day = str((int(day) + 1)%days_in_month)
            if month != '12':
                month = str((int(month)+1)%12)
            else:
                month = str((int(month)+1)%12)
                year = str(int(year)+1)
    date_el = '.'.join([day, month, year])
    time_el = ':'.join([h,m,s])
    return ' '.join([date_el, time_el])
# функция добавления 3х часов для МЧС
def time_zone_checker(mass):
    for i in range(len(mass)):
        mass[i] = time_round_el(mass[i])
    return mass
    
# тест работы с файлами
os.chdir('files')
dirname = 'files'
files = os.listdir()
true_files = [] # содержит только имена .xml
for el in files:
    if 'sess_plan.xml' in el:
        true_files.append(el)

print(true_files)

os.chdir('..')
tree = ET.parse('sess_plan_full.xml')
root = tree.getroot()

#print()
time_start = ''
# список тегов дерева
#for child in root:
#    print(child.tag, child.attrib)
#    print()
#    for el in child:
#        print(el.tag, el.attrib)
#        if el.tag == 'date_time_start':
#            time_start = el
        #print(time_start)
#print()
date_time_end_array = []
sat_turn_in = []
date_time_start_array = []
for_exel_file = []
# Парсим содержисое тегов из .xml
for el in root.findall('session'):
    t_start = el.find('date_time_start').text
    name = el.find('sat_name').text
    date_time_start_array.append(t_start)
    culm = el.find('el_culm').text
    t_end = el.find('date_time_end').text
    date_time_end_array.append(t_end)
    sat_turn_in.append(el.find('sat_turn').text)
    for_exel_file.append([name, t_start, t_end, culm])
    # print(name, t_start, t_end, culm)
#print()

# записываем правильные витки в файл
temp = 0
sat_turn_out = sat_turn_checker(sat_turn_in)

for el in root.iter('sat_turn'):
    el.text = sat_turn_out[temp]
    temp += 1
tree.write('sess_plan_full.xml')
date_time_start_array1 = date_time_start_array.copy()
res_time_start = time_round_sec(date_time_start_array1)    


#print()
print(date_time_start_array)
print()
#print(for_exel_file) #надо забить в эксель
print()

# создание xml-таблицы и запись в файл
os.system('cp sess_plan_full.xml sess_plan_rcurchs.xml') #создание копии файла(для винды заменить cp на copy)
tree2 = ET.ElementTree('sess_plan_rcurchs.xml')
root2 = tree.getroot()
# долбаное удаление лишних элементов для создания правильного xml
for parent in root2.findall('.//sat_id/..'):
    for element in parent.findall('sat_id'):
        parent.remove(element)
for parent in root2.findall('.//sat_turn/..'):
    for element in parent.findall('sat_turn'):
        parent.remove(element)
for parent in root2.findall('.//az_start/..'):
    for element in parent.findall('az_start'):
        parent.remove(element)
for parent in root2.findall('.//az_culm/..'):
    for element in parent.findall('az_culm'):
        parent.remove(element)
for parent in root2.findall('.//date_time_culm/..'):
    for element in parent.findall('date_time_culm'):
        parent.remove(element)
for parent in root2.findall('.//az_end/..'):
    for element in parent.findall('az_end'):
        parent.remove(element)

# надо добавить удаление лишних спутников

# добавление 3х часов к времени
temp = 0
date_time_st_rcurchs = time_zone_checker(date_time_start_array)
for el in root2.iter('date_time_start'):
    el.text = date_time_st_rcurchs[temp]
    temp += 1
temp = 0
date_time_end_rcurchs = time_zone_checker(date_time_end_array)
for el in root2.iter('date_time_end'):
    el.text = date_time_end_rcurchs[temp]
    temp += 1


tree2 = ET.ElementTree(root2)
tree2.write("sess_plan_rcurchs.xml")

print()


#print(time.strftime('%d.%m.%Y %H:%M:%S', struct))

# установка часового пояса
#print(time.strftime('%X %x %Z'))
#'12:45:20 08/19/09 CDT'
#os.environ['TZ'] = 'Europe/Minsk'
#time.tzset()
#print(time.strftime('%X %x %Z'))
#'18:45:39 08/19/09 BST'

print()

#print(time.strftime('%d.%m.%Y %H:%M:%S') == res[0])
#print(res_time_start)
#print(len(res_time_start))
#print(time.strftime('%d.%m.%Y %H:%M:%S'))
print(time_3m_before('16.01.2022 11:07:29'))
print()
#отсекаем прошедшее время, если есть
while time.strftime('%d.%m.%Y %H:%M:%S') > res_time_start[0]:
    res_time_start.pop(0)
#реакция на время и отсекание прошедшего пока не закончится список
print(res_time_start)
print()
while len(res_time_start) > 0:
    time_now = time.strftime('%d.%m.%Y %H:%M:%S')
    time_now1 = time.strftime('%d.%m.%Y %H:%M:%S')
    #print(res_time_start)
    #print()
    res_time_3m_before = list(map(time_3m_before, res_time_start.copy()))
    #print(res_time_3m_before)
    #print()
    if time_now == res_time_3m_before[0]:
        print("3 минуты до начала сеанса!")
        playsound('before_start.mp3')

    if time_now == res_time_start[0]:
        print("Сеанс начат")
        playsound('start.mp3')
        res_time_start.pop(0)
    print(time_now)
    time.sleep(1)

