#!/usr/bin/env python3
"""
Проверка этапа 4: Реализация АЛУ и команды ABS.
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
from vm.alu import ALU


def print_header(text):
    """Печатает заголовок."""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def test_alu_module():
    """Тест модуля АЛУ."""
    print_header("ТЕСТ МОДУЛЯ АЛУ")

    alu = ALU()

    test_cases = [
        (123, 123, "положительное число"),
        (-456, 456, "отрицательное число"),
        (0, 0, "ноль"),
        (2147483647, 2147483647, "максимальное положительное"),
        (-2147483648, 2147483647, "минимальное отрицательное (с переполнением)"),
    ]

    print("Тестирование операции abs() в АЛУ:")
    print("-" * 70)

    all_passed = True
    for input_val, expected, description in test_cases:
        result = alu.abs(input_val)

        if result == expected:
            print(f"  [OK] abs({input_val:11}) = {result:11} - {description}")
        else:
            print(f"  [ERROR] abs({input_val:11}) = {result:11} (ожидалось {expected}) - {description}")
            all_passed = False

    # Проверяем флаги для случая с переполнением
    alu.reset_flags()
    alu.abs(-2147483648)
    if alu.overflow_flag:
        print(f"  [OK] Флаг переполнения установлен для abs(-2147483648)")
    else:
        print(f"  [ERROR] Флаг переполнения не установлен для abs(-2147483648)")
        all_passed = False

    return all_passed


def test_abs_command_integration():
    """Тест команды ABS в полном цикле."""
    print_header("ТЕСТ КОМАНДЫ ABS В ИНТЕРПРЕТАТОРЕ")

    encoder = Encoder()
    vm = VirtualMachine(data_memory_size=5000)
    vm.show_alu_flags = True

    temp_dir = tempfile.mkdtemp()

    try:
        # Создаем программу, которая тестирует ABS
        commands = [
            # Загружаем тестовые значения в регистры
            Command(158, [1000, 0], 1, ""),  # R0 = 1000 (базовый адрес)
            Command(158, [123, 1], 2, ""),  # R1 = 123
            Command(158, [-456, 2], 3, ""),  # R2 = -456
            Command(158, [0, 3], 4, ""),  # R3 = 0

            # Выполняем ABS для каждого значения
            Command(214, [0, 0, 1], 5, ""),  # memory[1000] = abs(123)
            Command(214, [4, 0, 2], 6, ""),  # memory[1004] = abs(-456)
            Command(214, [8, 0, 3], 7, ""),  # memory[1008] = abs(0)

            # Считываем результаты для проверки
            Command(17, [1000, 4], 8, ""),  # R4 = memory[1000]
            Command(17, [1004, 5], 9, ""),  # R5 = memory[1004]
            Command(17, [1008, 6], 10, ""),  # R6 = memory[1008]
        ]

        binary = encoder.encode_commands(commands)

        # Сохраняем программу
        bin_file = os.path.join(temp_dir, "alu_test.bin")
        with open(bin_file, 'wb') as f:
            f.write(binary)

        # Запускаем интерпретатор
        print("Запуск тестовой программы...")
        vm.load_program_from_file(bin_file)
        vm.run()

        # Проверяем результаты
        print("\nПроверка результатов:")
        print("-" * 70)

        expected_results = [
            (1000, 123, "abs(123)"),
            (1004, 456, "abs(-456)"),
            (1008, 0, "abs(0)"),
        ]

        all_passed = True
        for address, expected, description in expected_results:
            actual = vm.memory.read_data(address)
            if actual == expected:
                print(f"  [OK] memory[{address}] = {actual} - {description}")
            else:
                print(f"  [ERROR] memory[{address}] = {actual} (ожидалось {expected}) - {description}")
                all_passed = False

        # Проверяем регистры
        print("\nПроверка регистров:")
        print("-" * 70)

        register_checks = [
            (4, 123, "R4 (abs(123))"),
            (5, 456, "R5 (abs(-456))"),
            (6, 0, "R6 (abs(0))"),
        ]

        for reg, expected, description in register_checks:
            actual = vm.memory.get_register(reg)
            if actual == expected:
                print(f"  [OK] R{reg} = {actual} - {description}")
            else:
                print(f"  [ERROR] R{reg} = {actual} (ожидалось {expected}) - {description}")
                all_passed = False

        return all_passed

    finally:
        shutil.rmtree(temp_dir)


def test_comprehensive_abs():
    """Тест всесторонней проверки команды ABS."""
    print_header("ВСЕСТОРОННИЙ ТЕСТ КОМАНДЫ ABS")

    encoder = Encoder()
    vm = VirtualMachine(data_memory_size=10000)

    temp_dir = tempfile.mkdtemp()

    try:
        # Тестируем ABS с разными сценариями
        commands = []

        # Сценарий 1: Простые значения
        commands.append(Command(158, [2000, 0], 1, ""))  # R0 = 2000
        commands.append(Command(158, [42, 1], 2, ""))  # R1 = 42
        commands.append(Command(214, [0, 0, 1], 3, ""))  # memory[2000] = abs(42)

        # Сценарий 2: Отрицательное значение
        commands.append(Command(158, [-1234, 2], 4, ""))  # R2 = -1234
        commands.append(Command(214, [4, 0, 2], 5, ""))  # memory[2004] = abs(-1234)

        # Сценарий 3: Ноль
        commands.append(Command(158, [0, 3], 6, ""))  # R3 = 0
        commands.append(Command(214, [8, 0, 3], 7, ""))  # memory[2008] = abs(0)

        # Сценарий 4: С отрицательным смещением
        commands.append(Command(158, [3000, 4], 8, ""))  # R4 = 3000
        commands.append(Command(158, [-999, 5], 9, ""))  # R5 = -999
        commands.append(Command(214, [-100, 4, 5], 10, ""))  # memory[2900] = abs(-999)

        # Сценарий 5: С положительным смещением
        commands.append(Command(158, [4000, 6], 11, ""))  # R6 = 4000
        commands.append(Command(158, [777, 7], 12, ""))  # R7 = 777
        commands.append(Command(214, [250, 6, 7], 13, ""))  # memory[4250] = abs(777)

        binary = encoder.encode_commands(commands)

        bin_file = os.path.join(temp_dir, "comprehensive.bin")
        with open(bin_file, 'wb') as f:
            f.write(binary)

        print("Запуск всестороннего теста ABS...")
        vm.load_program_from_file(bin_file)
        vm.run()

        # Проверяем все результаты
        print("\nПроверка всех сценариев:")
        print("-" * 70)

        test_cases = [
            (2000, 42, "ABS положительного"),
            (2004, 1234, "ABS отрицательного"),
            (2008, 0, "ABS нуля"),
            (2900, 999, "ABS с отрицательным смещением"),
            (4250, 777, "ABS с положительным смещением"),
        ]

        all_passed = True
        for address, expected, description in test_cases:
            try:
                actual = vm.memory.read_data(address)
                if actual == expected:
                    print(f"  [OK] {description}: memory[{address}] = {actual}")
                else:
                    print(f"  [ERROR] {description}: memory[{address}] = {actual} (ожидалось {expected})")
                    all_passed = False
            except Exception as e:
                print(f"  [ERROR] {description}: {e}")
                all_passed = False

        # Выводим статистику
        print(f"\nСтатистика выполнения:")
        print(f"  Выполнено инструкций: {vm.memory.instructions_executed}")
        print(f"  Обращений к памяти: {vm.memory.memory_accesses}")

        return all_passed

    finally:
        shutil.rmtree(temp_dir)


def create_test_program():
    """Создает тестовую программу для демонстрации."""
    print_header("СОЗДАНИЕ ТЕСТОВОЙ ПРОГРАММЫ")

    # Создаем простую тестовую программу на лету
    temp_dir = tempfile.mkdtemp()

    try:
        # Создаем программу напрямую через код
        encoder = Encoder()
        vm = VirtualMachine(data_memory_size=5000)

        # Простая тестовая программа для ABS
        commands = [
            Command(158, [1000, 0], 1, ""),  # R0 = 1000 (базовый адрес)
            Command(158, [123, 1], 2, ""),  # R1 = 123
            Command(158, [-456, 2], 3, ""),  # R2 = -456
            Command(158, [0, 3], 4, ""),  # R3 = 0

            # Выполняем ABS
            Command(214, [0, 0, 1], 5, ""),  # memory[1000] = abs(123)
            Command(214, [4, 0, 2], 6, ""),  # memory[1004] = abs(-456)
            Command(214, [8, 0, 3], 7, ""),  # memory[1008] = abs(0)

            # Считываем результаты
            Command(17, [1000, 4], 8, ""),  # R4 = memory[1000]
            Command(17, [1004, 5], 9, ""),  # R5 = memory[1004]
            Command(17, [1008, 6], 10, ""),  # R6 = memory[1008]
        ]

        binary = encoder.encode_commands(commands)

        # Сохраняем программу
        bin_file = os.path.join(temp_dir, "simple_alu_test.bin")
        with open(bin_file, 'wb') as f:
            f.write(binary)

        print(f"Создана тестовая программа: {bin_file}")

        # Запускаем интерпретатор
        print(f"\nЗапуск тестовой программы...")
        vm.load_program_from_file(bin_file)
        vm.run()

        # Проверяем результаты
        print("\nПроверка результатов выполнения:")
        print("-" * 70)

        test_cases = [
            (1000, 123, "abs(123)"),
            (1004, 456, "abs(-456)"),
            (1008, 0, "abs(0)"),
        ]

        all_passed = True
        for address, expected, description in test_cases:
            actual = vm.memory.read_data(address)
            if actual == expected:
                print(f"  [OK] memory[{address}] = {actual} - {description}")
            else:
                print(f"  [ERROR] memory[{address}] = {actual} (ожидалось {expected}) - {description}")
                all_passed = False

        return all_passed

    finally:
        shutil.rmtree(temp_dir)


def main():
    """Основная функция."""
    print("ПРОВЕРКА ЭТАПА 4: РЕАЛИЗАЦИЯ АРИФМЕТИКО-ЛОГИЧЕСКОГО УСТРОЙСТВА")

    # Запускаем тесты
    test1 = test_alu_module()
    test2 = test_abs_command_integration()
    test3 = test_comprehensive_abs()
    test4 = create_test_program()

    print_header("ИТОГИ ЭТАПА 4")

    if test1 and test2 and test3 and test4:
        print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("\nЭтап 4 завершен. Реализовано:")
        print("  1. Арифметико-логическое устройство (АЛУ)")
        print("  2. Полная поддержка команды abs()")
        print("  3. Флаги состояния АЛУ (Z, N, V, C)")
        print("  4. Обработка переполнения для крайних случаев")
        print("  5. Интеграция АЛУ с интерпретатором")
        print("  6. Тестовая программа, демонстрирующая вычисления")

        print("\nПример использования:")
        print("  python run_assembler.py examples/alu_test.asm program.bin")
        print("  python run_interpreter.py program.bin dump.xml 900 1300 --debug --show-flags")

        return 0
    else:
        print("НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        print("\nПроблемы обнаружены в:")
        if not test1: print("  - Модуль АЛУ")
        if not test2: print("  - Интеграция команды ABS")
        if not test3: print("  - Всесторонний тест ABS")
        if not test4: print("  - Создание тестовой программы")
        return 1


if __name__ == '__main__':
    sys.exit(main())