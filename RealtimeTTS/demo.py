from engines import BaseEngine  # noqa: F401
from engines import OpenAIEngine, OpenAIVoice  # noqa: F401
from text_to_stream import TextToAudioStream  # noqa: F401
import time
import openai

# from .engines import SystemEngine, SystemVoice  # noqa: F401
# from .engines import AzureEngine, AzureVoice  # noqa: F401
# from .engines import ElevenlabsEngine, ElevenlabsVoice  # noqa: F401
# from .engines import CoquiEngine, CoquiVoice  # noqa: F401

# engine = SystemEngine() # replace with your TTS engine
# stream = TextToAudioStream(engine)
# stream.feed("Hello world! How are you today?")
# stream.play_async()
#############################################################################################################################
def write(prompt: str):
    for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content" : prompt}],
        stream=True
    ):
        if (text_chunk := chunk["choices"][0]["delta"].get("content")) is not None:
            yield text_chunk


text = "Nice to meet you, Alex! I'm Rachel, a real estate agent with Premium Properties. I came across your address and thought I'd reach out to introduce myself. We've been helping homeowners in the area find great tenants and maximize their rental income."
engine = OpenAIEngine(model="tts-1", voice="alloy")
stream = TextToAudioStream(engine)
# stream.feed("Fourier transform is a mathematical technique that breaks down a signal into its individual frequency components.")
# text_stream = write("A three-sentence relaxing speech.")

# # stream.feed(text_stream)
# # print ("Synthesizing...")
# # stream.play_async()

# stream.feed("It's commonly used in signal processing and many other fields to analyze and manipulate functions or signals in the frequency domain.")

# print ("Synthesizing...")
# stream.play_async()

# stream.feed("Uhm, yeah! This sounds great. I will make sure to get back to you on that.")

# print ("Synthesizing...")
# stream.play_async()
stream.feed(text)

print ("Synthesizing...")
stream.play_async()

from openai import OpenAI
from pydub import AudioSegment
import io

client = OpenAI()

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text,
    # streaming=True  # Ensure streaming is enabled
)

# The response will directly be the binary content of the audio
audio_data = response.content  # If using an HTTP client, this would typically be how you access the binary data

# Save the audio data to an MP3 file
with open("output.mp3", "wb") as f:
    f.write(audio_data)
# stream.play_async()
# while stream.is_playing():
#     time.sleep(0.1)


# stream.feed("Hello, World! ")

# def dummy_generator():
#     yield "This "
#     # time.sleep(0.2)
#     yield "is "
#     # time.sleep(0.2)
#     yield "a "
#     # time.sleep(0.2)
#     yield "stream of words. "
#     # time.sleep(0.2)
#     yield "And here's another sentence! Yet, "
#     # time.sleep(0.2)
#     yield "there's more. This ends now. "

# stream.feed(dummy_generator())    

# stream.feed("Nice to be here! ")
# stream.feed("Welcome all ")
# stream.feed("my dear friends ")
# stream.feed("of realtime apps. ")

# stream.play()