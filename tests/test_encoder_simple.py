"""
Упрощенные тесты для кодировщика команд (без Unicode символов).
"""

import unittest
from src.assembler.command import Command
from src.assembler.encoder import Encoder

class TestEncoderSimple(unittest.TestCase):
    """Упрощенные тесты кодировщика команд."""
    
    def setUp(self):
        """Настройка тестов."""
        self.encoder = Encoder()
    
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
    
    def test_encode_basic(self):
        """Базовый тест кодирования."""
        commands = [
            Command(158, [100, 5], 1, ""),
            Command(17, [200, 10], 2, ""),
            Command(12, [1, 2], 3, ""),
            Command(214, [50, 3, 4], 4, ""),
        ]
        
        # Кодируем все команды
        encoded = self.encoder.encode_commands(commands)
        
        # Проверяем общий размер
        expected_size = 6 + 5 + 3 + 5  # 19 байт
        self.assertEqual(len(encoded), expected_size)
    
    def test_encode_individual(self):
        """Тест кодирования отдельных команд."""
        # LOAD_CONST
        cmd1 = Command(158, [679, 28], 1, "")
        self.assertEqual(len(cmd1.encode()), 6)
        
        # READ_MEM
        cmd2 = Command(17, [356, 24], 2, "")
        self.assertEqual(len(cmd2.encode()), 5)
        
        # WRITE_MEM
        cmd3 = Command(12, [5, 3], 3, "")
        self.assertEqual(len(cmd3.encode()), 3)
        
        # ABS
        cmd4 = Command(214, [95, 2, 27], 4, "")
        self.assertEqual(len(cmd4.encode()), 5)

if __name__ == '__main__':
    unittest.main()