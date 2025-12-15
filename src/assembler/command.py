"""
Модель команды ассемблера.
"""

from dataclasses import dataclass
from typing import List
import struct


@dataclass
class Command:
    """Представление команды ассемблера."""
    opcode: int
    args: List[int]
    line_number: int
    raw_line: str

    def __post_init__(self):
        """Валидация команды после инициализации."""
        self.validate()

    def validate(self):
        """Проверка корректности команды."""
        if self.opcode == 158:  # LOAD_CONST
            if len(self.args) != 2:
                raise ValueError(f"Команда 158 требует 2 аргумента, получено {len(self.args)}")
            if self.args[0] < 0 or self.args[0] > 0x3FFFFFFF:  # 30 бит
                raise ValueError(f"Константа {self.args[0]} выходит за пределы 30 бит")
            if self.args[1] < 0 or self.args[1] > 31:
                raise ValueError(f"Адрес регистра {self.args[1]} должен быть в диапазоне 0-31")

        elif self.opcode == 17:  # READ_MEM
            if len(self.args) != 2:
                raise ValueError(f"Команда 17 требует 2 аргумента, получено {len(self.args)}")
            if self.args[0] < 0 or self.args[0] > 0x3FFFFFF:  # 26 бит
                raise ValueError(f"Адрес памяти {self.args[0]} выходит за пределы 26 бит")
            if self.args[1] < 0 or self.args[1] > 31:
                raise ValueError(f"Адрес регистра {self.args[1]} должен быть в диапазоне 0-31")

        elif self.opcode == 12:  # WRITE_MEM
            if len(self.args) != 2:
                raise ValueError(f"Команда 12 требует 2 аргумента, получено {len(self.args)}")
            if not (0 <= self.args[0] <= 31 and 0 <= self.args[1] <= 31):
                raise ValueError(f"Адреса регистров должны быть в диапазоне 0-31")

        elif self.opcode == 214:  # ABS
            if len(self.args) != 3:
                raise ValueError(f"Команда 214 требует 3 аргумента, получено {len(self.args)}")
            if self.args[0] < 0 or self.args[0] > 0xFFFF:  # 16 бит
                raise ValueError(f"Смещение {self.args[0]} выходит за пределы 16 бит")
            if not (0 <= self.args[1] <= 31 and 0 <= self.args[2] <= 31):
                raise ValueError(f"Адреса регистров должны быть в диапазоне 0-31")

        else:
            raise ValueError(f"Неизвестный код операции: {self.opcode}")

    def to_intermediate_format(self) -> str:
        """Преобразование в промежуточное представление (формат полей)."""
        if self.opcode == 158:
            return f"A={self.opcode}, B={self.args[0]}, C={self.args[1]}"
        elif self.opcode == 17:
            return f"A={self.opcode}, B={self.args[0]}, C={self.args[1]}"
        elif self.opcode == 12:
            return f"A={self.opcode}, B={self.args[0]}, C={self.args[1]}"
        elif self.opcode == 214:
            return f"A={self.opcode}, B={self.args[0]}, C={self.args[1]}, D={self.args[2]}"
        return ""

    def get_size(self) -> int:
        """Возвращает размер команды в байтах."""
        if self.opcode == 158:
            return 6
        elif self.opcode == 17:
            return 5
        elif self.opcode == 12:
            return 3
        elif self.opcode == 214:
            return 5
        return 0

    def encode(self) -> bytes:
        """Кодирует команду в бинарное представление."""
        if self.opcode == 158:  # LOAD_CONST - 6 байт
            # Формат: A (8 бит), B (30 бит), C (5 бит)
            a = self.opcode & 0xFF
            b = self.args[0] & 0x3FFFFFFF  # 30 бит
            c = self.args[1] & 0x1F  # 5 бит

            # Упаковка: (c << 38) | (b << 8) | a
            value = (c << 38) | (b << 8) | a
            return value.to_bytes(6, byteorder='little')

        elif self.opcode == 17:  # READ_MEM - 5 байт
            # Формат: A (8 бит), B (26 бит), C (5 бит)
            a = self.opcode & 0xFF
            b = self.args[0] & 0x3FFFFFF  # 26 бит
            c = self.args[1] & 0x1F  # 5 бит

            # Упаковка: (c << 34) | (b << 8) | a
            value = (c << 34) | (b << 8) | a
            return value.to_bytes(5, byteorder='little')

        elif self.opcode == 12:  # WRITE_MEM - 3 байта
            # Формат: A (8 бит), B (5 бит), C (5 бит)
            a = self.opcode & 0xFF
            b = self.args[0] & 0x1F  # 5 бит
            c = self.args[1] & 0x1F  # 5 бит

            # Упаковка: (c << 13) | (b << 8) | a
            value = (c << 13) | (b << 8) | a
            return value.to_bytes(3, byteorder='little')

        elif self.opcode == 214:  # ABS - 5 байт
            # Формат: A (8 бит), B (16 бит), C (5 бит), D (5 бит)
            a = self.opcode & 0xFF
            b = self.args[0] & 0xFFFF  # 16 бит
            c = self.args[1] & 0x1F  # 5 бит
            d = self.args[2] & 0x1F  # 5 бит

            # Упаковка: (d << 29) | (c << 24) | (b << 8) | a
            value = (d << 29) | (c << 24) | (b << 8) | a
            return value.to_bytes(5, byteorder='little')

        else:
            raise ValueError(f"Кодирование не поддерживается для кода операции: {self.opcode}")

    def to_hex_string(self) -> str:
        """Возвращает hex-представление команды."""
        binary_data = self.encode()
        hex_bytes = [f"{byte:02x}" for byte in binary_data]
        return ", ".join(hex_bytes)

    def to_test_format(self) -> str:
        """Возвращает представление в тестовом формате (как в спецификации)."""
        binary_data = self.encode()
        hex_bytes = [f"вх{byte:02X}" for byte in binary_data]
        return ", ".join(hex_bytes)