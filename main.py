import vosk
import pyaudio
import json
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 120)

volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

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
isSpeaking = False

while True:
    if not isSpeaking:
        data = stream.read(1024, exception_on_overflow=False)
        exception_on_overflow = False
        print("Listening...")
        if rec.AcceptWaveform(data):

            result = json.loads(rec.Result())
            recognized_text = result['text']

            if recognized_text != "":
                isSpeaking = True
                print(recognized_text)
                engine.say(recognized_text)
                engine.runAndWait()
                engine.stop()
                isSpeaking = False

            if "terminate" in recognized_text.lower():
                print("Termination keyword detected. Stopping...")
                break

# Stop and close the stream
stream.stop_stream()
stream.close()

# Terminate the PyAudio object
audio.terminate()
