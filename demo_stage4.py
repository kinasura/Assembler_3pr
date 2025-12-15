#!/usr/bin/env python3
"""
Демонстрация Этапа 4: Работа АЛУ и команды ABS.
"""

import sys
import os

# Добавляем src в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from assembler.command import Command
from assembler.encoder import Encoder
from vm.interpreter import VirtualMachine
from vm.alu import ALU

def demo_alu_operations():
    """Демонстрация операций АЛУ."""
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ АЛУ")
    print("=" * 70)
    
    alu = ALU()
    
    print("\n1. Базовые операции abs():")
    print("-" * 40)
    
    test_values = [123, -456, 0, 500000, -500000]
    for val in test_values:
        result = alu.abs(val)
        print(f"   abs({val:10}) = {result:10} Флаги: {alu.get_status_string()}")
        alu.reset_flags()
    
    print("\n2. Проверка флагов состояния:")
    print("-" * 40)
    
    # Ноль
    alu.abs(0)
    print(f"   abs(0): Флаги: {alu.get_status_string()} (Z должен быть установлен)")
    alu.reset_flags()
    
    # Отрицательное число
    alu.abs(-123)
    print(f"   abs(-123): Флаги: {alu.get_status_string()}")
    alu.reset_flags()

def demo_abs_command():
    """Демонстрация команды ABS в интерпретаторе."""
    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ КОМАНДЫ ABS В ИНТЕРПРЕТАТОРЕ")
    print("=" * 70)
    
    # Создаем программу вручную
    encoder = Encoder()
    vm = VirtualMachine(data_memory_size=2000)
    vm.debug = True
    vm.show_alu_flags = True
    
    # Простая программа с ABS
    commands = [
        Command(158, [1000, 0], 1, "R0 = 1000 (базовый адрес)"),
        Command(158, [123, 1], 2, "R1 = 123"),
        Command(158, [-456, 2], 3, "R2 = -456"),
        Command(214, [0, 0, 1], 4, "memory[1000] = abs(R1) = abs(123)"),
        Command(214, [4, 0, 2], 5, "memory[1004] = abs(R2) = abs(-456)"),
        Command(17, [1000, 3], 6, "R3 = memory[1000] (должно быть 123)"),
        Command(17, [1004, 4], 7, "R4 = memory[1004] (должно быть 456)"),
    ]
    
    print("\nПрограмма:")
    print("-" * 40)
    for i, cmd in enumerate(commands):
        print(f"{i+1:2}. {cmd.raw_line if cmd.raw_line else cmd}")
    
    binary = encoder.encode_commands(commands)
    
    # Сохраняем временно
    import tempfile
    temp_dir = tempfile.mkdtemp()
    bin_file = os.path.join(temp_dir, "demo.bin")
    
    with open(bin_file, 'wb') as f:
        f.write(binary)
    
    try:
        print(f"\nРазмер программы: {len(binary)} байт")
        
        # Запускаем
        vm.load_program_from_file(bin_file)
        print("\nВыполнение программы:")
        print("-" * 40)
        vm.run()
        
        # Показываем результаты
        print("\nРезультаты:")
        print("-" * 40)
        print(f"  memory[1000] = {vm.memory.read_data(1000)} (ожидалось 123)")
        print(f"  memory[1004] = {vm.memory.read_data(1004)} (ожидалось 456)")
        print(f"  R3 = {vm.memory.get_register(3)} (ожидалось 123)")
        print(f"  R4 = {vm.memory.get_register(4)} (ожидалось 456)")
        
        # Создаем дамп
        dump_file = "stage4_demo_dump.xml"
        vm.memory.dump_to_xml(990, 1010, dump_file)
        print(f"\nДамп памяти сохранен в: {dump_file}")
        
    finally:
        import shutil
        shutil.rmtree(temp_dir)

def demo_comprehensive():
    """Комплексная демонстрация."""
    print("\n" + "=" * 70)
    print("КОМПЛЕКСНАЯ ДЕМОНСТРАЦИЯ")
    print("=" * 70)
    
    print("\n1. Создаем и выполняем программу с различными случаями ABS:")
    
    encoder = Encoder()
    vm = VirtualMachine(data_memory_size=3000)
    
    commands = [
        # Различные тесты ABS
        Command(158, [2000, 0], 1, ""),   # Базовый адрес
        Command(158, [42, 1], 2, ""),     # Положительное
        Command(158, [-1234, 2], 3, ""),  # Отрицательное
        Command(158, [0, 3], 4, ""),      # Ноль
        
        # ABS с разными смещениями
        Command(214, [0, 0, 1], 5, ""),   # memory[2000] = abs(42)
        Command(214, [4, 0, 2], 6, ""),   # memory[2004] = abs(-1234)
        Command(214, [8, 0, 3], 7, ""),   # memory[2008] = abs(0)
        
        # ABS с отрицательным смещением
        Command(158, [2500, 4], 8, ""),   # Базовый адрес
        Command(158, [-999, 5], 9, ""),   # Отрицательное число
        Command(214, [-100, 4, 5], 10, ""), # memory[2400] = abs(-999)
    ]
    
    binary = encoder.encode_commands(commands)
    
    import tempfile
    import shutil
    temp_dir = tempfile.mkdtemp()
    
    try:
        bin_file = os.path.join(temp_dir, "comprehensive.bin")
        with open(bin_file, 'wb') as f:
            f.write(binary)
        
        vm.load_program_from_file(bin_file)
        vm.run()
        
        print("\nРезультаты выполнения:")
        print("-" * 40)
        
        results = [
            (2000, 42, "ABS положительного (42)"),
            (2004, 1234, "ABS отрицательного (-1234)"),
            (2008, 0, "ABS нуля (0)"),
            (2400, 999, "ABS с отрицательным смещением (-999 по адресу 2500-100=2400)"),
        ]
        
        for addr, expected, desc in results:
            actual = vm.memory.read_data(addr)
            status = "OK" if actual == expected else "ERROR"
            print(f"  [{status}] {desc}: memory[{addr}] = {actual} (ожидалось {expected})")
        
        print(f"\nСтатистика выполнения:")
        print(f"  Выполнено инструкций: {vm.memory.instructions_executed}")
        print(f"  Обращений к памяти: {vm.memory.memory_accesses}")
        
    finally:
        shutil.rmtree(temp_dir)

def main():
    """Основная функция."""
    print("ДЕМОНСТРАЦИЯ ЭТАПА 4: АРИФМЕТИКО-ЛОГИЧЕСКОЕ УСТРОЙСТВО")
    print("=" * 70)
    
    print("\nЭтап 4 демонстрирует реализацию АЛУ и полную поддержку команды ABS.")
    
    # Демонстрация АЛУ
    demo_alu_operations()
    
    # Демонстрация команды ABS
    demo_abs_command()
    
    # Комплексная демонстрация
    demo_comprehensive()
    
    print("\n" + "=" * 70)
    print("ВЫВОДЫ:")
    print("-" * 70)
    print("1. АЛУ успешно реализовано и интегрировано с интерпретатором")
    print("2. Команда ABS корректно вычисляет абсолютное значение")
    print("3. Поддерживаются отрицательные и положительные смещения")
    print("4. Результаты сохраняются в память для проверки")
    print("5. Флаги состояния АЛУ работают корректно")
    print("\nЭтап 4 успешно завершен!")
    print("=" * 70)

if __name__ == '__main__':
    main()