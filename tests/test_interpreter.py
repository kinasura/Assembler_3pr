"""
Тесты для интерпретатора виртуальной машины.
"""

import unittest
import tempfile
import os
import xml.etree.ElementTree as ET
from pathlib import Path

# Добавляем src в путь
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vm.interpreter import VirtualMachine
from assembler.command import Command
from assembler.encoder import Encoder

class TestInterpreter(unittest.TestCase):
    """Тесты интерпретатора."""
    
    def setUp(self):
        """Настройка тестов."""
        self.vm = VirtualMachine(data_memory_size=1024, num_registers=16)
        
        # Создаем временный файл
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Очистка после тестов."""
        # Удаляем временные файлы
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_program(self, commands):
        """Создает тестовую программу из списка команд."""
        encoder = Encoder()
        binary_data = encoder.encode_commands(commands)
        
        # Сохраняем во временный файл
        temp_file = os.path.join(self.temp_dir, "test_program.bin")
        with open(temp_file, 'wb') as f:
            f.write(binary_data)
        
        return temp_file
    
    def test_load_const(self):
        """Тест команды LOAD_CONST."""
        # Создаем программу: LOAD_CONST 123, R5
        cmd = Command(158, [123, 5], 1, "158,123,5")
        program_file = self.create_test_program([cmd])
        
        # Загружаем и выполняем
        self.vm.load_program_from_file(program_file)
        self.vm.run(max_steps=1)
        
        # Проверяем результат
        self.assertEqual(self.vm.memory.get_register(5), 123)
        self.assertEqual(self.vm.memory.instructions_executed, 1)
    
    def test_read_mem(self):
        """Тест команды READ_MEM."""
        # Сначала записываем значение в память
        self.vm.memory.write_data(100, 456)
        
        # Создаем программу: READ_MEM 100, R3
        cmd = Command(17, [100, 3], 1, "17,100,3")
        program_file = self.create_test_program([cmd])
        
        # Загружаем и выполняем
        self.vm.load_program_from_file(program_file)
        self.vm.run(max_steps=1)
        
        # Проверяем результат
        self.assertEqual(self.vm.memory.get_register(3), 456)
    
    def test_write_mem(self):
        """Тест команды WRITE_MEM."""
        # Создаем программу:
        # 1. LOAD_CONST 789, R1
        # 2. LOAD_CONST 200, R2
        # 3. WRITE_MEM R2, R1
        cmd1 = Command(158, [789, 1], 1, "158,789,1")
        cmd2 = Command(158, [200, 2], 2, "158,200,2")
        cmd3 = Command(12, [2, 1], 3, "12,2,1")
        
        program_file = self.create_test_program([cmd1, cmd2, cmd3])
        
        # Загружаем и выполняем
        self.vm.load_program_from_file(program_file)
        self.vm.run(max_steps=3)
        
        # Проверяем результат
        self.assertEqual(self.vm.memory.read_data(200), 789)
    
    def test_memory_dump_xml(self):
        """Тест создания дампа памяти в XML."""
        # Записываем некоторые значения в память
        self.vm.memory.write_data(0, 123)
        self.vm.memory.write_data(1, 456)
        self.vm.memory.set_register(0, 999)
        self.vm.memory.set_register(1, 888)
        
        # Создаем дамп
        dump_file = os.path.join(self.temp_dir, "dump.xml")
        xml_str = self.vm.memory.dump_to_xml(0, 5, dump_file)
        
        # Проверяем, что файл создан
        self.assertTrue(os.path.exists(dump_file))
        
        # Парсим XML и проверяем содержимое
        tree = ET.parse(dump_file)
        root = tree.getroot()
        
        # Проверяем наличие основных элементов
        self.assertIsNotNone(root.find("system_info"))
        self.assertIsNotNone(root.find("registers"))
        self.assertIsNotNone(root.find("data_memory"))
        
        # Проверяем регистры
        registers = root.find("registers")
        reg_list = list(registers.findall("register"))
        self.assertGreaterEqual(len(reg_list), 2)
    
    def test_multiple_instructions(self):
        """Тест выполнения нескольких инструкций."""
        # Создаем программу:
        commands = [
            Command(158, [100, 0], 1, ""),
            Command(158, [200, 1], 2, ""),
            Command(12, [0, 1], 3, ""),  # memory[100] = 200
            Command(17, [100, 2], 4, ""),  # R2 = memory[100]
        ]
        
        program_file = self.create_test_program(commands)
        
        # Загружаем и выполняем
        self.vm.load_program_from_file(program_file)
        self.vm.run(max_steps=10)
        
        # Проверяем результаты
        self.assertEqual(self.vm.memory.get_register(0), 100)
        self.assertEqual(self.vm.memory.get_register(1), 200)
        self.assertEqual(self.vm.memory.get_register(2), 200)
        self.assertEqual(self.vm.memory.read_data(100), 200)
        self.assertEqual(self.vm.memory.instructions_executed, 4)

if __name__ == '__main__':
    unittest.main()