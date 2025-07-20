.PHONY: split_vocals_env pitch_detection_env visualization_env music21_notation_env compare_vocals_env all_envs run_split_vocals run_pitch_detection run_visualization run_music21_notation run_compare_vocals

split_vocals_env:
	cd 01_split_vocals && python3.10 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

pitch_detection_env:
	cd 02_pitch_detection && python3.10 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

visualization_env:
	cd 03_visualization && python3.10 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

music21_notation_env:
	cd 03_music21_notation && python3.10 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

compare_vocals_env:
	cd 05_compare_vocals && python3.10 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

all_envs: split_vocals_env pitch_detection_env visualization_env music21_notation_env compare_vocals_env

run_split_vocals:
	. 01_split_vocals/venv/bin/activate && python 01_split_vocals/split_vocals.py

run_pitch_detection:
	. 02_pitch_detection/venv/bin/activate && python 02_pitch_detection/pitch_detection.py

run_visualization:
	. 03_visualization/venv/bin/activate && python 03_visualization/visualize_notes.py

run_music21_notation:
	. 03_music21_notation/venv/bin/activate && python 03_music21_notation/music21_notation.py

run_compare_vocals:
	. 05_compare_vocals/venv/bin/activate && python 05_compare_vocals/compare_vocals.py 

test2:
	make pitch_detection_env
	make run_pitch_detection
test3:
	make music21_notation_env
	make run_music21_notation