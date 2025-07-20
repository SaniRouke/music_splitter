import os
import librosa
import numpy as np
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(BASE_DIR, 'input')
output_dir = os.path.join(BASE_DIR, 'output')
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

input_audio = input(f'Введите имя аудиофайла из папки input (например, vocals.wav): ').strip()
input_path = os.path.join(input_dir, input_audio)

if not os.path.isfile(input_path):
    print(f'Файл {input_path} не найден! Положите его в папку input.')
    exit(1)

# Параметры анализа
frame_length = 2048
hop_length = 256

# Загружаем аудио
print('Загружаю аудио...')
y, sr = librosa.load(input_path, sr=None)

# Определяем pitch (частоту) с помощью librosa.pyin
print('Определяю pitch...')
fmin = float(librosa.note_to_hz('C2'))
fmax = float(librosa.note_to_hz('C7'))
f0, voiced_flag, voiced_probs = librosa.pyin(
    y, fmin=fmin, fmax=fmax,
    frame_length=frame_length, hop_length=hop_length
)

# Переводим частоты в ноты
notes = []
times = librosa.frames_to_time(np.arange(len(f0)), sr=sr, hop_length=hop_length)
for idx, (hz, voiced) in enumerate(zip(f0, voiced_flag)):
    if not voiced or hz is None:
        notes.append(None)
    else:
        note_name = librosa.hz_to_note(hz)
        notes.append(note_name)

# Группируем одинаковые ноты подряд
result = []
current_note = None
start_time = None
for i, note in enumerate(notes):
    if note != current_note:
        if current_note is not None:
            end_time = times[i]
            result.append((start_time, end_time, current_note))
        current_note = note
        start_time = times[i]
# Добавляем последнюю ноту
if current_note is not None:
    result.append((start_time, times[-1], current_note))

# Убираем паузы (None)
result = [r for r in result if r[2] is not None]

# Сохраняем в CSV
output_csv = os.path.join(output_dir, 'pitch.csv')
with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['start_time', 'end_time', 'note'])
    for row in result:
        writer.writerow([f'{row[0]:.3f}', f'{row[1]:.3f}', row[2]])

print(f'Готово! Результат сохранён в {output_csv}') 