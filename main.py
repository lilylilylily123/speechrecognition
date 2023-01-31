#!/usr/bin/env python3
import struct
import pyaudio
import pvporcupine
import os
import speech_recognition as sr
import whisper
import torch
import numpy as np
from datetime import datetime
import openai
import pyttsx3
from conversation import Conversation



class DanielGPT:

    def __init__(self,
                 voice_id="com.apple.speech.synthesis.voice.Daniel",
                 voice_rate=120):
        self.porcupine = None
        self.PyAudio = None
        self.audio_stream = None
        self.porcupine_key = 'K+IKUv3z2d58y8Tx8amkJsPOqHulYAEr4GCUqKFTBcreVOkfQL5TAA=='
        openai.api_key = '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'
        self.engine = pyttsx3.init()
        self.voice_id = voice_id
        self.voice_rate = voice_rate
        self.engine.setProperty('voice', self.voice_id)
        self.engine.setProperty('rate', self.voice_rate)
        self.conversation = Conversation()

    def wakeword(self):
        try:
            self.porcupine = pvporcupine.create(keyword_paths=[
                "porcupine_keywords\Circus_en_windows_v2_1_0.ppn" ],
                                                access_key=self.porcupine_key)

            self.PyAudio = pyaudio.PyAudio()

            self.audio_stream = self.PyAudio.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length)

            while True:
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length,
                                         pcm)

                keyword_index = self.porcupine.process(pcm)

                if keyword_index >= 0:
                    return "Hotword Detected"
        finally:
            if self.porcupine is not None:
                self.porcupine.delete()

            if self.audio_stream is not None:
                self.audio_stream.close()

            if self.PyAudio is not None:
                self.PyAudio.terminate()

    def speech_recognizer(self, energy=300, pause=0.8, dynamic_energy=False):
        print(datetime.now())
        audio_model = whisper.load_model("base")

        #load the speech recognizer and set the initial energy threshold and pause threshold
        r = sr.Recognizer()
        r.energy_threshold = energy
        r.pause_threshold = pause
        r.dynamic_energy_threshold = dynamic_energy

        with sr.Microphone(sample_rate=16000) as source:
            while True:
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, phrase_time_limit=4)
                torch_audio = torch.from_numpy(
                    np.frombuffer(audio.get_raw_data(),
                                  np.int16).flatten().astype(np.float32) /
                    32768.0)
                audio_data = torch_audio

                result = audio_model.transcribe(audio_data, fp16=False)
                print(result)
                predicted_text = result["text"]

                self.conversation.add(f"Person: {predicted_text}")
                return predicted_text

    def generate_response(self, prompt):
        prompt = self.conversation.to_ctx()
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        self.conversation.add(f"Daniel: {response.choices[0].text}")

        return response

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def handler(self):
        while True:
            if self.wakeword() == "Hotword Detected":

                query = self.speech_recognizer()
                print(query)
                response = self.generate_response(query).choices[0].text
                self.speak(response)


DanielGPT().handler()
