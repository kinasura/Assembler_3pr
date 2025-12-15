#!/usr/bin/env python3
"""
Скрипт для запуска тестов.
"""

import unittest
import sys

if __name__ == '__main__':
    # Находим все тесты в директории tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir)

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Возвращаем код выхода в зависимости от результата
    sys.exit(0 if result.wasSuccessful() else 1)