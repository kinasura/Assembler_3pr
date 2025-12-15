"""
Парсер исходного кода ассемблера.
"""

import re
from typing import List
import chardet
from .command import Command

class Parser:
    """Парсер для языка ассемблера УВМ."""

    def __init__(self):
        self.comment_pattern = re.compile(r';.*$')
        self.whitespace_pattern = re.compile(r'\s+')

    def detect_encoding(self, file_path: str) -> str:
        """Определяет кодировку файла."""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(1024)
                result = chardet.detect(raw_data)
                encoding = result.get('encoding', 'utf-8')

                # Если кодировка не определена или это ASCII, используем UTF-8
                if not encoding or encoding.lower() == 'ascii':
                    encoding = 'utf-8'

                return encoding
        except Exception:
            return 'utf-8'

    def parse_line(self, line: str, line_number: int) -> Command:
        """Парсинг одной строки ассемблера."""
        # Удаляем комментарии
        line = self.comment_pattern.sub('', line).strip()

        # Пропускаем пустые строки
        if not line:
            return None

        # Разделяем по запятым
        parts = [part.strip() for part in line.split(',')]

        # Проверяем, что есть код операции
        if not parts:
            raise ValueError(f"Строка {line_number}: пустая команда")

        # Преобразуем в числа
        try:
            opcode = int(parts[0])
            args = [int(arg) for arg in parts[1:]]
        except ValueError as e:
            raise ValueError(f"Строка {line_number}: неверный числовой формат: {line}") from e

        # Создаем команду
        return Command(opcode=opcode, args=args, line_number=line_number, raw_line=line)

    def parse_file(self, file_path: str) -> List[Command]:
        """Парсинг всего файла."""
        commands = []

        try:
            # Определяем кодировку файла
            encoding = self.detect_encoding(file_path)

            with open(file_path, 'r', encoding=encoding) as f:
                for line_number, line in enumerate(f, 1):
                    try:
                        command = self.parse_line(line, line_number)
                        if command:
                            commands.append(command)
                    except ValueError as e:
                        print(f"Ошибка в строке {line_number}: {e}")
                        raise

        except FileNotFoundError:
            print(f"Файл не найден: {file_path}")
            raise
        except UnicodeDecodeError as e:
            print(f"Ошибка декодирования файла {file_path}: {e}")
            print("Попытка использовать кодировку cp1251...")
            try:
                # Попробуем cp1251 (Windows-1251) для русских символов
                with open(file_path, 'r', encoding='cp1251') as f:
                    for line_number, line in enumerate(f, 1):
                        try:
                            command = self.parse_line(line, line_number)
                            if command:
                                commands.append(command)
                        except ValueError as e:
                            print(f"Ошибка в строке {line_number}: {e}")
                            raise
            except Exception as e2:
                print(f"Ошибка при чтении файла: {e2}")
                raise
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            raise
        
        return commands