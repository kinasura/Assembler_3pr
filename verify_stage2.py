#!/usr/bin/env python3
"""
Скрипт для проверки этапа 2.
"""

import sys
import os

# Добавляем src в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from assembler.command import Command


def test_encoding():
    """Тест кодирования команд."""
    print("=" * 60)
    print("Проверка кодирования команд")
    print("=" * 60)

    test_cases = [
        {
            'name': 'LOAD_CONST (158,679,28)',
            'command': Command(158, [679, 28], 1, "158,679,28"),
            'expected_size': 6,
        },
        {
            'name': 'READ_MEM (17,356,24)',
            'command': Command(17, [356, 24], 1, "17,356,24"),
            'expected_size': 5,
        },
        {
            'name': 'WRITE_MEM (12,5,3)',
            'command': Command(12, [5, 3], 1, "12,5,3"),
            'expected_size': 3,
        },
        {
            'name': 'ABS (214,95,2,27)',
            'command': Command(214, [95, 2, 27], 1, "214,95,2,27"),
            'expected_size': 5,
        },
    ]

    all_passed = True

    for test in test_cases:
        print(f"\nТест: {test['name']}")

        try:
            # Проверяем размер
            actual_size = test['command'].get_size()
            if actual_size == test['expected_size']:
                print(f"  [OK] Размер правильный: {actual_size} байт")
            else:
                print(f"  [ERROR] Неверный размер: ожидалось {test['expected_size']}, получено {actual_size}")
                all_passed = False

            # Кодируем
            encoded = test['command'].encode()
            hex_str = test['command'].to_hex_string()
            print(f"  [OK] Закодировано: {hex_str}")

            # Проверяем размер закодированных данных
            if len(encoded) == test['expected_size']:
                print(f"  [OK] Размер закодированных данных правильный: {len(encoded)} байт")
            else:
                print(f"  [ERROR] Неверный размер закодированных данных: {len(encoded)} байт")
                all_passed = False

        except Exception as e:
            print(f"  [ERROR] Ошибка: {e}")
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("Все тесты пройдены успешно!")
    else:
        print("Некоторые тесты не пройдены.")
    print("=" * 60)

    return all_passed


def test_file_output():
    """Тест записи в файл."""
    print("\n" + "=" * 60)
    print("Проверка записи в файл")
    print("=" * 60)

    try:
        # Создаем тестовую команду
        command = Command(158, [100, 5], 1, "158,100,5")
        encoded = command.encode()

        # Записываем в файл
        test_filename = "test_binary_output.bin"
        with open(test_filename, 'wb') as f:
            f.write(encoded)

        # Читаем обратно и проверяем
        with open(test_filename, 'rb') as f:
            read_data = f.read()

        if encoded == read_data:
            print(f"[OK] Файл успешно записан и прочитан: {test_filename}")
            print(f"  Размер файла: {len(read_data)} байт")

            # Формируем hex-строку без использования sep параметра
            hex_bytes = [f"{b:02x}" for b in read_data]
            print(f"  Содержимое: {', '.join(hex_bytes)}")

            # Удаляем тестовый файл
            import os
            os.remove(test_filename)
            print(f"  Тестовый файл удален")

            return True
        else:
            print(f"[ERROR] Данные не совпадают!")
            return False

    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        return False


def main():
    """Основная функция."""
    print("Проверка этапа 2: Формирование машинного кода")

    # Проверяем кодирование
    encoding_ok = test_encoding()

    # Проверяем запись в файл
    file_ok = test_file_output()

    if encoding_ok and file_ok:
        print("\n" + "=" * 60)
        print("Этап 2 успешно пройден!")
        print("=" * 60)
        return 0
    else:
        print("\n" + "=" * 60)
        print("Этап 2 не пройден!")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())    