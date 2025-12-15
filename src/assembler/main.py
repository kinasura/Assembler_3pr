"""
Главный модуль ассемблера УВМ.
"""

import sys
import argparse
from pathlib import Path
from .parser import Parser
from .encoder import Encoder

def main():
    """Точка входа ассемблера."""
    parser = argparse.ArgumentParser(
        description='Ассемблер для учебной виртуальной машины (УВМ)',
        epilog='Пример: python assembler.py program.asm program.bin --test'
    )
    
    parser.add_argument('input_file', help='Путь к исходному файлу с текстом программы')
    parser.add_argument('output_file', help='Путь к двоичному файлу-результату')
    parser.add_argument('--test', action='store_true', 
                       help='Режим тестирования (вывод промежуточного представления и байтов)')
    
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
        
        # Кодируем команды в бинарный формат
        encoder = Encoder()
        binary_data = encoder.encode_commands(commands)
        
        # Сохраняем бинарный файл
        output_path = Path(args.output_file)
        with open(output_path, 'wb') as f:
            f.write(binary_data)
        
        # Выводим информацию о файле
        file_size = output_path.stat().st_size
        print(f"\nДвоичный файл создан: {output_path}")
        print(f"Размер файла: {file_size} байт")
        
        # В режиме тестирования выводим байтовое представление
        if args.test:
            print("\nБайтовое представление (hex):")
            print("-" * 40)
            for i, command in enumerate(commands):
                print(f"Команда {i+1}: {command.to_hex_string()}")
            
            print("\nБайтовое представление (тестовый формат):")
            print("-" * 40)
            for i, command in enumerate(commands):
                print(f"Команда {i+1}: {command.to_test_format()}")
            print("-" * 40)
        
    except Exception as e:
        print(f"Ошибка ассемблирования: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()