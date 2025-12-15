"""
Декодер команд для виртуальной машины.
"""

from typing import Tuple
from dataclasses import dataclass

@dataclass
class DecodedInstruction:
    """Декодированная инструкция."""
    opcode: int
    args: Tuple[int, ...]
    size: int  # Размер команды в байтах

class Decoder:
    """Декодер команд УВМ."""

    @staticmethod
    def _sign_extend(value: int, bits: int) -> int:
        """Расширяет знак для signed чисел."""
        if value & (1 << (bits - 1)):  # Если старший бит установлен
            # Расширяем знак до 32 бит
            mask = (1 << bits) - 1
            value_unsigned = value & mask
            # Для отрицательного числа
            return value_unsigned - (1 << bits)
        return value

    @staticmethod
    def _to_signed32(value: int) -> int:
        """Преобразует 32-битное беззнаковое в знаковое."""
        if value & 0x80000000:
            return value - 0x100000000
        return value

    @staticmethod
    def decode_instruction(data: bytes, ip: int) -> DecodedInstruction:
        """
        Декодирует инструкцию из бинарных данных.

        Args:
            data: все бинарные данные программы
            ip: текущий указатель инструкции

        Returns:
            DecodedInstruction: декодированная инструкция
        """
        if ip >= len(data):
            raise IndexError(f"Указатель инструкции {ip} вне диапазона программы")

        # Читаем первый байт (код операции)
        opcode = data[ip]

        # Определяем тип команды и декодируем
        if opcode == 158:  # LOAD_CONST - 6 байт
            if ip + 6 > len(data):
                raise ValueError("Недостаточно данных для команды LOAD_CONST")

            # Извлекаем байты
            bytes_data = data[ip:ip+6]

            # Декодируем: (c << 38) | (b << 8) | a
            value = int.from_bytes(bytes_data, byteorder='little')

            # Извлекаем поля
            a = value & 0xFF  # opcode
            b_raw = (value >> 8) & 0x3FFFFFFF  # 30 бит (беззнаковое)
            c = (value >> 38) & 0x1F  # 5 бит

            # Расширяем знак для 30-битного числа
            b_signed = Decoder._sign_extend(b_raw, 30)

            return DecodedInstruction(opcode=a, args=(b_signed, c), size=6)

        elif opcode == 17:  # READ_MEM - 5 байт
            if ip + 5 > len(data):
                raise ValueError("Недостаточно данных для команды READ_MEM")

            bytes_data = data[ip:ip+5]
            value = int.from_bytes(bytes_data, byteorder='little')

            a = value & 0xFF  # opcode
            b = (value >> 8) & 0x3FFFFFF  # 26 бит (адрес памяти - беззнаковый)
            c = (value >> 34) & 0x1F  # 5 бит

            return DecodedInstruction(opcode=a, args=(b, c), size=5)

        elif opcode == 12:  # WRITE_MEM - 3 байта
            if ip + 3 > len(data):
                raise ValueError("Недостаточно данных для команды WRITE_MEM")

            bytes_data = data[ip:ip+3]
            value = int.from_bytes(bytes_data, byteorder='little')

            a = value & 0xFF  # opcode
            b = (value >> 8) & 0x1F  # 5 бит
            c = (value >> 13) & 0x1F  # 5 бит

            return DecodedInstruction(opcode=a, args=(b, c), size=3)

        elif opcode == 214:  # ABS - 5 байт
            if ip + 5 > len(data):
                raise ValueError("Недостаточно данных для команды ABS")

            bytes_data = data[ip:ip+5]
            value = int.from_bytes(bytes_data, byteorder='little')

            a = value & 0xFF  # opcode
            b_raw = (value >> 8) & 0xFFFF  # 16 бит (беззнаковое)
            c = (value >> 24) & 0x1F  # 5 бит
            d = (value >> 29) & 0x1F  # 5 бит

            # Расширяем знак для 16-битного смещения
            b_signed = Decoder._sign_extend(b_raw, 16)

            return DecodedInstruction(opcode=a, args=(b_signed, c, d), size=5)
        
        else:
            raise ValueError(f"Неизвестный код операции: {opcode}")
    
    @staticmethod
    def print_instruction(instr: DecodedInstruction, ip: int):
        """Выводит информацию об инструкции."""
        if instr.opcode == 158:
            print(f"[{ip:04X}] LOAD_CONST const={instr.args[0]}, reg={instr.args[1]}")
        elif instr.opcode == 17:
            print(f"[{ip:04X}] READ_MEM  addr={instr.args[0]}, reg={instr.args[1]}")
        elif instr.opcode == 12:
            print(f"[{ip:04X}] WRITE_MEM reg_addr={instr.args[0]}, reg_val={instr.args[1]}")
        elif instr.opcode == 214:
            print(f"[{ip:04X}] ABS       offset={instr.args[0]}, base_reg={instr.args[1]}, src_reg={instr.args[2]}")