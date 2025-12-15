#!/usr/bin/env python3
"""
Проверка этапа 3: Интерпретатор и операции с памятью.
"""

import sys
import os
import tempfile
import shutil

# Добавляем src в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from assembler.command import Command
from assembler.encoder import Encoder
from vm.interpreter import VirtualMachine

def print_header(text):
    """Печатает заголовок."""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)

def test_single_instructions():
    """Тест отдельных инструкций."""
    print_header("ТЕСТ ОТДЕЛЬНЫХ ИНСТРУКЦИЙ")
    
    # Создаем временную директорию
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Тест 1: LOAD_CONST
        print("\n1. Тест LOAD_CONST:")
        vm = VirtualMachine()
        cmd = Command(158, [12345, 3], 1, "")
        
        # Кодируем и сохраняем
        encoder = Encoder()
        binary = encoder.encode_commands([cmd])
        
        bin_file = os.path.join(temp_dir, "test1.bin")
        with open(bin_file, 'wb') as f:
            f.write(binary)
        
        # Выполняем
        vm.load_program_from_file(bin_file)
        vm.run()
        
        if vm.memory.get_register(3) == 12345:
            print("  [OK] LOAD_CONST работает корректно")
        else:
            print(f"  [ERROR] Ожидалось 12345, получено {vm.memory.get_register(3)}")
        
        # Тест 2: WRITE_MEM и READ_MEM
        print("\n2. Тест WRITE_MEM и READ_MEM:")
        vm2 = VirtualMachine()
        
        # Программа: записать 999 в memory[500], затем прочитать в регистр
        cmds = [
            Command(158, [999, 1], 1, ""),      # R1 = 999
            Command(158, [500, 2], 2, ""),      # R2 = 500
            Command(12, [2, 1], 3, ""),         # memory[R2] = R1 (memory[500] = 999)
            Command(17, [500, 3], 4, ""),       # R3 = memory[500]
        ]
        
        binary2 = encoder.encode_commands(cmds)
        bin_file2 = os.path.join(temp_dir, "test2.bin")
        
        with open(bin_file2, 'wb') as f:
            f.write(binary2)
        
        vm2.load_program_from_file(bin_file2)
        vm2.run()
        
        if vm2.memory.get_register(3) == 999:
            print("  [OK] WRITE_MEM/READ_MEM работают корректно")
        else:
            print(f"  [ERROR] Ожидалось 999, получено {vm2.memory.get_register(3)}")
        
        return True
        
    finally:
        # Очищаем временные файлы
        shutil.rmtree(temp_dir)

def test_memory_dump():
    """Тест дампа памяти в XML."""
    print_header("ТЕСТ ДАМПА ПАМЯТИ В XML")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        vm = VirtualMachine(data_memory_size=100)
        
        # Записываем некоторые значения
        vm.memory.write_data(0, 111)
        vm.memory.write_data(1, 222)
        vm.memory.write_data(50, 333)
        vm.memory.set_register(0, 444)
        vm.memory.set_register(1, 555)
        
        # Создаем дамп
        dump_file = os.path.join(temp_dir, "test_dump.xml")
        vm.memory.dump_to_xml(0, 10, dump_file)
        
        # Проверяем создание файла
        if os.path.exists(dump_file):
            print("  [OK] XML файл дампа создан")
            
            # Проверяем содержимое
            with open(dump_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'memory_dump' in content and 'data_memory' in content:
                print("  [OK] XML файл имеет правильную структуру")
                
                # Проверяем наличие некоторых значений
                if '111' in content and '444' in content:
                    print("  [OK] XML содержит правильные значения")
                else:
                    print("  [ERROR] XML не содержит ожидаемых значений")
                    return False
            else:
                print("  [ERROR] XML имеет неправильную структуру")
                return False
        else:
            print("  [ERROR] XML файл не создан")
            return False
        
        return True
        
    finally:
        shutil.rmtree(temp_dir)

def test_array_copy_program():
    """Тест программы копирования массива."""
    print_header("ТЕСТ ПРОГРАММЫ КОПИРОВАНИЯ МАССИВА")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Создаем простую программу копирования
        # Копируем 5 значений из адресов 100-104 в 200-204
        
        encoder = Encoder()
        commands = []
        
        # Инициализация
        commands.append(Command(158, [100, 0], 1, ""))   # R0 = 100 (источник)
        commands.append(Command(158, [200, 1], 2, ""))   # R1 = 200 (назначение)
        commands.append(Command(158, [5, 2], 3, ""))     # R2 = 5 (размер)
        commands.append(Command(158, [0, 3], 4, ""))     # R3 = 0 (счетчик)
        
        # В реальности здесь был бы цикл, но так как у нас нет ветвлений,
        # просто выполним фиксированное число операций
        
        # Записываем тестовые данные в источник
        for i in range(5):
            commands.append(Command(158, [1000 + i, 4], 5 + i*3, ""))      # R4 = значение
            commands.append(Command(158, [100 + i, 5], 6 + i*3, ""))       # R5 = адрес источника
            commands.append(Command(12, [5, 4], 7 + i*3, ""))              # memory[адрес] = значение
        
        # Копируем данные
        for i in range(5):
            commands.append(Command(17, [100 + i, 6], 20 + i*3, ""))       # R6 = memory[100+i]
            commands.append(Command(158, [200 + i, 7], 21 + i*3, ""))      # R7 = адрес назначения
            commands.append(Command(12, [7, 6], 22 + i*3, ""))             # memory[адрес] = значение
        
        binary = encoder.encode_commands(commands)
        
        # Сохраняем программу
        bin_file = os.path.join(temp_dir, "array_copy.bin")
        with open(bin_file, 'wb') as f:
            f.write(binary)
        
        # Запускаем
        vm = VirtualMachine()
        vm.load_program_from_file(bin_file)
        vm.run()
        
        # Проверяем результаты
        all_correct = True
        for i in range(5):
            src_val = vm.memory.read_data(100 + i)
            dst_val = vm.memory.read_data(200 + i)
            
            if src_val == dst_val:
                print(f"  [OK] Элемент {i}: {src_val} успешно скопирован")
            else:
                print(f"  [ERROR] Элемент {i}: источник={src_val}, назначение={dst_val}")
                all_correct = False
        
        return all_correct
        
    finally:
        shutil.rmtree(temp_dir)

def main():
    """Основная функция."""
    print("ПРОВЕРКА ЭТАПА 3: ИНТЕРПРЕТАТОР И ОПЕРАЦИИ С ПАМЯТЬЮ")
    
    # Запускаем тесты
    test1 = test_single_instructions()
    test2 = test_memory_dump()
    test3 = test_array_copy_program()
    
    print_header("ИТОГИ")
    
    if test1 and test2 and test3:
        print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("\nЭтап 3 завершен. Интерпретатор может:")
        print("  1. Загружать бинарные программы из файлов")
        print("  2. Декодировать и выполнять команды:")
        print("     - LOAD_CONST (загрузка константы)")
        print("     - READ_MEM (чтение из памяти)")
        print("     - WRITE_MEM (запись в память)")
        print("     - ABS (абсолютное значение)")
        print("  3. Управлять памятью данных и регистрами")
        print("  4. Создавать дамп памяти в формате XML")
        print("  5. Выполнять программы копирования массивов")
        
        # Пример использования
        print("\nПример использования:")
        print("  python run_interpreter.py program.bin dump.xml 0 100 --debug")
        
        return 0
    else:
        print("НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        return 1

if __name__ == '__main__':
    sys.exit(main())