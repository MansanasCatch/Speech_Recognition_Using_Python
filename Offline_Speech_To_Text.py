import vosk
import pyaudio
import json

model_path = "vosk-model-en-us-0.22"
model = vosk.Model(model_path)

# Create a recognizer
rec = vosk.KaldiRecognizer(model, 16000)
rec.SetWords(True)

# Open the microphone stream
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)

print("Listening for speech. Say 'Terminate' to stop.")
while True:
    data = stream.read(1024, exception_on_overflow=False)
    exception_on_overflow = False
    if rec.AcceptWaveform(data):

        result = json.loads(rec.Result())
        recognized_text = result['text']

        print(recognized_text)

        if "terminate" in recognized_text.lower():
            print("Termination keyword detected. Stopping...")
            break

# Stop and close the stream
stream.stop_stream()
stream.close()

# Terminate the PyAudio object
audio.terminate()
