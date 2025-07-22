import os
import librosa
import numpy as np
import csv
import crepe

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(BASE_DIR, 'input')
output_dir = os.path.join(BASE_DIR, 'output')
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

output_csv = os.path.join(output_dir, 'pitch.csv')
# Удаляем старый pitch.csv, если он есть
if os.path.exists(output_csv):
    os.remove(output_csv)

input_audio = input(f'Введите имя аудиофайла из папки input (например, vocals.wav): ').strip()
input_path = os.path.join(input_dir, input_audio)

if not os.path.isfile(input_path):
    print(f'Файл {input_path} не найден! Положите его в папку input.')
    exit(1)

# Параметры анализа
MIN_NOTE_DURATION = 0.15  # минимальная длительность ноты в секундах
MIN_CONFIDENCE = 0.5      # минимальная уверенность CREPE
BPM = 120
beat_length = 60 / BPM  # длительность четверти (0.5 сек)
quant_step = beat_length / 4  # 1/16 = 0.125 сек

def quantize_time(t, step):
    return round(t / step) * step

# Загружаем аудио (CREPE требует 16кГц, float32, моно)
print('Загружаю аудио...')
y, sr = librosa.load(input_path, sr=16000, mono=True)
y = y.astype(np.float32)

# Извлекаем питч с помощью CREPE
print('Извлекаю pitch с помощью CREPE...')
time, frequency, confidence, activation = crepe.predict(y, sr, viterbi=True, step_size=10)

# Переводим частоты в ноты, фильтруем по уверенности
notes = []
times = time  # time уже в секундах
for idx, (hz, conf) in enumerate(zip(frequency, confidence)):
    if conf < MIN_CONFIDENCE or hz < 40 or hz > 2000:
        notes.append(None)
    else:
        note_name = librosa.hz_to_note(hz)
        note_name = note_name.replace('♯', '#').replace('♭', 'b')
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

# Квантование к сетке 120 BPM (1/16)
quantized_result = []
for start, end, n in result:
    q_start = quantize_time(start, quant_step)
    q_end = quantize_time(end, quant_step)
    if q_end > q_start:
        quantized_result.append((q_start, q_end, n))
result = quantized_result

# Убираем паузы (None) и слишком короткие ноты
result = [r for r in result if r[2] is not None and (r[1] - r[0]) >= MIN_NOTE_DURATION]

# Сохраняем в CSV
with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['start_time', 'end_time', 'note'])
    for row in result:
        writer.writerow([f'{row[0]:.3f}', f'{row[1]:.3f}', row[2]])

print(f'Готово! Результат сохранён в {output_csv}') 