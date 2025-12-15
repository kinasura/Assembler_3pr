"""
Тесты для кодировщика команд.
"""

import unittest
from src.assembler.command import Command
from src.assembler.encoder import Encoder

class TestEncoder(unittest.TestCase):
    """Тесты кодировщика команд."""
    
    def setUp(self):
        """Настройка тестов."""
        self.encoder = Encoder()
    
    def test_encode_load_const(self):
        """Тест кодирования команды LOAD_CONST."""
        command = Command(opcode=158, args=[679, 28], line_number=1, raw_line="158,679,28")
        
        # Кодируем команду
        encoded = command.encode()
        
        # Проверяем размер
        self.assertEqual(len(encoded), 6)
        
        # Проверяем hex-строку
        hex_str = command.to_hex_string()
        self.assertEqual(len(hex_str.split(', ')), 6)

    def test_encode_read_mem(self):
        """Тест кодирования команды READ_MEM."""
        command = Command(opcode=17, args=[356, 24], line_number=1, raw_line="17,356,24")

        # Кодируем команду
        encoded = command.encode()

        # Проверяем размер
        self.assertEqual(len(encoded), 5)

    def test_encode_write_mem(self):
        """Тест кодирования команды WRITE_MEM."""
        command = Command(opcode=12, args=[5, 3], line_number=1, raw_line="12,5,3")

        # Кодируем команду
        encoded = command.encode()

        # Проверяем размер
        self.assertEqual(len(encoded), 3)

    def test_encode_abs(self):
        """Тест кодирования команды ABS."""
        command = Command(opcode=214, args=[95, 2, 27], line_number=1, raw_line="214,95,2,27")

        # Кодируем команду
        encoded = command.encode()

        # Проверяем размер
        self.assertEqual(len(encoded), 5)

    def test_encode_multiple_commands(self):
        """Тест кодирования нескольких команд."""
        commands = [
            Command(158, [679, 28], 1, ""),
            Command(17, [356, 24], 2, ""),
            Command(12, [5, 3], 3, ""),
            Command(214, [95, 2, 27], 4, ""),
        ]

        # Кодируем все команды
        encoded = self.encoder.encode_commands(commands)

        # Проверяем общий размер
        expected_size = 6 + 5 + 3 + 5  # 19 байт
        self.assertEqual(len(encoded), expected_size)

    def test_command_sizes(self):
        """Тест получения размеров команд."""
        test_cases = [
            (Command(158, [100, 5], 1, ""), 6),
            (Command(17, [100, 5], 1, ""), 5),
            (Command(12, [5, 3], 1, ""), 3),
            (Command(214, [10, 5, 3], 1, ""), 5),
        ]

        for command, expected_size in test_cases:
            self.assertEqual(command.get_size(), expected_size)

if __name__ == '__main__':
    unittest.main()