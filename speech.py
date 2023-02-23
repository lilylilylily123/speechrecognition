import pvporcupine
import pyaudio
import struct
import asyncio

import gui
#from gui import App
#from press import *
import speech_recognition
import sounddevice as sd
# Path to the keyword model
Jump = ("./keywords/Jump-Up_en_windows_v2_1_0.ppn")
PressA = ("./keywords/Press-A_en_windows_v2_1_0.ppn")
PressD = ("./keywords/Press-D_en_windows_v2_1_0.ppn")
PressS = ("./keywords/Press-S_en_windows_v2_1_0.ppn")
PressW = ("./keywords/Press-W_en_windows_v2_1_0.ppn")
PressShift = ("./keywords/Press-Shift_en_windows_v2_1_0.ppn")
keyword_paths = [Jump, PressW, PressA, PressD, PressS, PressShift]

porc = pvporcupine.create(keyword_paths=keyword_paths, access_key="K+IKUv3z2d58y8Tx8amkJsPOqHulYAEr4GCUqKFTBcreVOkfQL5TAA==")
#print(speech_recognition.Microphone.list_microphone_names())
#global gui.active
def wake():
    print(sd.query_devices())
    audio_stream = pyaudio.PyAudio().open(
        rate=porc.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porc.frame_length,
        input_device_index=3   )
    while True:
        pcm = audio_stream.read(porc.frame_length)
        pcm = struct.unpack_from("h" * porc.frame_length, pcm)

        keyword_index = porc.process(pcm)

        if keyword_index == 0:
            print("Jump detected")
            asyncio.run(press_jump())
        elif keyword_index == 1:
            print("w detected")
            asyncio.run(press_up())
        elif keyword_index == 2:
            print("a detected")
            asyncio.run(press_left())
        elif keyword_index == 3:
            print("d detected")
            asyncio.run(press_right())
        elif keyword_index == 4:
            print("s detected")
            asyncio.run(press_down())
        elif keyword_index == 5:
            print("shift detected")
            asyncio.run(press_shift())
        else:
             pass
# wake()