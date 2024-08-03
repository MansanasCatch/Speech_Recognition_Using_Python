import pyttsx3
engine = pyttsx3.init()

engine.setProperty('rate', 120)

volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

engine.say("Feel free to wrap another text-to-speech engine for use with pyttsx3.")
engine.runAndWait()
engine.stop()
