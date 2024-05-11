import pyaudio
import wave
import webrtcvad
import collections
from openai import OpenAI

client = OpenAI()

def record_audio_vad(filename="output.wav", max_silence_seconds=2):
    # Audio configuration
    chunk_duration = 0.02  # Each read length in seconds
    sample_rate = 16000  # Sample rate in Hz
    channels = 1  # Mono audio
    format = pyaudio.paInt16  # 16 bits per sample

    vad = webrtcvad.Vad(3)  # Set aggressiveness from 0 to 3
    p = pyaudio.PyAudio()

    # Open the stream for recording
    stream = p.open(format=format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=int(sample_rate * chunk_duration))
    num_padding_frames = int(max_silence_seconds / chunk_duration)  # Number of frames silence before stopping

    # Store frames here
    frames = []
    triggered = False
    silent_frames = collections.deque(maxlen=num_padding_frames)

    print("Please start speaking. The recording will start when you start speaking.")
    while True:
        frame = stream.read(int(sample_rate * chunk_duration))
        is_speech = vad.is_speech(frame, sample_rate)

        if not triggered:
            silent_frames.append(frame)
            if is_speech:
                print("Recording started...")
                triggered = True
                frames.extend(list(silent_frames))  # Append the buffer of previous frames
                silent_frames.clear()
        else:
            frames.append(frame)
            print(is_speech)
            if is_speech:
                silent_frames.clear()  # Reset silence counter on speech detection
            else:
                silent_frames.append(frame)
                print(len(silent_frames),num_padding_frames)
                if len(silent_frames) >= num_padding_frames:
                    print("Maximum silence reached; stopping recording.")
                    break

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PyAudio session
    p.terminate()

    # Save the recorded data as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    print("Recording stopped and saved to", filename)
    return filename

def transcribe_audio(filename):
    audio_file = open(filename, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
    )
    return transcription

def s2t():
    audio_filename = record_audio_vad(max_silence_seconds=1)  # Adjust silence timeout as needed
    transcription = transcribe_audio(audio_filename)
    return transcription



