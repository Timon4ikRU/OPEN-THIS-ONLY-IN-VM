import os
import sys
import datetime
import random
import time
import shutil
from cmd import Cmd
import builtins
import platform
import ctypes
import math
from colorama import init, Fore, Back, Style
import pyfiglet
import keyboard
import json
import socket
import subprocess
import re

init()

# Глобальные переменные для отслеживания режима запуска
FIRST_RUN_FILE = os.path.join(os.path.expanduser("~"), ".nexusos_first_run")
BOOTLOADER_MODE = False

# Проверяем, первый ли это запуск
if not os.path.exists(FIRST_RUN_FILE):
    # Первый запуск - создаем маркер
    with open(FIRST_RUN_FILE, 'w') as f:
        f.write('1')
    BOOTLOADER_MODE = False
else:
    # Последующие запуски - проверяем режим
    BOOTLOADER_MODE = True

version = "0.0.9 DevTest"
DATA_ROOT = os.path.join(os.path.expanduser("~"), "NexusOS_data")

LANGUAGES = {
    'ru': {
        'welcome': "Добро пожаловать в NexusOS!",
        'select_lang': "Выберите язык (ru/en): ",
        'invalid_lang': "Неверный выбор языка, используется английский по умолчанию.",
        'help_title': "Справка по командам",
        'help_page': "Страница {}",
        'help_next': "Следующая страница: HELP {}",
        'ver_title': "О системе",
        'ver_content': "NexusOS Версия {}\n\nНовые возможности в этой версии:\n- BIOS",
        'current_dir': "Текущий каталог: {}",
        'dir_title': "Содержимое каталога",
        'dir_content': "\n Содержимое каталога {}\n\n{:<12} {:<8} {:>10} {:>12}\n{}\n",
        'dir_footer': "\n Файлов: {}\n Каталогов: {}",
        'file_not_found': "Файл {} не найден!",
        'color_usage': "Использование:\n  COLOR #AABBCC  - HEX-цвет\n  COLOR RED      - именованные цвета (RED, GREEN, BLUE, WHITE)",
        'color_changed': "Цвет изменен на {}",
        'color_error': "Неверный цвет! Доступно:\n- HEX: #AABBCC или #ABC\n- Именованные: RED, GREEN, BLUE, WHITE",
        'calc_usage': "Использование: CALC <число> <операция> <число>\nДоступные операции: + - * /",
        'calc_result': "Результат: {}",
        'calc_error': "Ошибка: {}\nИспользование: CALC <число> <операция> <число>",
        'ttt_usage': "Использование: TICTACTOE START\nИли просто введите координаты (A1, B2 и т.д.)",
        'ttt_start': "Игра началась! Ходят крестики (X)\nВводите координаты (например: A1)",
        'ttt_invalid': "Неверный ход. Используйте формат A1, B2, C3 и т.д.",
        'ttt_taken': "Эта клетка уже занята!",
        'ttt_win': "Игрок {} победил!",
        'ttt_draw': "Ничья!",
        'ttt_turn': "Ход игрока {}",
        'cf_usage': "Использование: CF Имя_файла \"Содержимое\" Расширение\nПример для Python: CF SCRIPT \"print('Hello')\" PY\nСпецсимволы: /n - перенос строки, /t - табуляция\nДля записи кавычек внутри текста используйте \\\"\nФайл будет создан в: {}",
        'cf_created': "Файл создан: {}{}",
        'cf_exists': "Ошибка: Файл {} уже существует!",
        'cf_error': "Ошибка: {}\nПравильный формат: CF Имя \"Содержимое\" Расширение\nПример с кавычками: CF TEST \"print(\\\"Hello\\\")\" PY",
        'run_usage': "Использование: RUN Имя_файла.PY или RUN Имя_файла.BAT",
        'run_error': "Ошибка: Можно выполнять только .PY или .BAT файлы!",
        'type_usage': "Использование: TYPE Имя_файла\nПоказывает содержимое файла из текущей директории: {}",
        'type_error': "Ошибка: Файл {} не найден!",
        'type_binary': "Ошибка: Файл содержит бинарные данные и не может быть прочитан как текст!",
        'type_content': "Содержимое файла {}{}:\n{}\n{}\n{}\nРазмер: {} байт",
        'time_current': "Текущее время: {}",
        'time_set': "Время установлено (эмуляция)",
        'date_current': "Текущая дата: {}",
        'date_set': "Дата установлена (эмуляция)",
        'copy_success': "1 файл(ов) скопирован(о)",
        'del_success': "Файл удален:\n{}",
        'md_success': "Каталог создан:\n{}",
        'rd_success': "Каталог удален:\n{}",
        'bsod_title': "ПРОИЗОШЛА КРИТИЧЕСКАЯ ОШИБКА",
        'bsod_message': "NexusOS обнаружила проблему и будет перезагружена",
        'bsod_code': "Код ошибки: {}",
        'bsod_restart': "Нажмите Enter для перезагрузки...",
        'prompt': "{}> ",
        'boot': "Загрузка системы...",
        'intro': "NexusOS Версия {}\n© Тимофей Якубов 2025\n\nФайловая система: {}\nДля первого тестового запуска введите: RUN HELLO_WORLD.BAT\n\nВведите HELP для списка команд",
        'bios_title': "NexusOS BIOS",
        'bios_menu': (
            "1. Войти в BIOS\n"
            "2. Выйти\n"
            "3. Звук Вкл/Выкл\n"
            "4. Безопасный режим\n"
            "5. Сохранить и выйти\n"
            "6. Выйти без сохранения\n"
            "7. Выкл. безопасный режим\n"
            "8. Блокировка команд\n"
            "9. Быстрый BIOS"
        ),
        'bios_sound_on': "✓ Звук включен",
        'bios_sound_off': "✗ Звук выключен",
        'bios_safe_on': "✓ Безопасный режим (заблокированы RF, RD, RUN, DRVLOAD, DRVUNLOAD)",
        'bios_safe_off': "✗ Безопасный режим выключен",
        'bios_fast_on': "✓ Быстрый BIOS включен",
        'bios_fast_off': "✗ Быстрый BIOS выключен",
        'bios_block_prompt': "Введите команду для блокировки:",
        'bios_blocked': "➤ Команда '{}' заблокирована",
        'bios_saved': "✔ Настройки сохранены",
        'bios_invalid': "Неверный выбор",
        'press_for_bios': "Нажмите DEL для входа в BIOS",
        'system_loaded': "Система загружена",
        'command_blocked': "Команда '{}' заблокирована в безопасном режиме",
        'thanks_for_using': "Спасибо за использование NexusOS версии {}",
        'creating_root_dir': "Создаю корневую папку",
        'shutting_down': "Завершение работы",
        'startup_error': "Ошибка запуска",
        'ping_usage': "Использование: PING <хост> [кол-во пакетов]",
        'ping_result': "Ответ от {}: время={}мс TTL={}",
        'ping_timeout': "Превышен интервал ожидания для запроса.",
        'ping_error': "Ошибка ping: {}",
        'netstat_usage': "Использование: NETSTAT [-a]",
        'netstat_result': "Активные подключения:\n{}",
        'tracert_usage': "Использование: TRACERT <хост>",
        'tracert_result': "Трассировка маршрута к {}\n{}",
        'tracert_error': "Ошибка трассировки: {}",
        'drvinfo_title': "Информация о драйверах",
        'drvinfo_error': "Ошибка при получении информации о драйверах: {}"
    },
    'en': {
        'welcome': "Welcome to NexusOS!",
        'select_lang': "Choose language (ru/en): ",
        'invalid_lang': "Invalid language choice, using English by default.",
        'help_title': "Command Help",
        'help_page': "Page {}",
        'help_next': "Next page: HELP {}",
        'ver_title': "About System",
        'ver_content': "NexusOS Version {}\n\nNew features in this version:\n- BIOS",
        'current_dir': "Current directory: {}",
        'dir_title': "Directory Content",
        'dir_content': "\n Content of directory {}\n\n{:<12} {:<8} {:>10} {:>12}\n{}\n",
        'dir_footer': "\n Files: {}\n Directories: {}",
        'file_not_found': "File {} not found!",
        'color_usage': "Usage:\n  COLOR #AABBCC  - HEX color\n  COLOR RED      - named colors (RED, GREEN, BLUE, WHITE)",
        'color_changed': "Color changed to {}",
        'color_error': "Invalid color! Available:\n- HEX: #AABBCC or #ABC\n- Named: RED, GREEN, BLUE, WHITE",
        'calc_usage': "Usage: CALC <number> <operation> <number>\nAvailable operations: + - * /",
        'calc_result': "Result: {}",
        'calc_error': "Error: {}\nUsage: CALC <number> <operation> <number>",
        'ttt_usage': "Usage: TICTACTOE START\nOr just enter coordinates (A1, B2 etc.)",
        'ttt_start': "Game started! X's turn\nEnter coordinates (e.g. A1)",
        'ttt_invalid': "Invalid move. Use format A1, B2, C3 etc.",
        'ttt_taken': "This cell is already taken!",
        'ttt_win': "Player {} wins!",
        'ttt_draw': "Draw!",
        'ttt_turn': "Player {}'s turn",
        'cf_usage': "Usage: CF Filename \"Content\" Extension\nPython example: CF SCRIPT \"print('Hello')\" PY\nSpecial chars: /n - new line, /t - tab\nTo use quotes inside text use \\\"\nFile will be created in: {}",
        'cf_created': "File created: {}{}",
        'cf_exists': "Error: File {} already exists!",
        'cf_error': "Error: {}\nCorrect format: CF Name \"Content\" Extension\nExample with quotes: CF TEST \"print(\\\"Hello\\\")\" PY",
        'run_usage': "Usage: RUN Filename.PY or RUN Filename.BAT",
        'run_error': "Error: Only .PY or .BAT files can be executed!",
        'type_usage': "Usage: TYPE Filename\nShows file content from current directory: {}",
        'type_error': "Error: File {} not found!",
        'type_binary': "Error: File contains binary data and cannot be read as text!",
        'type_content': "Content of file {}{}:\n{}\n{}\n{}\nSize: {} bytes",
        'time_current': "Current time: {}",
        'time_set': "Time set (emulation)",
        'date_current': "Current date: {}",
        'date_set': "Date set (emulation)",
        'copy_success': "1 file(s) copied",
        'del_success': "File deleted:\n{}",
        'md_success': "Directory created:\n{}",
        'rd_success': "Directory deleted:\n{}",
        'bsod_title': "A CRITICAL ERROR OCCURRED",
        'bsod_message': "NexusOS has encountered a problem and will be restarted",
        'bsod_code': "Error code: {}",
        'bsod_restart': "Press Enter to restart...",
        'prompt': "{}> ",
        'boot': "Loading system...",
        'intro': "NexusOS Version {}\n© Timofey Yakubov 2025\n\nFile system: {}\nFor first test run enter: RUN HELLO_WORLD.BAT\n\nType HELP for command list",
        'bios_title': "NexusOS BIOS", 
        'bios_menu': (
            "1. Enter BIOS\n"
            "2. Exit\n"
            "3. Toggle sound\n"
            "4. Safe mode\n" 
            "5. Save and exit\n"
            "6. Exit without saving\n"
            "7. Disable safe mode\n"
            "8. Block commands\n"
            "9. Fast BIOS"
        ),
        'bios_sound_on': "✓ Sound enabled",
        'bios_sound_off': "✗ Sound disabled",
        'bios_safe_on': "✓ Safe mode (blocked RF, RD, RUN, DRVLOAD, DRVUNLOAD)",
        'bios_safe_off': "✗ Safe mode disabled",
        'bios_fast_on': "✓ Fast BIOS enabled",
        'bios_fast_off': "✗ Fast BIOS disabled",
        'bios_block_prompt': "Enter command to block:",
        'bios_blocked': "➤ Command '{}' blocked",
        'bios_saved': "✔ Settings saved",
        'bios_invalid': "Invalid option",
        'press_for_bios': "Press DEL to enter BIOS",
        'system_loaded': "System loaded",
        'command_blocked': "Command '{}' blocked in safe mode",
        'thanks_for_using': "Thank you for using NexusOS version {}",
        'creating_root_dir': "Creating root directory",
        'shutting_down': "Shutting down",
        'startup_error': "Startup error",
        'ping_usage': "Usage: PING <host> [packets count]",
        'ping_result': "Reply from {}: time={}ms TTL={}",
        'ping_timeout': "Request timed out.",
        'ping_error': "Ping error: {}",
        'netstat_usage': "Usage: NETSTAT [-a]",
        'netstat_result': "Active connections:\n{}",
        'tracert_usage': "Usage: TRACERT <host>",
        'tracert_result': "Tracing route to {}\n{}",
        'tracert_error': "Tracert error: {}",
        'drvinfo_title': "Drivers Information", 
        'drvinfo_error': "Error getting drivers info: {}"
    }
}

