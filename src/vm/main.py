"""
Главный модуль интерпретатора УВМ.
"""

import sys
import argparse
from pathlib import Path
from .interpreter import VirtualMachine

def main():
    """Точка входа интерпретатора."""
    parser = argparse.ArgumentParser(
        description='Интерпретатор учебной виртуальной машины (УВМ)',
        epilog='Пример: python interpreter.py program.bin dump.xml 0 100 --debug'
    )
    
    parser.add_argument('program_file', help='Путь к бинарному файлу с программой')
    parser.add_argument('dump_file', help='Путь к файлу для дампа памяти')
    parser.add_argument('start_addr', type=int, help='Начальный адрес для дампа памяти')
    parser.add_argument('end_addr', type=int, help='Конечный адрес для дампа памяти')
    
    parser.add_argument('--debug', action='store_true', 
                       help='Режим отладки (вывод выполняемых инструкций)')
    parser.add_argument('--step', action='store_true', 
                       help='Пошаговый режим выполнения')
    parser.add_argument('--max-steps', type=int, default=0,
                       help='Максимальное количество инструкций для выполнения')
    
    args = parser.parse_args()
    
    # Проверяем существование файла программы
    program_path = Path(args.program_file)
    if not program_path.exists():
        print(f"Ошибка: файл программы не найден: {args.program_file}")
        sys.exit(1)
    
    # Проверяем диапазон адресов
    if args.start_addr < 0:
        print(f"Ошибка: начальный адрес не может быть отрицательным: {args.start_addr}")
        sys.exit(1)
    
    if args.end_addr < args.start_addr:
        print(f"Ошибка: конечный адрес должен быть >= начального: {args.end_addr} < {args.start_addr}")
        sys.exit(1)
    
    # Создаем и настраиваем виртуальную машину
    vm = VirtualMachine()
    vm.debug = args.debug
    vm.step_by_step = args.step
    
    print("=" * 60)
    print("УЧЕБНАЯ ВИРТУАЛЬНАЯ МАШИНА (УВМ) - ИНТЕРПРЕТАТОР")
    print("=" * 60)
    
    # Загружаем программу
    vm.load_program_from_file(args.program_file)
    
    # Запускаем выполнение
    vm.run(max_steps=args.max_steps)
    
    # Создаем дамп памяти
    vm.dump_memory(args.start_addr, args.end_addr, args.dump_file)
    
    # Выводим статус
    vm.memory.print_status()
    
    print(f"\nДамп памяти сохранен в: {args.dump_file}")
    print("=" * 60)

if __name__ == '__main__':
    main()