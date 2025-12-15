"""
Модель команды ассемблера.
"""

from dataclasses import dataclass
from typing import List, Optional


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