#!/usr/bin/env python3
"""
Basic Pitch Processor - Advanced note extraction using Spotify's Basic Pitch
Extracts notes from vocals using neural network-based transcription
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.inference import predict
import librosa
import pretty_midi

def setup_directories():
    """Create necessary directories if they don't exist"""
    # Get the project root directory (parent of current module)
    project_root = Path(__file__).parent.parent
    dirs = [
        project_root / 'input',
        project_root / 'output', 
        project_root / 'output' / 'basic_pitch'
    ]
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

def find_vocal_files():
    """Find vocal files in input directory"""
    project_root = Path(__file__).parent.parent
    input_dir = project_root / 'input'
    vocal_files = []
    
    # Look for vocal files (common patterns)
    patterns = ['*vocals*', '*vocal*', '*voice*', '*sing*']
    for pattern in patterns:
        vocal_files.extend(input_dir.glob(pattern))
    
    # Also check for any audio files if no specific vocal files found
    if not vocal_files:
        audio_extensions = ['.wav', '.mp3', '.flac', '.m4a']
        for ext in audio_extensions:
            vocal_files.extend(input_dir.glob(f'*{ext}'))
    
    return vocal_files

def process_audio_with_basic_pitch(audio_path):
    """Process audio file using Basic Pitch"""
    print(f"Processing: {audio_path}")
    
    # Load and predict using Basic Pitch
    model_output, midi_data, note_events = predict(str(audio_path))
    
    return model_output, midi_data, note_events

def save_results(model_output, midi_data, note_events, output_dir, base_name):
    """Save Basic Pitch results in various formats"""
    output_path = Path(output_dir)
    
    # Save MIDI file
    midi_path = output_path / f"{base_name}_basic_pitch.mid"
    midi_data.write(str(midi_path))
    print(f"MIDI saved: {midi_path}")
    
    # Convert to CSV format compatible with music21
    csv_path = output_path / f"{base_name}_basic_pitch.csv"
    convert_to_csv(note_events, csv_path)
    print(f"CSV saved: {csv_path}")
    
    return csv_path

def convert_to_csv(note_events, csv_path):
    """Convert Basic Pitch output to CSV format compatible with music21"""
    notes_data = []
    
    # Extract note information from note_events
    # note_events format: (start_time, end_time, pitch_midi, velocity, pitch_bend)
    for start_time, end_time, pitch_midi, velocity, pitch_bend in note_events:
        # Convert MIDI pitch to frequency
        pitch_hz = librosa.midi_to_hz(pitch_midi)
        
        # Convert MIDI pitch to note name
        note_name = librosa.midi_to_note(pitch_midi, octave=True)
        
        # Convert to format compatible with music21
        # Replace unicode symbols with ASCII for music21 compatibility
        note_name = note_name.replace('♯', 'sharp').replace('♭', 'flat')
        note_name = note_name.replace('#', 'sharp').replace('b', 'flat')
        
        notes_data.append({
            'start_time': start_time,
            'end_time': end_time,
            'duration': end_time - start_time,
            'pitch': pitch_hz,
            'pitch_midi': pitch_midi,
            'velocity': velocity,
            'note_name': note_name
        })
    
    # Create DataFrame and save
    df = pd.DataFrame(notes_data)
    df.to_csv(csv_path, index=False)
    
    print(f"Extracted {len(notes_data)} notes")
    return df

def main():
    """Main processing function"""
    print("=== Basic Pitch Processor ===")
    print("Advanced note extraction using Spotify's Basic Pitch")
    
    # Setup directories
    setup_directories()
    
    # Find vocal files
    vocal_files = find_vocal_files()
    
    if not vocal_files:
        project_root = Path(__file__).parent.parent
        input_dir = project_root / 'input'
        print(f"No audio files found in {input_dir}/")
        print("Please place your vocal files in the input directory")
        return
    
    print(f"Found {len(vocal_files)} audio file(s)")
    
    # Process each file
    for audio_file in vocal_files:
        try:
            print(f"\n--- Processing {audio_file.name} ---")
            
            # Process with Basic Pitch
            model_output, midi_data, note_events = process_audio_with_basic_pitch(audio_file)
            
            # Save results
            base_name = audio_file.stem
            project_root = Path(__file__).parent.parent
            output_dir = project_root / 'output' / 'basic_pitch'
            csv_path = save_results(model_output, midi_data, note_events, output_dir, base_name)
            
            print(f"✅ Successfully processed {audio_file.name}")
            
        except Exception as e:
            print(f"❌ Error processing {audio_file.name}: {e}")
            continue
    
    print("\n=== Processing Complete ===")
    print("Results saved in ../output/basic_pitch/")

if __name__ == "__main__":
    main() 