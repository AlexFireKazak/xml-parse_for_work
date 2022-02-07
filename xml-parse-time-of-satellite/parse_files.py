os.chdir('files')
dirname = 'files'
files = os.listdir()
true_files = [] # содержит только имена .xml
for el in files:
    if 'sess_plan.xml' in el:
        true_files.append(el)

print(true_files)

os.chdir('..')
date_time_start_array_all_files = []

# функция работы с одним .xml-файлом. проверяет витки и создает файл для мчс
def one_xml_work(name_file):
    tree = ET.parse(name_file)
    root = tree.getroot()
    date_time_end_array = []
    sat_turn_in = []
    date_time_start_array = []
    # Парсим содержисое тегов из .xml
    for el in root.findall('session'):
        t_start = el.find('date_time_start').text
        name = el.find('sat_name').text
        date_time_start_array.append(t_start)
        culm = el.find('el_culm').text
        t_end = el.find('date_time_end').text
        date_time_end_array.append(t_end)
        sat_turn_in.append(el.find('sat_turn').text)    
    # записываем правильные витки в файл
    temp = 0
    sat_turn_out = sat_turn_checker(sat_turn_in)
    for el in root.iter('sat_turn'):
        el.text = sat_turn_out[temp]
        temp += 1
    tree.write(name_file)

    date_time_start_array1 = date_time_start_array.copy()
    res_time_start = time_round_sec(date_time_start_array1)

    # создание xml-таблицы для мчс и запись в файл
    command_for_copy = 'cp '+ name_file + ' ' + name_file[:-4] + '_rcurchs' + '.xml'
    name_for_mchs = name_file[:-4] + 'rcurchs'+'.xml'
    os.system(command_for_copy) #создание копии файла(для винды заменить cp на copy)
    tree2 = ET.ElementTree(name_for_mchs)
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
    tree2.write(name_for_mchs)
    return res_time_start
####


for file in files:
    date_time_start_array_all_files += one_xml_work(file)