current_lang = 'en'

sound_enabled = False
if sys.platform == 'win32':
    try:
        import winsound
        sound_enabled = True
    except ImportError:
        sound_enabled = False

def is_idle():
    return 'idlelib.run' in sys.modules

def play_sound(frequency, duration):
    if not sound_enabled or is_idle():
        return
    try:
        winsound.Beep(frequency, int(duration * 1000))
    except:
        pass

def show_bsod(error_code="0x00000001"):
    try:
        play_sound(2000, 2.0)
        print("\n"*5)
        print(" "*20 + "="*60)
        print(" "*20 + f"|{LANGUAGES[current_lang]['bsod_title']:^58}|")
        print(" "*20 + f"|{LANGUAGES[current_lang]['bsod_message']:^58}|")
        print(" "*20 + f"| {LANGUAGES[current_lang]['bsod_code'].format(error_code):<45}|")
        print(" "*20 + f"| {LANGUAGES[current_lang]['bsod_restart']:^36} |")
        print(" "*20 + "="*60)
        print("\n"*5)
        input()
    except:
        pass
    finally:
        play_sound(300, 0.8)
        os.system('cls' if os.name == 'nt' else 'clear')
        main()

def draw_window(title, content, width=60, height=10):
    border_top = "╔" + "═" * (width - 2) + "╗"
    title_line = f"║ {Fore.CYAN}{title.center(width-3)}{Style.RESET_ALL}║"
    separator = "╟" + "─" * (width - 2) + "╢"
    
    content_lines = []
    for line in content.split('\n'):
        while len(line) > width-3:
            content_lines.append(line[:width-3])
            line = line[width-3:]
        content_lines.append(line)
    
    border_bottom = "╚" + "═" * (width - 2) + "╝"
    
    print(Fore.WHITE + Back.BLUE + border_top + Style.RESET_ALL)
    print(Fore.WHITE + Back.BLUE + title_line + Style.RESET_ALL)
    print(Fore.WHITE + Back.BLUE + separator + Style.RESET_ALL)
    
    for i in range(min(height, len(content_lines))):
        line = content_lines[i].ljust(width-3)
        print(Fore.WHITE + Back.BLUE + f"║ {line}║" + Style.RESET_ALL)
    
    for _ in range(height - len(content_lines)):
        print(Fore.WHITE + Back.BLUE + f"║ {' '*(width-3)}║" + Style.RESET_ALL)
    
    print(Fore.WHITE + Back.BLUE + border_bottom + Style.RESET_ALL)

