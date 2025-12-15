#!/usr/bin/env python3
"""
Удобный скрипт для запуска ассемблера.
"""

import sys
import os

# Добавляем src в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from assembler.main import main

if __name__ == '__main__':
    main()