.PHONY: split_vocals_env pitch_detection_env visualization_env music21_notation_env compare_vocals_env all_envs run_split_vocals run_pitch_detection run_visualization run_music21_notation run_compare_vocals

split_vocals_env:
	cd 01_split_vocals && python3.10 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

pitch_detection_env:
	cd 02_pitch_detection && python3.10 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

visualization_env:
	cd 03_visualization && python3.10 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

music21_notation_env:
	cd 04_music21_notation && python3.10 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

compare_vocals_env:
	cd 05_compare_vocals && python3.10 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

all_envs: split_vocals_env pitch_detection_env visualization_env music21_notation_env compare_vocals_env

run_split_vocals:
	cd 01_split_vocals && . venv/bin/activate && python split_vocals.py

run_pitch_detection:
	cd 02_pitch_detection && . venv/bin/activate && python pitch_detection.py

run_visualization:
	cd 03_visualization && . venv/bin/activate && python visualize_notes.py

run_music21_notation:
	cd 04_music21_notation && . venv/bin/activate && python notes_to_score.py

run_compare_vocals:
	cd 05_compare_vocals && . venv/bin/activate && python compare_vocals.py 