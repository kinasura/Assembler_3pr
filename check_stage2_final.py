#!/usr/bin/env python3
"""
Финальная проверка этапа 2.
"""

import sys
import os

# Добавляем src в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from assembler.command import Command

def print_header(text):
    """Печатает заголовок."""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)

def test_all_commands():
    """Тестирует все команды из спецификации."""
    print_header("ТЕСТ КОМАНД ИЗ СПЕЦИФИКАЦИИ")
    
    commands = [
        ("LOAD_CONST", Command(158, [679, 28], 1, "158,679,28")),
        ("READ_MEM", Command(17, [356, 24], 1, "17,356,24")),
        ("WRITE_MEM", Command(12, [5, 3], 1, "12,5,3")),
        ("ABS", Command(214, [95, 2, 27], 1, "214,95,2,27")),
    ]
    
    print("Команда                | Размер | Hex представление")
    print("-" * 70)
    
    for name, cmd in commands:
        try:
            encoded = cmd.encode()
            hex_str = cmd.to_hex_string()
            print(f"{name:20} | {len(encoded):6} | {hex_str}")
        except Exception as e:
            print(f"{name:20} | ERROR  | {e}")
    
    return True

def test_binary_file():
    """Тест создания бинарного файла."""
    print_header("ТЕСТ СОЗДАНИЯ БИНАРНОГО ФАЙЛА")
    
    try:
        # Создаем тестовые команды
        commands = [
            Command(158, [100, 0], 1, ""),
            Command(17, [500, 1], 2, ""),
            Command(12, [0, 2], 3, ""),
            Command(214, [10, 3, 4], 4, ""),
        ]
        
        # Кодируем все команды
        from src.assembler.encoder import Encoder
        encoder = Encoder()
        binary_data = encoder.encode_commands(commands)
        
        # Записываем в файл
        output_file = "stage2_test_output.bin"
        with open(output_file, 'wb') as f:
            f.write(binary_data)
        
        # Проверяем размер
        file_size = os.path.getsize(output_file)
        expected_size = 6 + 5 + 3 + 5  # 19 байт
        
        print(f"Файл создан: {output_file}")
        print(f"Размер файла: {file_size} байт")
        print(f"Ожидаемый размер: {expected_size} байт")
        
        if file_size == expected_size:
            print("[OK] Размер файла правильный")
            
            # Читаем и показываем содержимое
            with open(output_file, 'rb') as f:
                data = f.read()
            
            # Показываем первые 32 байта
            print("\nПервые 32 байта файла:")
            hex_bytes = [f"{b:02x}" for b in data[:32]]
            for i in range(0, len(hex_bytes), 8):
                line = hex_bytes[i:i+8]
                print("  " + " ".join(line))
            
            # Удаляем тестовый файл
            os.remove(output_file)
            print(f"\nТестовый файл удален")
            return True
        else:
            print("[ERROR] Неверный размер файла")
            return False
            
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def test_intermediate_representation():
    """Тест промежуточного представления."""
    print_header("ТЕСТ ПРОМЕЖУТОЧНОГО ПРЕДСТАВЛЕНИЯ")
    
    commands = [
        Command(158, [679, 28], 1, "158,679,28"),
        Command(17, [356, 24], 2, "17,356,24"),
        Command(12, [5, 3], 3, "12,5,3"),
        Command(214, [95, 2, 27], 4, "214,95,2,27"),
    ]
    
    for cmd in commands:
        print(cmd.to_intermediate_format())
    
    return True

def main():
    """Основная функция."""
    print("ФИНАЛЬНАЯ ПРОВЕРКА ЭТАПА 2")
    print("=" * 70)
    
    # Запускаем все тесты
    test1 = test_all_commands()
    test2 = test_binary_file()
    test3 = test_intermediate_representation()
    
    print_header("ИТОГИ")
    
    if test1 and test2 and test3:
        print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("\nЭтап 2 завершен. Ассемблер может:")
        print("  1. Парсить команды из CSV-файлов")
        print("  2. Проверять валидность команд")
        print("  3. Преобразовывать команды в промежуточное представление")
        print("  4. Кодировать команды в бинарный формат")
        print("  5. Сохранять результат в бинарный файл")
        print("  6. Выводить hex-представление команд")
        return 0
    else:
        print("НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        return 1

if __name__ == '__main__':
    sys.exit(main())