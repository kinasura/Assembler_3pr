"""
Арифметико-логическое устройство (АЛУ) виртуальной машины.
"""

class ALU:
    """Арифметико-логическое устройство УВМ."""
    
    def __init__(self):
        """Инициализация АЛУ."""
        # Флаги состояния
        self.zero_flag = False
        self.negative_flag = False
        self.overflow_flag = False
        self.carry_flag = False
    
    def reset_flags(self):
        """Сбрасывает все флаги."""
        self.zero_flag = False
        self.negative_flag = False
        self.overflow_flag = False
        self.carry_flag = False
    
    def abs(self, value: int) -> int:
        """
        Вычисляет абсолютное значение.
        
        Args:
            value: входное значение (знаковое 32-битное)
            
        Returns:
            Абсолютное значение (положительное или ноль)
        """
        self.reset_flags()
        
        # Вычисляем абсолютное значение
        result = abs(value)
        
        # Устанавливаем флаги
        self.zero_flag = (result == 0)
        self.negative_flag = (result < 0)  # Для abs всегда False, но оставим
        
        # Проверка на переполнение (если входное значение было минимальным отрицательным)
        if value == -0x80000000:  # -2^31
            self.overflow_flag = True
            # В реальных системах abs(-2^31) = 2^31 вызывает переполнение
            # но в нашем случае ограничимся максимальным положительным 2^31-1
            result = 0x7FFFFFFF
        
        return result
    
    def add(self, a: int, b: int) -> int:
        """Сложение двух чисел (заглушка для будущего расширения)."""
        self.reset_flags()
        result = (a + b) & 0xFFFFFFFF
        return self._to_signed32(result)
    
    def subtract(self, a: int, b: int) -> int:
        """Вычитание (заглушка для будущего расширения)."""
        self.reset_flags()
        result = (a - b) & 0xFFFFFFFF
        return self._to_signed32(result)
    
    def multiply(self, a: int, b: int) -> int:
        """Умножение (заглушка для будущего расширения)."""
        self.reset_flags()
        result = (a * b) & 0xFFFFFFFF
        return self._to_signed32(result)
    
    def logical_and(self, a: int, b: int) -> int:
        """Логическое И (заглушка для будущего расширения)."""
        self.reset_flags()
        result = a & b
        return self._to_signed32(result)
    
    def _to_signed32(self, value: int) -> int:
        """Преобразует 32-битное беззнаковое в знаковое."""
        if value & 0x80000000:
            return value - 0x100000000
        return value
    
    def get_status_string(self) -> str:
        """Возвращает строку состояния флагов."""
        flags = []
        if self.zero_flag: flags.append("Z")
        if self.negative_flag: flags.append("N")
        if self.overflow_flag: flags.append("V")
        if self.carry_flag: flags.append("C")
        
        if not flags:
            return "[ ]"
        return f"[{''.join(flags)}]"