def ensure_data_dir():
    os.makedirs(os.path.join(DATA_ROOT, "C", "WINDOWS", "SYSTEM"), exist_ok=True)
    os.makedirs(os.path.join(DATA_ROOT, "C", "DOS"), exist_ok=True)
    os.makedirs(os.path.join(DATA_ROOT, "C", "TEMP"), exist_ok=True)
    os.makedirs(os.path.join(DATA_ROOT, "C", "GAMES"), exist_ok=True)
    
    for path, content in [
        ("C\\AUTOEXEC.BAT", "@echo off"),
        ("C\\CONFIG.SYS", "DEVICE=C:\\DOS\\HIMEM.SYS"),
        ("C\\WINDOWS\\WIN.INI", "[windows]"),
        ("C\\DOS\\MEM.EXE", "MEM" * 1000),
        ("C\\HELLO_WORLD.BAT", 
         "@echo off\n"
         "echo ============================\n"
         "echo Привет, мир от NexusOS!\n"
         "echo Это демонстрационный BAT-файл\n"
         "echo ============================\n"
         "echo.\n"
         "echo Текущая дата: %date%\n"
         "echo Текущее время: %time%\n"
         "echo.\n"
         "echo Список файлов в текущей папке:\n"
         "dir\n"
         "pause\n"
         "cls\n"
         "echo Спасибо за использование NexusOS!\n"
         "pause")
   ]:
        full_path = os.path.join(DATA_ROOT, path)
        if not os.path.exists(full_path):
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

