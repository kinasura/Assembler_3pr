"""
Главный модуль ассемблера УВМ.
"""

import sys
import argparse
from pathlib import Path
from .parser import Parser

def main():
    """Точка входа ассемблера."""
    parser = argparse.ArgumentParser(
        description='Ассемблер для учебной виртуальной машины (УВМ)',
        epilog='Пример: python assembler.py program.asm program.bin --test'
    )
    
    parser.add_argument('input_file', help='Путь к исходному файлу с текстом программы')
    parser.add_argument('output_file', help='Путь к двоичному файлу-результату')
    parser.add_argument('--test', action='store_true', 
                       help='Режим тестирования (вывод промежуточного представления)')
    
    args = parser.parse_args()
    
    # Проверяем существование входного файла
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Ошибка: файл '{args.input_file}' не найден")
        sys.exit(1)
    
    # Парсим файл
    try:
        parser = Parser()
        commands = parser.parse_file(args.input_file)
        
        # Выводим статистику
        print(f"Успешно распарсено {len(commands)} команд")
        
        # В режиме тестирования выводим промежуточное представление
        if args.test:
            print("\nПромежуточное представление:")
            print("-" * 40)
            for command in commands:
                print(command.to_intermediate_format())
            print("-" * 40)
        
        # На этом этапе просто сообщаем об успешном парсинге
        # Генерация машинного кода будет на этапе 2
        print(f"\nРезультат сохранен в промежуточном представлении")
        print(f"Двоичный файл будет сгенерирован на этапе 2")
        
        # Сохраняем промежуточное представление в файл (для отладки)
        intermediate_file = Path(args.output_file).with_suffix('.intermediate')
        with open(intermediate_file, 'w', encoding='utf-8') as f:
            for command in commands:
                f.write(command.to_intermediate_format() + '\n')
        
        print(f"Промежуточное представление сохранено в: {intermediate_file}")
        
    except Exception as e:
        print(f"Ошибка ассемблирования: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()