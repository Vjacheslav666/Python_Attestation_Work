from Function_Files import print_menu as print_menu
from Function_Files import application_functions as application_functions

def main_menu():
    print('\n\033[32mВы находитесь в приложении "Заметки".\033[0m\n')
    print(print_menu.print_main_menu())
    application_functions.selection_function()