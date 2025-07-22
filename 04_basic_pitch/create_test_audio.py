#!/usr/bin/env python3
"""
Create test audio file for Basic Pitch testing
Generates a simple melody with clear notes
"""

import numpy as np
import librosa
import soundfile as sf
from pathlib import Path

def create_test_melody():
    """Create a simple test melody with clear notes"""
    
    # Audio parameters
    sample_rate = 22050
    duration = 5.0  # 5 seconds
    
    # Create time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Define a simple melody (C major scale)
    notes = [
        (440.0, 0.0, 0.5),    # A4
        (493.88, 0.5, 0.5),   # B4
        (523.25, 1.0, 0.5),   # C5
        (587.33, 1.5, 0.5),   # D5
        (659.25, 2.0, 0.5),   # E5
        (698.46, 2.5, 0.5),   # F5
        (783.99, 3.0, 0.5),   # G5
        (880.0, 3.5, 0.5),    # A5
        (523.25, 4.0, 1.0),   # C5 (longer note)
    ]
    
    # Create audio signal
    audio = np.zeros_like(t)
    
    for freq, start_time, note_duration in notes:
        start_sample = int(start_time * sample_rate)
        end_sample = int((start_time + note_duration) * sample_rate)
        
        # Create sine wave for this note
        note_t = np.linspace(0, note_duration, end_sample - start_sample, False)
        note_audio = 0.3 * np.sin(2 * np.pi * freq * note_t)
        
        # Add fade in/out to avoid clicks
        fade_samples = int(0.01 * sample_rate)  # 10ms fade
        if fade_samples > 0:
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            note_audio[:fade_samples] *= fade_in
            note_audio[-fade_samples:] *= fade_out
        
        # Add to main audio
        audio[start_sample:end_sample] += note_audio
    
    return audio, sample_rate

def main():
    """Create and save test audio file"""
    print("Creating test audio file...")
    
    # Create test melody
    audio, sample_rate = create_test_melody()
    
    # Ensure output directory exists
    project_root = Path(__file__).parent.parent
    output_dir = project_root / 'input'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save audio file
    output_path = output_dir / 'test_melody.wav'
    sf.write(str(output_path), audio, sample_rate)
    
    print(f"✅ Test audio created: {output_path}")
    print(f"   Duration: {len(audio) / sample_rate:.1f} seconds")
    print(f"   Sample rate: {sample_rate} Hz")
    print(f"   Format: WAV")

if __name__ == "__main__":
    main() 