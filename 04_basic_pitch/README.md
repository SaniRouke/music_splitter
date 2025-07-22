# Basic Pitch Processor

Advanced note extraction module using Spotify's Basic Pitch neural network.

## Description

This module uses Basic Pitch, a state-of-the-art neural network model from Spotify, to extract musical notes from vocal audio files. Basic Pitch provides superior accuracy compared to traditional pitch detection methods.

## Features

- **Neural Network-based**: Uses advanced AI model for better accuracy
- **Multiple Output Formats**: MIDI, CSV, and simplified notes
- **Polyphonic Support**: Can handle multiple simultaneous notes
- **High Precision**: Better note detection and timing accuracy
- **Music21 Compatible**: Outputs CSV format compatible with music21 notation

## Requirements

- Python 3.8+
- Basic Pitch library
- Librosa for audio processing
- Pandas for data handling

## Installation

```bash
# Create virtual environment
python -m venv basic_pitch_env

# Activate environment
source basic_pitch_env/bin/activate  # Linux/Mac
# or
basic_pitch_env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. Place your vocal audio files in the `../input/` directory
2. Run the processor:
   ```bash
   python basic_pitch_processor.py
   ```
3. Results will be saved in `../output/basic_pitch/`

## Output Files

For each input file, the following outputs are generated:

- `*_basic_pitch.mid` - Full MIDI file with all detected notes
- `*_notes.mid` - Simplified MIDI with just the notes
- `*_basic_pitch.csv` - CSV file compatible with music21 notation

## CSV Format

The CSV file contains the following columns:
- `start_time` - Note start time in seconds
- `end_time` - Note end time in seconds  
- `duration` - Note duration in seconds
- `pitch` - Frequency in Hz
- `velocity` - Note velocity (loudness)
- `note_name` - Note name (e.g., "C4", "F#3")

## Advantages over Traditional Methods

- **Better Accuracy**: Neural network trained on large dataset
- **Noise Resistance**: Handles background noise better
- **Polyphonic Detection**: Can detect multiple notes simultaneously
- **Consistent Results**: More reliable across different audio qualities
- **Professional Quality**: Used by Spotify and other music platforms

## Integration

This module can be used as a replacement for the pitch detection module or as an additional option for higher quality results. The CSV output is compatible with the music21 notation module. 