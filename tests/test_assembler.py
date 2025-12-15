"""
Тесты для ассемблера УВМ.
"""

import unittest
import tempfile
import os
from pathlib import Path
from src.assembler.parser import Parser
from src.assembler.command import Command

class TestAssembler(unittest.TestCase):
    """Тесты ассемблера."""
    
    def setUp(self):
        """Настройка тестов."""
        self.parser = Parser()
    
    def test_parse_load_const(self):
        """Тест парсинга команды LOAD_CONST."""
        # Создаем временный файл с командой
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False, encoding='utf-8') as f:
            f.write("158,679,28\n")
            temp_file = f.name

        try:
            commands = self.parser.parse_file(temp_file)
            self.assertEqual(len(commands), 1)
            command = commands[0]

            self.assertEqual(command.opcode, 158)
            self.assertEqual(command.args, [679, 28])
            self.assertEqual(command.line_number, 1)
            self.assertEqual(command.raw_line, "158,679,28")

            # Проверяем промежуточное представление
            self.assertEqual(command.to_intermediate_format(), "A=158, B=679, C=28")

        finally:
            os.unlink(temp_file)

    def test_parse_multiple_commands(self):
        """Тест парсинга нескольких команд."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False, encoding='utf-8') as f:
            f.write("158,100,0\n")
            f.write("17,500,1\n")
            f.write("12,0,2\n")
            f.write("214,10,3,4\n")
            temp_file = f.name

        try:
            commands = self.parser.parse_file(temp_file)
            self.assertEqual(len(commands), 4)

            # Проверяем первую команду
            self.assertEqual(commands[0].opcode, 158)
            self.assertEqual(commands[0].args, [100, 0])

            # Проверяем вторую команду
            self.assertEqual(commands[1].opcode, 17)
            self.assertEqual(commands[1].args, [500, 1])

            # Проверяем третью команду
            self.assertEqual(commands[2].opcode, 12)
            self.assertEqual(commands[2].args, [0, 2])

            # Проверяем четвертую команду
            self.assertEqual(commands[3].opcode, 214)
            self.assertEqual(commands[3].args, [10, 3, 4])

        finally:
            os.unlink(temp_file)

    def test_parse_with_comments(self):
        """Тест парсинга с комментариями."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False, encoding='utf-8') as f:
            # Используем только ASCII символы для комментариев
            f.write("158,679,28    ; Load constant\n")
            f.write("; This is a comment\n")
            f.write("\n")  # Пустая строка
            f.write("17,356,24     ; Read from memory\n")
            temp_file = f.name
        
        try:
            commands = self.parser.parse_file(temp_file)
            self.assertEqual(len(commands), 2)
            
            self.assertEqual(commands[0].opcode, 158)
            self.assertEqual(commands[0].args, [679, 28])
            
            self.assertEqual(commands[1].opcode, 17)
            self.assertEqual(commands[1].args, [356, 24])
        
        finally:
            os.unlink(temp_file)
    
    def test_command_validation(self):
        """Тест валидации команд."""
        # Корректная команда
        command = Command(opcode=158, args=[679, 28], line_number=1, raw_line="158,679,28")
        # Не должно вызывать исключения
        
        # Некорректный код операции
        with self.assertRaises(ValueError):
            Command(opcode=999, args=[1, 2], line_number=1, raw_line="999,1,2")
        
        # LOAD_CONST: константа слишком большая
        with self.assertRaises(ValueError):
            Command(opcode=158, args=[0x40000000, 10], line_number=1, raw_line="158,1073741824,10")
        
        # LOAD_CONST: адрес регистра слишком большой
        with self.assertRaises(ValueError):
            Command(opcode=158, args=[100, 32], line_number=1, raw_line="158,100,32")
        
        # READ_MEM: адрес памяти слишком большой
        with self.assertRaises(ValueError):
            Command(opcode=17, args=[0x4000000, 10], line_number=1, raw_line="17,67108864,10")
        
        # ABS: смещение слишком большое
        with self.assertRaises(ValueError):
            Command(opcode=214, args=[0x10000, 5, 10], line_number=1, raw_line="214,65536,5,10")
    
    def test_to_intermediate_format(self):
        """Тест преобразования в промежуточное представление."""
        test_cases = [
            (Command(158, [679, 28], 1, ""), "A=158, B=679, C=28"),
            (Command(17, [356, 24], 1, ""), "A=17, B=356, C=24"),
            (Command(12, [5, 3], 1, ""), "A=12, B=5, C=3"),
            (Command(214, [95, 2, 27], 1, ""), "A=214, B=95, C=2, D=27"),
        ]
        
        for command, expected in test_cases:
            self.assertEqual(command.to_intermediate_format(), expected)

if __name__ == '__main__':
    unittest.main()