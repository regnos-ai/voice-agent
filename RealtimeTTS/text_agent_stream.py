import os
from groq import Groq
from engines import BaseEngine  # noqa: F401
from engines import OpenAIEngine, OpenAIVoice  # noqa: F401
from text_to_stream import TextToAudioStream  # noqa: F401
import time
import openai

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# for chunk in  client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Explain the importance of fast language models",
#         }
#     ],
#     model="llama3-8b-8192",
#     stream=True
#     ):
#     print(chunk.choices[0])
# with client.chat.completions.with_streaming_response.create(
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a helpful assisstant.",
#         },
#         {
#             "role": "user",
#             "content": "Explain the importance of low latency LLMs",
#         },
#     ],
#     model="llama3-8b-8192",
# ) as response:
#     print(response.headers.get("X-My-Header"))
#     print("STARTT")
#     for line in response.iter_lines():
#         print(line)
voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
engine = OpenAIEngine(model="tts-1", voice=voices[0])
stream = TextToAudioStream(engine)

def write():
    for chunk in client.chat.completions.create(
        #
        # Required parameters
        #
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {"role": "system", 
            "content": "you are a helpful assistant."},
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": "Explain the importance of low latency LLMs",
            },
        ],
        # The language model which will generate the completion.
        model="llama3-70b-8192",
        stream=True,
    ):
        if (text_chunk := chunk.choices[0].delta.content) is not None:
            yield text_chunk

text_stream = write()

stream.feed(text_stream)
stream.play_async()