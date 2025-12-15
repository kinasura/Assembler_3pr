"""
Модель памяти виртуальной машины.
"""

from typing import List, Optional
import xml.etree.ElementTree as ET
from xml.dom import minidom

class Memory:
    """Память виртуальной машины УВМ."""
    
    def __init__(self, data_size: int = 65536, num_registers: int = 32):
        """
        Инициализация памяти.
        
        Args:
            data_size: размер памяти данных
            num_registers: количество регистров
        """
        self.data_memory = [0] * data_size  # Память данных
        self.registers = [0] * num_registers  # Регистры
        self.program_memory = []  # Память команд (будет загружена из файла)
        
        # Счетчики
        self.data_size = data_size
        self.num_registers = num_registers
        
        # Статистика
        self.instructions_executed = 0
        self.memory_accesses = 0
    
    def _to_signed32(self, value: int) -> int:
        """Преобразует 32-битное беззнаковое число в знаковое."""
        if value & 0x80000000:  # Если установлен старший бит
            return value - 0x100000000
        return value

    def _to_unsigned32(self, value: int) -> int:
        """Преобразует знаковое число в 32-битное беззнаковое."""
        return value & 0xFFFFFFFF

    def clear(self):
        """Очищает память."""
        self.data_memory = [0] * self.data_size
        self.registers = [0] * self.num_registers
        self.program_memory = []
        self.instructions_executed = 0
        self.memory_accesses = 0

    def load_program(self, program_data: bytes):
        """
        Загружает программу в память команд.

        Args:
            program_data: бинарные данные программы
        """
        self.program_memory = list(program_data)
        print(f"Загружено {len(program_data)} байт программы")

    def read_data(self, address: int) -> int:
        """Читает значение из памяти данных (возвращает знаковое число)."""
        if 0 <= address < self.data_size:
            self.memory_accesses += 1
            return self._to_signed32(self.data_memory[address])
        else:
            raise ValueError(f"Адрес памяти вне диапазона: {address}")

    def write_data(self, address: int, value: int):
        """Записывает значение в память данных (принимает знаковое число)."""
        if 0 <= address < self.data_size:
            self.memory_accesses += 1
            self.data_memory[address] = self._to_unsigned32(value)
        else:
            raise ValueError(f"Адрес памяти вне диапазона: {address}")

    def get_register(self, reg_num: int) -> int:
        """Читает значение из регистра (возвращает знаковое число)."""
        if 0 <= reg_num < self.num_registers:
            return self._to_signed32(self.registers[reg_num])
        else:
            raise ValueError(f"Номер регистра вне диапазона: {reg_num}")

    def set_register(self, reg_num: int, value: int):
        """Записывает значение в регистр (принимает знаковое число)."""
        if 0 <= reg_num < self.num_registers:
            self.registers[reg_num] = self._to_unsigned32(value)
        else:
            raise ValueError(f"Номер регистра вне диапазона: {reg_num}")

    def get_register_raw(self, reg_num: int) -> int:
        """Читает необработанное значение из регистра (беззнаковое)."""
        if 0 <= reg_num < self.num_registers:
            return self.registers[reg_num]
        else:
            raise ValueError(f"Номер регистра вне диапазона: {reg_num}")

    def set_register_raw(self, reg_num: int, value: int):
        """Записывает необработанное значение в регистр (беззнаковое)."""
        if 0 <= reg_num < self.num_registers:
            self.registers[reg_num] = value & 0xFFFFFFFF
        else:
            raise ValueError(f"Номер регистра вне диапазона: {reg_num}")

    def dump_to_xml(self, start_addr: int = 0, end_addr: Optional[int] = None,
                   file_path: str = "memory_dump.xml") -> str:
        """
        Создает дамп памяти в формате XML.

        Args:
            start_addr: начальный адрес для дампа
            end_addr: конечный адрес для дампа (None - до конца памяти)
            file_path: путь к файлу для сохранения

        Returns:
            XML-строка с дампом памяти
        """
        if end_addr is None:
            end_addr = self.data_size - 1

        # Ограничиваем диапазон
        start_addr = max(0, min(start_addr, self.data_size - 1))
        end_addr = max(start_addr, min(end_addr, self.data_size - 1))

        # Создаем XML структуру
        root = ET.Element("memory_dump")

        # Добавляем информацию о системе
        info = ET.SubElement(root, "system_info")
        ET.SubElement(info, "total_data_memory").text = str(self.data_size)
        ET.SubElement(info, "num_registers").text = str(self.num_registers)
        ET.SubElement(info, "instructions_executed").text = str(self.instructions_executed)
        ET.SubElement(info, "memory_accesses").text = str(self.memory_accesses)

        # Добавляем регистры
        registers_elem = ET.SubElement(root, "registers")
        for i in range(self.num_registers):
            reg_elem = ET.SubElement(registers_elem, "register")
            reg_elem.set("id", str(i))
            signed_val = self.get_register(i)
            unsigned_val = self.registers[i]
            reg_elem.set("value_signed", str(signed_val))
            reg_elem.set("value_unsigned", str(unsigned_val))
            reg_elem.set("value_hex", f"0x{unsigned_val:08X}")

        # Добавляем память данных
        memory_elem = ET.SubElement(root, "data_memory")
        memory_elem.set("start_address", str(start_addr))
        memory_elem.set("end_address", str(end_addr))

        for addr in range(start_addr, end_addr + 1):
            cell_elem = ET.SubElement(memory_elem, "cell")
            cell_elem.set("address", str(addr))
            signed_val = self.read_data(addr)
            unsigned_val = self.data_memory[addr]
            cell_elem.set("value_signed", str(signed_val))
            cell_elem.set("value_unsigned", str(unsigned_val))
            cell_elem.set("value_hex", f"0x{unsigned_val:08X}")

        # Форматируем XML
        xml_str = ET.tostring(root, encoding='unicode')

        # Используем minidom для красивого форматирования
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="  ")

        # Сохраняем в файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)

        print(f"Дамп памяти сохранен в {file_path}")
        return pretty_xml

    def print_status(self):
        """Выводит статус памяти и регистров."""
        print("\n" + "=" * 60)
        print("СТАТУС ВИРТУАЛЬНОЙ МАШИНЫ")
        print("=" * 60)
        print(f"Память данных: {self.data_size} ячеек")
        print(f"Регистры: {self.num_registers}")
        print(f"Выполнено инструкций: {self.instructions_executed}")
        print(f"Обращений к памяти: {self.memory_accesses}")

        # Показываем ненулевые регистры
        print("\nРегистры (ненулевые, знаковые значения):")
        for i in range(self.num_registers):
            val = self.get_register(i)
            if val != 0:
                unsigned_val = self.registers[i]
                print(f"  R{i:2}: {val:10} (0x{unsigned_val:08X})") 