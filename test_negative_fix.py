#!/usr/bin/env python3
"""
Тест исправлений для отрицательных чисел.
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


def test_negative_load():
    """Тест загрузки отрицательных чисел."""
    print("Тест загрузки отрицательных чисел:")

    # Проверяем валидацию
    try:
        cmd1 = Command(158, [-100, 0], 1, "")
        print("  [OK] LOAD_CONST с -100 проходит валидацию")
    except ValueError as e:
        print(f"  [ERROR] {e}")
        return False

    # Проверяем кодирование/декодирование
    encoder = Encoder()
    vm = VirtualMachine()

    temp_dir = tempfile.mkdtemp()

    try:
        # Создаем программу с отрицательным числом
        cmds = [
            Command(158, [-100, 0], 1, ""),
            Command(158, [200, 1], 2, ""),
            Command(158, [1000, 2], 3, ""),
            Command(12, [2, 0], 4, ""),  # memory[1000] = R0 (-100)
            Command(17, [1000, 3], 5, ""),  # R3 = memory[1000]
        ]

        binary = encoder.encode_commands(cmds)

        # Сохраняем
        bin_file = os.path.join(temp_dir, "test.bin")
        with open(bin_file, 'wb') as f:
            f.write(binary)

        # Запускаем
        vm.load_program_from_file(bin_file)
        vm.run()

        # Проверяем
        reg0 = vm.memory.get_register(0)
        reg3 = vm.memory.get_register(3)

        if reg0 == -100:
            print(f"  [OK] Отрицательное число успешно загружено в регистр 0: {reg0}")
        else:
            print(f"  [ERROR] Ожидалось -100, получено {reg0}")
            return False

        if reg3 == -100:
            print(f"  [OK] Отрицательное число успешно прочитано из памяти в регистр 3: {reg3}")
        else:
            print(f"  [ERROR] Ожидалось -100, получено {reg3}")
            return False

        return True

    finally:
        shutil.rmtree(temp_dir)


def test_abs_command():
    """Тест команды ABS."""
    print("\nТест команды ABS:")

    encoder = Encoder()
    vm = VirtualMachine(data_memory_size=2000)

    temp_dir = tempfile.mkdtemp()

    try:
        # Создаем программу с ABS
        cmds = [
            Command(158, [-123, 0], 1, ""),  # R0 = -123
            Command(158, [1000, 1], 2, ""),  # R1 = 1000
            Command(214, [0, 1, 0], 3, ""),  # memory[1000] = abs(R0) = 123
            Command(158, [456, 2], 4, ""),  # R2 = 456
            Command(158, [1001, 3], 5, ""),  # R3 = 1001
            Command(214, [0, 3, 2], 6, ""),  # memory[1001] = abs(R2) = 456
        ]

        binary = encoder.encode_commands(cmds)

        bin_file = os.path.join(temp_dir, "test.bin")
        with open(bin_file, 'wb') as f:
            f.write(binary)

        vm.load_program_from_file(bin_file)
        vm.run()

        # Проверяем
        mem1000 = vm.memory.read_data(1000)
        mem1001 = vm.memory.read_data(1001)

        if mem1000 == 123:
            print(f"  [OK] ABS(-123) = 123 правильно записан в память по адресу 1000")
        else:
            print(f"  [ERROR] Ожидалось 123, получено {mem1000}")
            return False

        if mem1001 == 456:
            print(f"  [OK] ABS(456) = 456 правильно записан в память по адресу 1001")
        else:
            print(f"  [ERROR] Ожидалось 456, получено {mem1001}")
            return False

        return True

    finally:
        shutil.rmtree(temp_dir)


def test_negative_offset():
    """Тест отрицательного смещения в ABS."""
    print("\nТест отрицательного смещения в ABS:")

    encoder = Encoder()
    vm = VirtualMachine(data_memory_size=2000)

    temp_dir = tempfile.mkdtemp()

    try:
        # Создаем программу с отрицательным смещением
        cmds = [
            Command(158, [-999, 0], 1, ""),  # R0 = -999
            Command(158, [1050, 1], 2, ""),  # R1 = 1050
            Command(214, [-50, 1, 0], 3, ""),  # memory[1050-50] = abs(R0) = 999
        ]

        binary = encoder.encode_commands(cmds)

        bin_file = os.path.join(temp_dir, "test.bin")
        with open(bin_file, 'wb') as f:
            f.write(binary)

        vm.load_program_from_file(bin_file)
        vm.run()

        # Проверяем: адрес должен быть 1050 - 50 = 1000
        mem1000 = vm.memory.read_data(1000)

        if mem1000 == 999:
            print(f"  [OK] ABS с отрицательным смещением работает:")
            print(f"      memory[1000] = {mem1000}")
        else:
            print(f"  [ERROR] Ожидалось 999, получено {mem1000}")
            return False

        return True

    finally:
        shutil.rmtree(temp_dir)


def main():
    """Основная функция."""
    print("=" * 70)
    print("ТЕСТ ИСПРАВЛЕНИЙ ДЛЯ ОТРИЦАТЕЛЬНЫХ ЧИСЕЛ")
    print("=" * 70)

    tests = [
        ("Загрузка отрицательных чисел", test_negative_load),
        ("Команда ABS", test_abs_command),
        ("Отрицательное смещение", test_negative_offset),
    ]

    all_passed = True
    for name, test_func in tests:
        print(f"\n{name}:")
        try:
            if test_func():
                print(f"  [OK] Тест пройден")
            else:
                print(f"  [ERROR] Тест не пройден")
                all_passed = False
        except Exception as e:
            print(f"  [ERROR] Исключение: {e}")
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("Отрицательные числа теперь поддерживаются корректно.")
        return 0
    else:
        print("НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        return 1


if __name__ == '__main__':
    sys.exit(main())