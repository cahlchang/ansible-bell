import wave
import struct
import math

def generate_beep(filename, duration, start_freq, end_freq, volume=1.0, framerate=44100):
    """
    Generate a beep sound with linearly changing frequency and save it as a WAV file.

    :param filename: Name of the WAV file to generate
    :param duration: Duration of the sound (seconds)
    :param start_freq: Starting frequency (Hz)
    :param end_freq: Ending frequency (Hz)
    :param volume: Volume (0.0 to 1.0)
    :param framerate: Sampling rate (default is 44100)
    """
    # Number of wave samples (duration seconds × framerate)
    n_samples = int(duration * framerate)

    # Use 16-bit PCM, so maximum amplitude is 32767
    max_amplitude = 32767

    # Calculate frequency increment per sample (linear interpolation)
    freq_increment = (end_freq - start_freq) / n_samples
    
    # Open WAV file in "wb" (write binary) mode
    with wave.open(filename, 'wb') as wav_file:
        # Channel count = 1 (mono), sample size = 2 bytes (16-bit), framerate, data size is undefined so 0
        wav_file.setparams((1, 2, framerate, 0, 'NONE', 'not compressed'))

        current_freq = start_freq
        for i in range(n_samples):
            # Basic sine wave formula
            sample_value = math.sin(2.0 * math.pi * current_freq * (i / framerate))
            # Multiply by volume and maximum amplitude, then convert to integer
            packed_value = struct.pack('<h', int(sample_value * max_amplitude * volume))
            wav_file.writeframes(packed_value)
            
            # Gradually change the frequency
            current_freq += freq_increment

# -------------------------
# Create actual sound files
# -------------------------

# "Success sound": frequency low → high (e.g., 500Hz → 800Hz)
generate_beep(
    filename='success_sound.wav',
    duration=0.3,       # Duration (seconds)
    start_freq=500.0,   # Starting frequency
    end_freq=800.0,     # Ending frequency
    volume=0.8
)

# "Failure sound": frequency high → low (e.g., 800Hz → 500Hz)
generate_beep(
    filename='failure_sound.wav',
    duration=0.3,
    start_freq=800.0,
    end_freq=500.0,
    volume=0.8
)

print("Success sound (success_sound.wav) and failure sound (failure_sound.wav) have been generated.")
