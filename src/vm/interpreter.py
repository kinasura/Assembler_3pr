"""
Интерпретатор виртуальной машины УВМ.
"""

import sys
from pathlib import Path
from .memory import Memory
from .decoder import Decoder, DecodedInstruction
from .alu import ALU  # Импортируем АЛУ

class VirtualMachine:
    """Виртуальная машина УВМ."""

    def __init__(self, data_memory_size: int = 65536, num_registers: int = 32):
        """
        Инициализация виртуальной машины.

        Args:
            data_memory_size: размер памяти данных
            num_registers: количество регистров
        """
        self.memory = Memory(data_memory_size, num_registers)
        self.alu = ALU()  # Создаем экземпляр АЛУ
        self.ip = 0  # Instruction Pointer
        self.running = False
        self.max_instructions = 100000  # Защита от бесконечного цикла

        # Флаги для отладки
        self.debug = False
        self.step_by_step = False
        self.show_alu_flags = False  # Показывать флаги АЛУ

    def load_program_from_file(self, file_path: str):
        """
        Загружает программу из бинарного файла.

        Args:
            file_path: путь к бинарному файлу
        """
        try:
            with open(file_path, 'rb') as f:
                program_data = f.read()

            self.memory.load_program(program_data)
            self.ip = 0
            print(f"Программа загружена из {file_path}")
            print(f"Размер программы: {len(program_data)} байт")

        except FileNotFoundError:
            print(f"Ошибка: файл не найден: {file_path}")
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка загрузки программы: {e}")
            sys.exit(1)

    def execute_load_const(self, const: int, reg_addr: int):
        """Выполняет команду LOAD_CONST."""
        self.memory.set_register(reg_addr, const)
        if self.debug:
            print(f"  LOAD_CONST: R{reg_addr} = {const}")

    def execute_read_mem(self, mem_addr: int, reg_addr: int):
        """Выполняет команду READ_MEM."""
        value = self.memory.read_data(mem_addr)
        self.memory.set_register(reg_addr, value)
        if self.debug:
            print(f"  READ_MEM: R{reg_addr} = memory[{mem_addr}] = {value}")

    def execute_write_mem(self, reg_addr_dest: int, reg_addr_src: int):
        """Выполняет команду WRITE_MEM."""
        # Адрес берется из регистра reg_addr_dest
        address = self.memory.get_register(reg_addr_dest)

        # Проверяем, что адрес неотрицательный
        if address < 0:
            raise ValueError(f"Адрес памяти не может быть отрицательным: {address}")

        value = self.memory.get_register(reg_addr_src)
        self.memory.write_data(address, value)
        if self.debug:
            print(f"  WRITE_MEM: memory[{address}] = R{reg_addr_src} = {value}")

    def execute_abs(self, offset: int, base_reg: int, src_reg: int):
        """Выполняет команду ABS с использованием АЛУ."""
        # Получаем значение из регистра-источника
        value = self.memory.get_register(src_reg)

        # Вычисляем абсолютное значение с помощью АЛУ
        abs_value = self.alu.abs(value)

        # Вычисляем адрес назначения
        base_address = self.memory.get_register(base_reg)
        address = base_address + offset

        # Проверяем границы
        if address < 0:
            raise ValueError(f"Адрес памяти не может быть отрицательным: {address}")

        if 0 <= address < self.memory.data_size:
            self.memory.write_data(address, abs_value)
            if self.debug:
                print(f"  ABS: memory[{address}] = abs(R{src_reg}) = {abs_value}")
                if self.show_alu_flags:
                    print(f"       Флаги АЛУ: {self.alu.get_status_string()}")
        else:
            raise ValueError(f"Адрес {address} вне диапазона памяти [0, {self.memory.data_size-1}]")

    def execute_instruction(self, instr: DecodedInstruction):
        """Выполняет одну инструкцию."""
        if instr.opcode == 158:  # LOAD_CONST
            self.execute_load_const(instr.args[0], instr.args[1])
        elif instr.opcode == 17:  # READ_MEM
            self.execute_read_mem(instr.args[0], instr.args[1])
        elif instr.opcode == 12:  # WRITE_MEM
            self.execute_write_mem(instr.args[0], instr.args[1])
        elif instr.opcode == 214:  # ABS
            self.execute_abs(instr.args[0], instr.args[1], instr.args[2])
        else:
            raise ValueError(f"Неизвестный код операции: {instr.opcode}")

        self.memory.instructions_executed += 1

    def run(self, max_steps: int = 0):
        """
        Запускает выполнение программы.

        Args:
            max_steps: максимальное количество инструкций для выполнения (0 - без ограничений)
        """
        if not self.memory.program_memory:
            print("Ошибка: программа не загружена")
            return

        self.running = True
        instructions_executed = 0

        print(f"\nЗапуск выполнения программы...")
        print(f"Начальный IP: 0x{self.ip:04X}")

        while self.running and self.ip < len(self.memory.program_memory):
            try:
                # Декодируем инструкцию
                instr = Decoder.decode_instruction(
                    bytes(self.memory.program_memory),
                    self.ip
                )

                # Выводим информацию в режиме отладки
                if self.debug:
                    Decoder.print_instruction(instr, self.ip)

                # Выполняем инструкцию
                self.execute_instruction(instr)

                # Переходим к следующей инструкции
                self.ip += instr.size
                instructions_executed += 1

                # Проверяем ограничение по шагам
                if max_steps > 0 and instructions_executed >= max_steps:
                    print(f"\nДостигнут лимит инструкций: {max_steps}")
                    break

                # Пошаговый режим
                if self.step_by_step:
                    input("Нажмите Enter для следующей инструкции...")

                # Защита от бесконечного цикла
                if instructions_executed > self.max_instructions:
                    print(f"\nПревышен лимит инструкций: {self.max_instructions}")
                    break

            except (ValueError, IndexError) as e:
                print(f"\nОшибка выполнения инструкции по адресу 0x{self.ip:04X}: {e}")
                break
            except KeyboardInterrupt:
                print("\nВыполнение прервано пользователем")
                break

        self.running = False
        print(f"\nВыполнение завершено.")
        print(f"Выполнено инструкций: {instructions_executed}")
        print(f"Финальный IP: 0x{self.ip:04X}")

        # Показываем флаги АЛУ, если нужно
        if self.show_alu_flags:
            print(f"Флаги АЛУ: {self.alu.get_status_string()}")
    
    def dump_memory(self, start_addr: int = 0, end_addr: int = 100, 
                   file_path: str = "memory_dump.xml"):
        """Создает дамп памяти."""
        self.memory.dump_to_xml(start_addr, end_addr, file_path)