class NexusOS_BIOS:
    def __init__(self, os_instance):
        self.os = os_instance
        self.settings = {
            "sound": True,
            "safe_mode": False,
            "fast_boot": False,
            "blocked_commands": []
        }
        self.load_settings()

    def load_settings(self):
        try:
            with open(f"{DATA_ROOT}/bios_config.json", "r") as f:
                self.settings = json.load(f)
        except:
            self.save_settings()

    def save_settings(self):
        with open(f"{DATA_ROOT}/bios_config.json", "w") as f:
            json.dump(self.settings, f)

    def show_menu(self):
        self.os.do_CLS('')
        print(Fore.CYAN + "╔════════════════════════════╗")
        print(f"║{LANGUAGES[current_lang]['bios_title']:^28}║")
        print("╠════════════════════════════╣" + Style.RESET_ALL)
        print(LANGUAGES[current_lang]['bios_menu'] + "\n")

    def enter_bios(self):
        while True:
            self.show_menu()
            try:
                choice = input("Выберите пункт (1-9): ").strip()
                
                if choice == '1':
                    continue
                elif choice == '2':
                    break
                elif choice == '3':
                    self.settings['sound'] = not self.settings['sound']
                    print(Fore.GREEN + LANGUAGES[current_lang]['bios_sound_on'] if self.settings['sound'] 
                          else Fore.RED + LANGUAGES[current_lang]['bios_sound_off'])
                elif choice == '4':
                    self.settings['safe_mode'] = True
                    self.settings['blocked_commands'] = ["RF", "RD", "RUN", "DRVLOAD", "DRVUNLOAD"]
                    print(Fore.GREEN + LANGUAGES[current_lang]['bios_safe_on'])
                elif choice == '5':
                    self.save_settings()
                    print(Fore.GREEN + LANGUAGES[current_lang]['bios_saved'])
                    break
                elif choice == '6':
                    break
                elif choice == '7':
                    self.settings['safe_mode'] = False
                    self.settings['blocked_commands'] = []
                    print(Fore.RED + LANGUAGES[current_lang]['bios_safe_off'])
                elif choice == '8':
                    cmd = input(Fore.YELLOW + LANGUAGES[current_lang]['bios_block_prompt'] + " ").upper()
                    if cmd not in self.settings['blocked_commands']:
                        self.settings['blocked_commands'].append(cmd)
                        print(Fore.RED + LANGUAGES[current_lang]['bios_blocked'].format(cmd))
                elif choice == '9':
                    self.settings['fast_boot'] = not self.settings['fast_boot']
                    print(Fore.GREEN + LANGUAGES[current_lang]['bios_fast_on'] if self.settings['fast_boot'] 
                          else Fore.RED + LANGUAGES[current_lang]['bios_fast_off'])
                else:
                    print(Fore.RED + LANGUAGES[current_lang]['bios_invalid'])
                
                time.sleep(0.5)
            except Exception as e:
                print(f"Error: {e}")
                break

