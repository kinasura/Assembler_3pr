"""
Интеграционные тесты: ассемблер + интерпретатор.
"""

import unittest
import tempfile
import os
import subprocess
import sys

class TestIntegration(unittest.TestCase):
    """Интеграционные тесты."""
    
    def setUp(self):
        """Настройка тестов."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Добавляем src в путь
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    
    def tearDown(self):
        """Очистка после тестов."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_assembler_to_interpreter(self):
        """Тест полного цикла: ассемблер -> интерпретатор."""
        # 1. Создаем исходный файл ассемблера
        asm_file = os.path.join(self.temp_dir, "test.asm")
        with open(asm_file, 'w', encoding='utf-8') as f:
            f.write("158,100,0\n")
            f.write("158,200,1\n")
            f.write("12,0,1\n")
            f.write("17,100,2\n")
        
        # 2. Ассемблируем
        bin_file = os.path.join(self.temp_dir, "test.bin")
        
        # Импортируем и запускаем ассемблер
        from assembler.main import main as assembler_main
        
        # Сохраняем оригинальные аргументы
        original_argv = sys.argv
        
        try:
            # Устанавливаем аргументы для ассемблера
            sys.argv = ['assembler.py', asm_file, bin_file]
            
            # Запускаем ассемблер
            assembler_main()
        finally:
            # Восстанавливаем аргументы
            sys.argv = original_argv
        
        # Проверяем, что бинарный файл создан
        self.assertTrue(os.path.exists(bin_file))
        
        # 3. Запускаем интерпретатор
        dump_file = os.path.join(self.temp_dir, "dump.xml")
        
        from vm.interpreter import VirtualMachine
        vm = VirtualMachine()
        vm.load_program_from_file(bin_file)
        vm.run()
        
        # Проверяем результаты
        self.assertEqual(vm.memory.get_register(0), 100)
        self.assertEqual(vm.memory.get_register(1), 200)
        self.assertEqual(vm.memory.get_register(2), 200)
        
        # 4. Создаем дамп
        vm.memory.dump_to_xml(0, 150, dump_file)
        self.assertTrue(os.path.exists(dump_file))

if __name__ == '__main__':
    unittest.main()