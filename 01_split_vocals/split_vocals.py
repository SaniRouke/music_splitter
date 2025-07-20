from spleeter.separator import Separator
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(BASE_DIR, 'input')
output_dir = os.path.join(BASE_DIR, 'output')

os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

input_audio = input(f'Введите имя аудиофайла из папки input (например, song.mp3): ').strip()
input_path = os.path.join(input_dir, input_audio)

if not os.path.isfile(input_path):
    print(f'Файл {input_path} не найден! Положите его в папку input.')
    exit(1)

separator = Separator('spleeter:2stems')
separator.separate_to_file(input_path, output_dir)

print(f'Готово! Вокал и минусовка сохранены в папке output.') 