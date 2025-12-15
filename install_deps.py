#!/usr/bin/env python3
"""
Скрипт для установки зависимостей.
"""

import subprocess
import sys

def install_requirements():
    """Устанавливает зависимости из requirements.txt."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Зависимости успешно установлены!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке зависимостей: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()