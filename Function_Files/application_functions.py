from Function_Files import print_menu as print_menu
import time
import csv
from tabulate import tabulate
from datetime import datetime

def selection_function():
    user_selection = int(input("\033[36mВыберите необходимый вам вариант: \033[0m"))
    print(f"\nВы выбрали {user_selection} вариант!\n")
    if user_selection == 1:
        print("\033[33mСписок всех заметок: \n\033[0m")
        open_all_notes()
        selection_function()

    elif user_selection == 2:
        title, body = print_menu.adding_notes1()
        adding_notes2(title, body)
        selection_function()

    elif user_selection == 3:
        with open("notes.csv", "r", encoding='UTF-8') as file:
            result = edit_note(file)
            if result is not None:
                id, title, body = result
                editing_notes(id, title, body)
            open_all_notes()
        selection_function()

    elif user_selection == 4:
        date = addition_date_selection()
        result = selection_of_notes_by_date(date)
        print_menu.display_notes(result)
        selection_function()

    elif user_selection == 5:
        with open("notes.csv", "r", encoding='UTF-8') as file:
            id_to_delete = ask_delete_note(file)
            delete_note(id_to_delete)
            open_all_notes()
        selection_function()

    elif user_selection == 6:
        print(print_menu.print_main_menu())
        selection_function()

    elif user_selection == 7:
        print('Вы покидаете приложении "Заметки".\n')
        exit()

    else:
        print("\033[31mВы ввели неправильные данные, повторите попытку ввода!\033[0m\n")
        selection_function()



# Функция добавления заметок
def adding_notes2(title, body):
    id = get_next_id()
    creation_time = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    with open("notes.csv", "a", encoding='UTF-8', newline='') as file:
        saving_data = csv.writer(file, delimiter=';')
        saving_data.writerow([id, title, body, creation_time, ''])



# Функция открытия всех заметок
def open_all_notes():
    notes = []
    with open('notes.csv', 'r', encoding='UTF-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            try:
                title = row[1][:30] + '\n' + \
                    row[1][30:] if len(row[1]) > 30 else row[1]
                body = row[2][:30] + '\n' + \
                    row[2][30:] if len(row[2]) > 30 else row[2]
                creation_time = row[3] if row[3] else ''
                change_time = row[4] if row[4] else ''
                notes.append([row[0], title, body, creation_time, change_time])
            except IndexError:
                notes.append(['', '', '', '', ''])
    print(tabulate(notes, headers=['\033[91mID\033[0m', '\033[91mЗаголовок\033[0m', '\033[91mОписание заметки\033[0m',
          '\033[91mДата/время создания\033[0m', '\033[91mДата/время изменения\033[0m'], tablefmt="fancy_grid", stralign="center"))



#Функция получения ID (следующего относительно последнего)
def get_next_id():
    with open("notes.csv", "r", encoding='UTF-8') as file:
        reader = csv.reader(file, delimiter=';')
        ids = [int(row[0].replace('.', '')) for row in reader if row]
        return max(ids) + 1 if ids else 1



#Функция редактирования заметки 
def edit_note(file):
    print("\033[33mРедактировать заметку: \033[0m")
    try:
        id = int(input("\n\033[36mВведите ID заметки, которую вы хотите изменить: \033[0m"))
    except ValueError:
        print("\033[31mНеверный ввод. Пожалуйста, введите число!!!\033[0m")
        return None
    
    notes = []
    reader = csv.reader(file, delimiter=";")
    for row in reader:
        notes.append(row)
      
    title = None
    body = None
    if id not in [int(note[0]) for note in notes]:
        print("\033[31mНеверный ID. Такая заметка отсутствует в списке!!!\033[0m")
        return None
    else:
        notes = [note for note in notes if int(note[0]) != id]
        title = input("\n\033[36mВведите новый заголовок заметки (можно оставить незаполненным): \033[0m") or None
        body = input("\033[36mВведите новое описание заметки (можно оставить незаполненным): \033[0m") or None
        print("\n\033[35mЗаметка отредактирована!!! \033[0m")
    return id, title, body



# Функция редактирования заметок
def editing_notes(id, title, body):
    notes = []
    with open("notes.csv", "r", encoding='UTF-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if int(row[0]) == id:
              if title is not None:
                row[1] = title
              if body is not None:
                row[2] = body
              row[4] = time.ctime()
            notes.append(row)
    
    with open("notes.csv", "w", encoding='UTF-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(notes)



#Функция удаления заметки
def ask_delete_note(file):
    print("\033[33mУдалить заметку: \033[0m")
    try:
        id_to_delete = int(input("\n\033[36mВведите ID заметки, которую вы хотите удалить: \033[0m"))
    except ValueError:
        print("\033[31mНеверный ввод. Пожалуйста, введите число!!!\033[0m")
        return None

    notes = []
    reader = csv.reader(file, delimiter=";")
    for row in reader:
        notes.append(row)

    if id_to_delete not in [int(note[0]) for note in notes]:
        print("\033[31mНеверный ID. Такая заметка отсутствует в списке!!!\033[0m")
    else:
        notes = [note for note in notes if int(note[0]) != id_to_delete]
        print("\033[35mЗаметка успешно удалена!!!\033[0m")
    return id_to_delete



# Функция удаления заметок
def delete_note(id_to_delete):
    notes = []
    with open("notes.csv", "r", encoding='UTF-8') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if int(row[0]) != id_to_delete:
                notes.append(row)
    with open("notes.csv", "w", encoding='UTF-8', newline='') as file:
        saving_data = csv.writer(file, delimiter=";")
        saving_data.writerows(notes)



#Функция ввода даты для поиска заметок
def addition_date_selection():
    print("\033[33mВыбор заметок по дате добавления: \033[0m")
    date_selection = input("\n\033[36mВведите дату для поиска, формат ввода (дд.мм.гггг): \033[0m")
    return date_selection



# Функция выборки заметок по дате добавления
def selection_of_notes_by_date(date):
  result = []
  with open("notes.csv", "r", encoding='UTF-8') as file:
    reader = csv.reader(file, delimiter=";")
    for row in reader:
      add_date = datetime.strptime(row[3], '%a %b %d %H:%M:%S %Y')
      if add_date.strftime("%d.%m.%Y") == date:
        result.append(row)
  return result
