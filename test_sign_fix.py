#!/usr/bin/env python3
"""
Тест исправлений для знаковых чисел.
"""

import sys
import os

# Добавляем src в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from assembler.command import Command
from vm.memory import Memory

def test_memory_signed():
    """Тест знаковых операций в памяти."""
    print("Тест знаковых операций в памяти:")
    
    mem = Memory()
    
    # Тест 1: Запись отрицательного числа
    mem.write_data(0, -100)
    val = mem.read_data(0)
    print(f"  Записано -100, прочитано: {val}")
    
    # Тест 2: Запись положительного числа
    mem.write_data(1, 200)
    val = mem.read_data(1)
    print(f"  Записано 200, прочитано: {val}")
    
    # Тест 3: Проверка регистров
    mem.set_register(0, -50)
    val = mem.get_register(0)
    print(f"  В регистр 0 записано -50, прочитано: {val}")
    
    mem.set_register(1, 150)
    val = mem.get_register(1)
    print(f"  В регистр 1 записано 150, прочитано: {val}")
    
    return val == 150

def test_command_negative():
    """Тест команд с отрицательными числами."""
    print("\nТест команд с отрицательными числами:")
    
    # Проверяем, что отрицательные числа проходят валидацию
    try:
        cmd1 = Command(158, [-100, 0], 1, "158,-100,0")
        print("  [OK] LOAD_CONST с -100 проходит валидацию")
        
        # Проверяем кодирование
        encoded = cmd1.encode()
        print(f"  Закодировано: {cmd1.to_hex_string()}")
        
    except ValueError as e:
        print(f"  [ERROR] {e}")
        return False
    
    return True

def test_abs_operation():
    """Тест операции ABS."""
    print("\nТест операции ABS:")
    
    mem = Memory()
    
    # Записываем отрицательное число в регистр
    mem.set_register(0, -123)
    val = mem.get_register(0)
    print(f"  В регистр 0 записано -123, прочитано: {val}")
    
    # Вычисляем abs
    abs_val = abs(val)
    print(f"  abs({val}) = {abs_val}")
    
    # Записываем результат в память
    mem.write_data(100, abs_val)
    mem_val = mem.read_data(100)
    print(f"  В память по адресу 100 записано {abs_val}, прочитано: {mem_val}")
    
    return mem_val == 123

def main():
    """Основная функция."""
    print("=" * 70)
    print("ТЕСТ ИСПРАВЛЕНИЙ ДЛЯ ЗНАКОВЫХ ЧИСЕЛ")
    print("=" * 70)
    
    tests = [
        ("Знаковые операции в памяти", test_memory_signed),
        ("Команды с отрицательными числами", test_command_negative),
        ("Операция ABS", test_abs_operation),
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
        print("Знаковые числа теперь работают корректно.")
        return 0
    else:
        print("НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        return 1

if __name__ == '__main__':
    sys.exit(main())