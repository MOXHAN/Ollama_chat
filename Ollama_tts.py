import ollama
from openai import OpenAI
import streamlit as st
import pyaudio
import threading
import queue
from dotenv import load_dotenv
import os

class AudioPlayer(threading.Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.queue = queue.Queue()
        self.daemon = True
        self.start()

    def run(self):
        while True:
            text = self.queue.get()
            if text is None:
                break
            self.play_audio(text)
            self.queue.task_done()

    def play_audio(self, text):
        player_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

        with self.client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            response_format="pcm",
            speed=1.0,
            input=text,
        ) as response:
            for chunk in response.iter_bytes(chunk_size=1024):
                player_stream.write(chunk)

        player_stream.close()

    def add_to_queue(self, text):
        self.queue.put(text)

def main():
    # initialize the context
    context = []
    buffer_txt = ""  # Buffer to store text before sending to TTS

    load_dotenv()

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # Initialize AudioPlayer obj
    audio_player = AudioPlayer(client)

    # infinetly loop to keep the conversation going
    while True:

        prompt = input("\nYou: ")

        # generate the response
        output = ollama.generate(model="llama3",prompt=prompt, context=context, stream=True) #stream=True)
        
        # loop through the response
        for chunk in output:
            # print the response
            print(chunk["response"], end="", flush=True)

            # Buffer full sentences for TTS
            buffer_txt += chunk["response"]
            if "." in buffer_txt or "?" in buffer_txt or "!" in buffer_txt:
                audio_player.add_to_queue(buffer_txt)
                buffer_txt = ""

            if chunk["done"]:
                context = chunk["context"]
                break  # Exit if conversation is done

if __name__ == "__main__":
    main()