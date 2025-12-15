"""
Модуль для кодирования команд в машинный код.
"""

class Encoder:
    """Кодировщик команд в бинарное представление."""
    
    @staticmethod
    def encode_commands(commands):
        """Кодирует список команд в бинарные данные."""
        binary_data = bytearray()
        
        for command in commands:
            try:
                encoded = command.encode()
                binary_data.extend(encoded)
            except Exception as e:
                raise ValueError(f"Ошибка кодирования команды в строке {command.line_number}: {e}")
        
        return bytes(binary_data)