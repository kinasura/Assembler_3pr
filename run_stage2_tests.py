#!/usr/bin/env python3
"""
Полная проверка этапа 2.
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Запускает команду и возвращает результат."""
    print(f"Выполняется: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Ошибка: {result.stderr}")
    else:
        print(f"Успешно: {result.stdout}")
    return result.returncode

def main():
    """Основная функция."""
    print("=" * 70)
    print("ПОЛНАЯ ПРОВЕРКА ЭТАПА 2: ФОРМИРОВАНИЕ МАШИННОГО КОДА")
    print("=" * 70)
    
    # 1. Запускаем unit-тесты
    print("\n1. Запуск unit-тестов...")
    tests_passed = run_command("python run_tests.py") == 0
    
    # 2. Запускаем проверку кодирования
    print("\n2. Проверка кодирования команд...")
    encoding_passed = run_command("python verify_stage2.py") == 0
    
    # 3. Запускаем ассемблер на тестовом файле
    print("\n3. Запуск ассемблера на тестовом файле...")
    
    # Удаляем старый выходной файл, если существует
    if os.path.exists("output.bin"):
        os.remove("output.bin")
    
    # Запускаем ассемблер
    assembler_cmd = 'python run_assembler.py examples/test_all_commands.asm output.bin --test'
    assembler_passed = run_command(assembler_cmd) == 0
    
    # 4. Проверяем размер выходного файла
    print("\n4. Проверка выходного файла...")
    if os.path.exists("output.bin"):
        file_size = os.path.getsize("output.bin")
        print(f"Размер файла output.bin: {file_size} байт")
        
        # Ожидаемый размер: 6 + 5 + 3 + 5 = 19 байт
        if file_size == 19:
            print("✓ Размер файла правильный")
            file_check = True
        else:
            print(f"✗ Неверный размер файла: ожидалось 19 байт, получено {file_size} байт")
            file_check = False
    else:
        print("✗ Файл output.bin не создан")
        file_check = False
    
    # 5. Итог
    print("\n" + "=" * 70)
    print("ИТОГИ ПРОВЕРКИ:")
    print(f"  Unit-тесты: {'ПРОЙДЕНО' if tests_passed else 'НЕ ПРОЙДЕНО'}")
    print(f"  Кодирование: {'ПРОЙДЕНО' if encoding_passed else 'НЕ ПРОЙДЕНО'}")
    print(f"  Ассемблер: {'ПРОЙДЕНО' if assembler_passed else 'НЕ ПРОЙДЕНО'}")
    print(f"  Файл: {'ПРОЙДЕНО' if file_check else 'НЕ ПРОЙДЕНО'}")
    
    all_passed = tests_passed and encoding_passed and assembler_passed and file_check
    
    if all_passed:
        print("\n✓ ЭТАП 2 УСПЕШНО ЗАВЕРШЕН!")
        print("  Все проверки пройдены.")
        return 0
    else:
        print("\n✗ ЭТАП 2 НЕ ПРОЙДЕН!")
        print("  Некоторые проверки не пройдены.")
        return 1

if __name__ == '__main__':
    sys.exit(main())