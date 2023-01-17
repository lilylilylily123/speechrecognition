import time
import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone()
#print(sr.Microphone.list_microphone_names())
with mic as source:
    try:
        r.adjust_for_ambient_noise(source, duration=2)
        audio = r.listen(source)
        print(r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
