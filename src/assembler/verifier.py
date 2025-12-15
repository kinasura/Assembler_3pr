"""
Модуль для проверки корректности кодирования.
"""

class Verifier:
    """Верификатор кодирования команд."""
    
    @staticmethod
    def verify_test_cases():
        """Проверяет тестовые случаи из спецификации."""
        test_cases = [
            {
                'name': 'LOAD_CONST',
                'command': (158, [679, 28]),
                'expected_bytes': bytes([0x9E, 0xA7, 0x02, 0x00, 0x00, 0x1C]),
                'expected_hex': '9e, a7, 02, 00, 00, 1c'
            },
            {
                'name': 'READ_MEM',
                'command': (17, [356, 24]),
                'expected_bytes': bytes([0x11, 0x64, 0x81, 0x89, 0x69]),
                'expected_hex': '11, 64, 81, 89, 69'
            },
            {
                'name': 'WRITE_MEM',
                'command': (12, [5, 3]),
                'expected_bytes': bytes([0x0C, 0xA8, 0x00]),  # Из нашего расчета
                'expected_hex': '0c, a8, 00'
            },
            {
                'name': 'ABS',
                'command': (214, [95, 2, 27]),
                'expected_bytes': bytes([0xD6, 0x5F, 0x00, 0x40, 0x1B]),  # Из нашего расчета
                'expected_hex': 'd6, 5f, 00, 40, 1b'
            }
        ]
        
        from .command import Command
        
        print("Проверка тестовых случаев из спецификации:")
        print("=" * 60)
        
        all_passed = True
        for test_case in test_cases:
            name = test_case['name']
            opcode, args = test_case['command']
            expected_bytes = test_case['expected_bytes']
            expected_hex = test_case['expected_hex']
            
            try:
                command = Command(opcode, args, 0, "")
                actual_bytes = command.encode()
                actual_hex = command.to_hex_string()
                
                if actual_bytes == expected_bytes:
                    print(f"✓ {name}: кодирование верное")
                    print(f"  Байты: {actual_hex}")
                else:
                    print(f"✗ {name}: ошибка кодирования")
                    print(f"  Ожидалось: {expected_bytes.hex(', ')}")
                    print(f"  Получено:  {actual_bytes.hex(', ')}")
                    all_passed = False
                    
            except Exception as e:
                print(f"✗ {name}: исключение - {e}")
                all_passed = False
        
        print("=" * 60)
        if all_passed:
            print("Все тесты пройдены успешно!")
        else:
            print("Некоторые тесты не пройдены.")
        
        return all_passed