class NexusOS(Cmd):
    def __init__(self):
        super().__init__()
        self.current_dir = "C:\\"
        self.bios = NexusOS_BIOS(self)
        self.update_prompt()
        self.tictactoe_board = None
        self.tictactoe_turn = 'X'
        self.boot_screen()
        ensure_data_dir()
        self.intro = self.get_intro()
    
    def boot_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        try:
            logo = pyfiglet.figlet_format("NexusOS", font="small")
            print(Fore.BLUE + logo + Style.RESET_ALL)
        except:
            print(Fore.BLUE + "NexusOS" + Style.RESET_ALL)
            print("=" * 40)
        
        print(Fore.CYAN + LANGUAGES[current_lang]['boot'] + Style.RESET_ALL)
        for i in range(1, 101):
            time.sleep(0.01)
            bar = "[" + "█" * (i//2) + " " * (50 - i//2) + "]"
            print(f"\r{Fore.YELLOW}{bar}{Style.RESET_ALL} {i}%", end='', flush=True)
        
        play_sound(300, 0.8)
        print("\n\n")
        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_intro(self):
        intro_text = LANGUAGES[current_lang]['intro'].format(version, DATA_ROOT)
        return f"""
{Fore.CYAN}╔══════════════════════════════════════════════════╗
║{Fore.WHITE}{'NexusOS ' + ('Версия' if current_lang == 'ru' else 'Version') + ' ' + version:^50}{Fore.CYAN}║
║{Fore.WHITE}{'© Тимофей Якубов 2025' if current_lang == 'ru' else '© Timofey Yakubov 2025':^50}{Fore.CYAN}║
╚══════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}{'Файловая система' if current_lang == 'ru' else 'File system'}: {DATA_ROOT}{Style.RESET_ALL}
{Fore.GREEN}{'Для первого тестового запуска введите' if current_lang == 'ru' else 'For first test run enter'}: RUN HELLO_WORLD.BAT{Style.RESET_ALL}

{Fore.WHITE}{'Введите' if current_lang == 'ru' else 'Type'} {Fore.CYAN}HELP{Fore.WHITE} {'для списка команд' if current_lang == 'ru' else 'for command list'}{Style.RESET_ALL}
"""
    
    def update_prompt(self):
        self.prompt = f"{Fore.BLUE}{self.current_dir}{Style.RESET_ALL}{Fore.CYAN}>{Style.RESET_ALL} "
    
    def boot(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.YELLOW + LANGUAGES[current_lang]['press_for_bios'] + Style.RESET_ALL)
        time.sleep(1)
        
        try:
            if keyboard.is_pressed('!'):
                self.bios.enter_bios()
        except:
            pass

        print(Fore.GREEN + LANGUAGES[current_lang]['system_loaded'] + Style.RESET_ALL)
    
    def do_BIOS(self, arg):
        self.bios.enter_bios()

    def emptyline(self):
        pass
    
    def precmd(self, line):
        if not line:
            return line
            
        if self.tictactoe_board and len(line) == 2 and line[0].upper() in 'ABC' and line[1] in '123':
            return f"TICTACTOE {line}"
            
        parts = line.split(maxsplit=1)
        cmd = parts[0].upper()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd in self.bios.settings['blocked_commands']:
            print(Fore.RED + LANGUAGES[current_lang]['command_blocked'].format(cmd) + Style.RESET_ALL)
            return ""
        
        return f"{cmd} {args}".strip()

    def do_COLOR(self, arg):
        self.do_CLS('')
        content = ""
        if not arg:
            content = LANGUAGES[current_lang]['color_usage']
            draw_window("Смена цвета текста", content)
            return
        
        arg = arg.upper().strip()
        
        if arg.startswith('#'):
            hex_color = arg[1:]
            
            if len(hex_color) not in (3, 6):
                content = "Ошибка: HEX-цвет должен быть в формате #ABC или #AABBCC"
                draw_window("Ошибка смены цвета", content)
                return
                
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            
            try:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                
                print(f"\033[38;2;{r};{g};{b}m")
                content = LANGUAGES[current_lang]['color_changed'].format(f"HEX #{hex_color}")
                draw_window("Смена цвета текста", content)
            except ValueError:
                content = "Ошибка: неверный HEX-формат"
                draw_window("Ошибка смены цвета", content)
            return
        
        color_map = {
            'RED': '\033[91m',
            'GREEN': '\033[92m',
            'BLUE': '\033[94m',
            'WHITE': '\033[0m',
        }
        
        if arg in color_map:
            print(color_map[arg], end='')
            content = LANGUAGES[current_lang]['color_changed'].format(arg)
            draw_window("Смена цвета текста", content)
        else:
            content = LANGUAGES[current_lang]['color_error']
            draw_window("Ошибка смены цвета", content)
            
    def do_VER(self, arg):
        self.do_CLS('')
        content = LANGUAGES[current_lang]['ver_content'].format(version)
        draw_window(LANGUAGES[current_lang]['ver_title'], content)
    
    def do_CLS(self, arg):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.get_intro())
    
    def do_DIR(self, arg):
        self.do_CLS('')
        target_path = os.path.join(self.current_dir, arg) if arg else self.current_dir
        target_path = target_path.replace("/", "\\")
        
        if not target_path.endswith("\\"):
            target_path += "\\"
        
        real_path = os.path.join(DATA_ROOT, "C", target_path[3:])
        
        if not os.path.isdir(real_path):
            show_bsod("0x00000024")
            return
        
        content = LANGUAGES[current_lang]['dir_content'].format(
            target_path,
            'Name' if current_lang == 'en' else 'Имя',
            'Type' if current_lang == 'en' else 'Тип',
            'Size' if current_lang == 'en' else 'Размер',
            'Date' if current_lang == 'en' else 'Дата',
            Fore.YELLOW + "-" * 45 + Style.RESET_ALL
        )
        
        total_files = 0
        total_dirs = 0
        
        try:
            for entry in os.listdir(real_path):
                full_path = os.path.join(real_path, entry)
                if os.path.isdir(full_path):
                    content += f"{Fore.RED}{entry:<12}{Style.RESET_ALL} {'<DIR>':<8} {'':>10} {datetime.date.fromtimestamp(os.path.getmtime(full_path)).strftime('%d-%m-%y'):>12}\n"
                    total_dirs += 1
                else:
                    size = os.path.getsize(full_path)
                    content += f"{Fore.GREEN}{entry:<12}{Style.RESET_ALL} {'File' if current_lang == 'en' else 'Файл':<8} {size:>10} {datetime.date.fromtimestamp(os.path.getmtime(full_path)).strftime('%d-%m-%y'):>12}\n"
                    total_files += 1
        except Exception as e:
            show_bsod("0x00000025")
            return
        
        content += LANGUAGES[current_lang]['dir_footer'].format(total_files, total_dirs)
        draw_window(LANGUAGES[current_lang]['dir_title'], content)
    
    def do_CD(self, arg):
        self.do_CLS('')
        if not arg:
            content = LANGUAGES[current_lang]['current_dir'].format(self.current_dir)
            draw_window("Текущая директория", content)
            return
        
        new_path = os.path.join(self.current_dir, arg)
        new_path = new_path.replace("/", "\\")
        
        if arg == "\\":
            new_path = "C:\\"
        elif arg == "..":
            if self.current_dir == "C:\\":
                content = "Уже в корневом каталоге" if current_lang == 'ru' else "Already at root directory"
                draw_window("Смена директории", content)
                return
            parts = self.current_dir.split("\\")
            new_path = "\\".join(parts[:-2]) + "\\"
        
        if not new_path.endswith("\\"):
            new_path += "\\"
        
        real_path = os.path.join(DATA_ROOT, "C", new_path[3:])
        if os.path.isdir(real_path):
            self.current_dir = new_path
            self.update_prompt()
            content = f"Текущая директория изменена на:\n{self.current_dir}" if current_lang == 'ru' else f"Current directory changed to:\n{self.current_dir}"
            draw_window("Смена директории", content)
        else:
            show_bsod("0x00000003")
    
    def do_MD(self, arg):
        self.do_CLS('')
        if not arg:
            show_bsod("0x0000001E")
            return
        
        new_dir = os.path.join(self.current_dir, arg)
        new_dir = new_dir.replace("/", "\\")
        
        if not new_dir.endswith("\\"):
            new_dir += "\\"
        
        real_path = os.path.join(DATA_ROOT, "C", new_dir[3:])
        if os.path.exists(real_path):
            content = "Каталог уже существует" if current_lang == 'ru' else "Directory already exists"
            draw_window("Ошибка создания", content)
        else:
            try:
                os.makedirs(real_path)
                content = LANGUAGES[current_lang]['md_success'].format(new_dir)
                draw_window("Создание каталога", content)
            except:
                show_bsod("0x0000001F")
    
    def do_RD(self, arg):
        self.do_CLS('')
        if not arg:
            show_bsod("0x0000002A")
            return
        
        target_dir = os.path.join(self.current_dir, arg)
        target_dir = target_dir.replace("/", "\\")
        
        if not target_dir.endswith("\\"):
            target_dir += "\\"
        
        real_path = os.path.join(DATA_ROOT, "C", target_dir[3:])
        if not os.path.isdir(real_path):
            content = "Каталог не найден" if current_lang == 'ru' else "Directory not found"
            draw_window("Ошибка удаления", content)
        else:
            try:
                shutil.rmtree(real_path)
                content = LANGUAGES[current_lang]['rd_success'].format(target_dir)
                draw_window("Удаление каталога", content)
            except:
                show_bsod("0x0000002B")
    
    def do_DEL(self, arg):
        self.do_CLS('')
        if not arg:
            show_bsod("0x00000020")
            return
        
        target_file = os.path.join(self.current_dir, arg)
        target_file = target_file.replace("/", "\\")
        
        real_path = os.path.join(DATA_ROOT, "C", target_file[3:])
        if not os.path.isfile(real_path):
            content = "Файл не найден" if current_lang == 'ru' else "File not found"
            draw_window("Ошибка удаления", content)
        else:
            try:
                os.remove(real_path)
                content = LANGUAGES[current_lang]['del_success'].format(target_file)
                draw_window("Удаление файла", content)
            except:
                show_bsod("0x00000021")
    
    def do_COPY(self, arg):
        self.do_CLS('')
        if not arg:
            show_bsod("0x00000022")
            return
        
        parts = arg.split()
        if len(parts) != 2:
            show_bsod("0x00000023")
            return
        
        src_file = os.path.join(self.current_dir, parts[0])
        dst_file = os.path.join(self.current_dir, parts[1])
        
        src_file = src_file.replace("/", "\\")
        dst_file = dst_file.replace("/", "\\")
        
        real_src = os.path.join(DATA_ROOT, "C", src_file[3:])
        real_dst = os.path.join(DATA_ROOT, "C", dst_file[3:])
        
        if not os.path.isfile(real_src):
            content = "Исходный файл не найден" if current_lang == 'ru' else "Source file not found"
            draw_window("Ошибка копирования", content)
        else:
            try:
                shutil.copy2(real_src, real_dst)
                content = LANGUAGES[current_lang]['copy_success']
                draw_window("Копирование файла", content)
            except:
                show_bsod("0x00000024")
    
    def do_TYPE(self, arg):
        self.do_CLS('')
        if not arg:
            content = LANGUAGES[current_lang]['type_usage'].format(self.current_dir)
            draw_window("Просмотр файла", content)
            return
        
        target_file = os.path.join(self.current_dir, arg)
        target_file = target_file.replace("/", "\\")
        
        real_path = os.path.join(DATA_ROOT, "C", target_file[3:])
        if not os.path.isfile(real_path):
            content = LANGUAGES[current_lang]['type_error'].format(target_file)
            draw_window("Ошибка", content)
        else:
            try:
                with open(real_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                size = os.path.getsize(real_path)
                lines = file_content.split('\n')
                first_lines = '\n'.join(lines[:5])
                last_lines = '\n'.join(lines[-5:]) if len(lines) > 10 else ""
                
                content = LANGUAGES[current_lang]['type_content'].format(
                    target_file,
                    f" ({len(lines)} строк)" if current_lang == 'ru' else f" ({len(lines)} lines)",
                    first_lines,
                    "\n..." if len(lines) > 10 else "",
                    last_lines,
                    size
                )
                draw_window("Содержимое файла", content)
            except UnicodeDecodeError:
                content = LANGUAGES[current_lang]['type_binary']
                draw_window("Ошибка", content)
            except Exception as e:
                show_bsod("0x00000026")
    
    def do_CF(self, arg):
        self.do_CLS('')
        if not arg:
            content = LANGUAGES[current_lang]['cf_usage'].format(self.current_dir)
            draw_window("Создание файла", content)
            return
        
        try:
            parts = arg.split(maxsplit=2)
            if len(parts) < 3:
                raise ValueError("Недостаточно аргументов")
            
            filename = parts[0]
            content_part = parts[1]
            extension = parts[2]
            
            if not content_part.startswith('"') or not content_part.endswith('"'):
                raise ValueError("Содержимое должно быть в кавычках")
            
            content_text = content_part[1:-1]
            content_text = content_text.replace('/n', '\n').replace('/t', '\t')
            
            target_file = os.path.join(self.current_dir, f"{filename}.{extension}")
            target_file = target_file.replace("/", "\\")
            
            real_path = os.path.join(DATA_ROOT, "C", target_file[3:])
            
            if os.path.exists(real_path):
                content = LANGUAGES[current_lang]['cf_exists'].format(target_file)
                draw_window("Ошибка создания", content)
                return
            
            with open(real_path, 'w', encoding='utf-8') as f:
                f.write(content_text)
            
            content = LANGUAGES[current_lang]['cf_created'].format(target_file, f" ({len(content_text)} символов)" if current_lang == 'ru' else f" ({len(content_text)} chars)")
            draw_window("Файл создан", content)
            
        except Exception as e:
            content = LANGUAGES[current_lang]['cf_error'].format(str(e))
            draw_window("Ошибка создания", content)
    
    def do_RUN(self, arg):
        self.do_CLS('')
        if not arg:
            content = LANGUAGES[current_lang]['run_usage']
            draw_window("Запуск файла", content)
            return
        
        target_file = os.path.join(self.current_dir, arg)
        target_file = target_file.replace("/", "\\")
        
        real_path = os.path.join(DATA_ROOT, "C", target_file[3:])
        
        if not os.path.isfile(real_path):
            content = LANGUAGES[current_lang]['file_not_found'].format(target_file)
            draw_window("Ошибка запуска", content)
            return
        
        if not arg.upper().endswith(('.PY', '.BAT')):
            content = LANGUAGES[current_lang]['run_error']
            draw_window("Ошибка запуска", content)
            return
        
        try:
            if arg.upper().endswith('.PY'):
                result = subprocess.run([sys.executable, real_path], 
                                      capture_output=True, text=True, cwd=os.path.dirname(real_path))
                content = result.stdout
                if result.stderr:
                    content += f"\n{Fore.RED}Ошибка:{Style.RESET_ALL}\n{result.stderr}"
            
            elif arg.upper().endswith('.BAT'):
                if os.name == 'nt':
                    result = subprocess.run([real_path], 
                                          capture_output=True, text=True, shell=True,
                                          cwd=os.path.dirname(real_path))
                    content = result.stdout
                    if result.stderr:
                        content += f"\n{Fore.RED}Ошибка:{Style.RESET_ALL}\n{result.stderr}"
                else:
                    content = "BAT файлы поддерживаются только на Windows"
            
            draw_window(f"Запуск {arg}", content)
            
        except Exception as e:
            content = f"Ошибка выполнения: {str(e)}"
            draw_window("Ошибка запуска", content)
    
    def do_CALC(self, arg):
        self.do_CLS('')
        if not arg:
            content = LANGUAGES[current_lang]['calc_usage']
            draw_window("Калькулятор", content)
            return
        
        try:
            parts = arg.split()
            if len(parts) != 3:
                raise ValueError("Неверное количество аргументов")
            
            num1 = float(parts[0])
            op = parts[1]
            num2 = float(parts[2])
            
            operations = {
                '+': lambda x, y: x + y,
                '-': lambda x, y: x - y,
                '*': lambda x, y: x * y,
                '/': lambda x, y: x / y if y != 0 else "Деление на ноль"
            }
            
            if op not in operations:
                raise ValueError("Неверная операция")
            
            result = operations[op](num1, num2)
            content = LANGUAGES[current_lang]['calc_result'].format(result)
            draw_window("Результат вычисления", content)
            
        except Exception as e:
            content = LANGUAGES[current_lang]['calc_error'].format(str(e))
            draw_window("Ошибка вычисления", content)
    
    def do_TICTACTOE(self, arg):
        self.do_CLS('')
        
        if not self.tictactoe_board:
            if arg.upper() != 'START':
                content = LANGUAGES[current_lang]['ttt_usage']
                draw_window("Крестики-нолики", content)
                return
            
            self.tictactoe_board = [[' ' for _ in range(3)] for _ in range(3)]
            self.tictactoe_turn = 'X'
            content = LANGUAGES[current_lang]['ttt_start']
            draw_window("Крестики-нолики", content)
            self.print_board()
            return
        
        if not arg:
            self.print_board()
            return
        
        if len(arg) != 2:
            content = LANGUAGES[current_lang]['ttt_invalid']
            draw_window("Ошибка хода", content)
            self.print_board()
            return
        
        col = arg[0].upper()
        row = arg[1]
        
        if col not in 'ABC' or row not in '123':
            content = LANGUAGES[current_lang]['ttt_invalid']
            draw_window("Ошибка хода", content)
            self.print_board()
            return
        
        x = ord(col) - ord('A')
        y = int(row) - 1
        
        if self.tictactoe_board[y][x] != ' ':
            content = LANGUAGES[current_lang]['ttt_taken']
            draw_window("Ошибка хода", content)
            self.print_board()
            return
        
        self.tictactoe_board[y][x] = self.tictactoe_turn
        self.print_board()
        
        if self.check_win():
            content = LANGUAGES[current_lang]['ttt_win'].format(self.tictactoe_turn)
            draw_window("Победа!", content)
            self.tictactoe_board = None
            return
        
        if self.check_draw():
            content = LANGUAGES[current_lang]['ttt_draw']
            draw_window("Ничья!", content)
            self.tictactoe_board = None
            return
        
        self.tictactoe_turn = 'O' if self.tictactoe_turn == 'X' else 'X'
        content = LANGUAGES[current_lang]['ttt_turn'].format(self.tictactoe_turn)
        draw_window("Ход игры", content)
    
    def print_board(self):
        board = "   A   B   C\n"
        for i, row in enumerate(self.tictactoe_board):
            board += f"{i+1}  {row[0]} | {row[1]} | {row[2]}\n"
            if i < 2:
                board += "  ---+---+---\n"
        print(board)
    
    def check_win(self):
        board = self.tictactoe_board
        
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != ' ':
                return True
            if board[0][i] == board[1][i] == board[2][i] != ' ':
                return True
        
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return True
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return True
        
        return False
    
    def check_draw(self):
        for row in self.tictactoe_board:
            if ' ' in row:
                return False
        return True
    
    def do_TIME(self, arg):
        self.do_CLS('')
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        content = LANGUAGES[current_lang]['time_current'].format(current_time)
        draw_window("Текущее время", content)
    
    def do_DATE(self, arg):
        self.do_CLS('')
        current_date = datetime.datetime.now().strftime("%d.%m.%Y")
        content = LANGUAGES[current_lang]['date_current'].format(current_date)
        draw_window("Текущая дата", content)
    
    def do_HELP(self, arg):
        self.do_CLS('')
        help_pages = {
            1: [
                "DIR [путь] - показать содержимое каталога",
                "CD [путь] - сменить каталог",
                "MD имя - создать каталог",
                "RD имя - удалить каталог",
                "DEL имя - удалить файл",
                "COPY исходный целевой - копировать файл"
            ],
            2: [
                "TYPE имя - показать содержимое файла",
                "CF имя \"текст\" расширение - создать файл",
                "RUN имя.расширение - запустить файл",
                "CALC число операция число - калькулятор",
                "TICTACTOE START - игра в крестики-нолики"
            ],
            3: [
                "COLOR [цвет] - изменить цвет текста",
                "TIME - показать текущее время",
                "DATE - показать текущую дату",
                "VER - информация о версии",
                "CLS - очистить экран",
                "EXIT - выход из системы"
            ],
            4: [
                "PING хост [кол-во] - проверить соединение",
                "NETSTAT [-a] - показать сетевые подключения",
                "TRACERT хост - трассировка маршрута",
                "DRVINFO - информация о драйверах",
                "BIOS - вход в настройки BIOS"
            ]
        }
        
        page = 1
        if arg:
            try:
                page = int(arg)
                if page not in help_pages:
                    page = 1
            except:
                page = 1
        
        title = f"{LANGUAGES[current_lang]['help_title']} - {LANGUAGES[current_lang]['help_page'].format(page)}"
        content = "\n".join(help_pages[page])
        
        if page < len(help_pages):
            content += f"\n\n{LANGUAGES[current_lang]['help_next'].format(page + 1)}"
        
        draw_window(title, content)
    
    def do_EXIT(self, arg):
        print(Fore.YELLOW + LANGUAGES[current_lang]['thanks_for_using'].format(version) + Style.RESET_ALL)
        play_sound(300, 0.8)
        return True

    def do_PING(self, arg):
        self.do_CLS('')
        if not arg:
            content = LANGUAGES[current_lang]['ping_usage']
            draw_window("PING", content)
            return
        
        parts = arg.split()
        host = parts[0]
        count = 4
        if len(parts) > 1:
            try:
                count = int(parts[1])
            except:
                pass
        
        try:
            content = f"Обмен пакетами с {host}:\n\n"
            for i in range(count):
                try:
                    start_time = time.time()
                    result = subprocess.run(['ping', '-n', '1', '-w', '1000', host], 
                                          capture_output=True, text=True)
                    end_time = time.time()
                    
                    if result.returncode == 0:
                        match = re.search(r'время=(\d+)мс', result.stdout)
                        if match:
                            ping_time = match.group(1)
                        else:
                            ping_time = int((end_time - start_time) * 1000)
                        
                        ttl_match = re.search(r'TTL=(\d+)', result.stdout)
                        ttl = ttl_match.group(1) if ttl_match else "64"
                        
                        content += LANGUAGES[current_lang]['ping_result'].format(host, ping_time, ttl) + "\n"
                    else:
                        content += LANGUAGES[current_lang]['ping_timeout'] + "\n"
                    
                    time.sleep(1)
                    
                except Exception as e:
                    content += f"Ошибка: {str(e)}\n"
                    break
            
            draw_window("PING Результат", content)
            
        except Exception as e:
            content = LANGUAGES[current_lang]['ping_error'].format(str(e))
            draw_window("PING Ошибка", content)

    def do_NETSTAT(self, arg):
        self.do_CLS('')
        try:
            result = subprocess.run(['netstat', '-a'] if arg == '-a' else ['netstat'], 
                                  capture_output=True, text=True)
            content = LANGUAGES[current_lang]['netstat_result'].format(result.stdout)
            draw_window("NETSTAT", content)
        except Exception as e:
            content = f"Ошибка: {str(e)}"
            draw_window("NETSTAT Ошибка", content)

    def do_TRACERT(self, arg):
        self.do_CLS('')
        if not arg:
            content = LANGUAGES[current_lang]['tracert_usage']
            draw_window("TRACERT", content)
            return
        
        try:
            result = subprocess.run(['tracert', arg], capture_output=True, text=True)
            content = LANGUAGES[current_lang]['tracert_result'].format(arg, result.stdout)
            draw_window("TRACERT Результат", content)
        except Exception as e:
            content = LANGUAGES[current_lang]['tracert_error'].format(str(e))
            draw_window("TRACERT Ошибка", content)

    def do_DRVINFO(self, arg):
        self.do_CLS('')
        try:
            if os.name == 'nt':
                result = subprocess.run(['driverquery'], capture_output=True, text=True)
                content = LANGUAGES[current_lang]['drvinfo_title'] + ":\n\n" + result.stdout
            else:
                content = "Эта команда доступна только на Windows"
            
            draw_window("DRVINFO", content)
        except Exception as e:
            content = LANGUAGES[current_lang]['drvinfo_error'].format(str(e))
            draw_window("DRVINFO Ошибка", content)

def main():
    global current_lang
    
    if not BOOTLOADER_MODE:
        print(Fore.CYAN + LANGUAGES['ru']['welcome'] + Style.RESET_ALL)
        lang_choice = input(LANGUAGES['ru']['select_lang']).lower().strip()
        current_lang = 'ru' if lang_choice == 'ru' else 'en'
        
        if lang_choice not in ['ru', 'en']:
            print(Fore.YELLOW + LANGUAGES[current_lang]['invalid_lang'] + Style.RESET_ALL)
    
    print(Fore.GREEN + LANGUAGES[current_lang]['creating_root_dir'] + Style.RESET_ALL)
    ensure_data_dir()
    
    os_instance = NexusOS()
    
    if BOOTLOADER_MODE:
        os_instance.boot()
    
    try:
        os_instance.cmdloop()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n" + LANGUAGES[current_lang]['shutting_down'] + Style.RESET_ALL)
        play_sound(300, 0.8)
    except Exception as e:
        print(Fore.RED + LANGUAGES[current_lang]['startup_error'] + f": {e}" + Style.RESET_ALL)
        play_sound(2000, 2.0)

if __name__ == "__main__":
    main()
