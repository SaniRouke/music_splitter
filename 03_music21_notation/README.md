# 03_music21_notation

Модуль: Перевод нот в нотную запись (music21)

## Как использовать

1. Помести файл `pitch.csv` (результат работы pitch_detection) в папку `input/` этого модуля.
2. Активируй виртуальное окружение модуля:
   ```bash
   source venv/bin/activate
   ```
3. Запусти скрипт:
   ```bash
   python music21_notation.py
   ```
4. В папке `output/` появятся файлы melody.pdf (нотная запись) и melody.mid (MIDI).

---

**Требования:**
- Python 3.10+
- music21
- numpy>=1.26.4 