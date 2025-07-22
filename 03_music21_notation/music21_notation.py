import os
import csv
from music21 import note, stream

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(BASE_DIR)
input_dir = os.path.join(project_root, 'output')
output_dir = os.path.join(BASE_DIR, 'output')
os.makedirs(output_dir, exist_ok=True)

input_csv = os.path.join(input_dir, 'pitch.csv')
if not os.path.isfile(input_csv):
    print(f'Файл {input_csv} не найден! Положите pitch.csv в папку input.')
    exit(1)

notes = []
with open(input_csv, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        start = float(row['start_time'])
        end = float(row['end_time'])
        dur = end - start
        # Try different possible column names for note
        if 'note_name' in row:
            n = row['note_name']
        elif 'note' in row:
            n = row['note']
        else:
            print(f"Error: No note column found. Available columns: {list(row.keys())}")
            exit(1)
        notes.append((n, dur))

# Создаём поток нот
melody = stream.Stream()
for n, dur in notes:
    melody.append(note.Note(n, quarterLength=dur))

# Сохраняем в PDF и MIDI
pdf_path = os.path.join(output_dir, 'melody.pdf')
midi_path = os.path.join(output_dir, 'melody.mid')
try:
    melody.write('pdf', fp=pdf_path)
    print(f'PDF нотной записи сохранён в {pdf_path}')
except Exception as e:
    print(f'Не удалось сохранить PDF: {e}')
melody.write('midi', fp=midi_path)
print(f'MIDI файл сохранён в {midi_path}') 