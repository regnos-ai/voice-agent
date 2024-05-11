key = "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"

# import os

# from groq import Groq

# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Explain the importance of fast language models",
#         }
#     ],
#     model="llama3-8b-8192",
# )

# print(chat_completion.choices[0].message.content)

import os

from groq import Groq
from engines import BaseEngine  # noqa: F401
from engines import OpenAIEngine, OpenAIVoice  # noqa: F401
from text_to_stream import TextToAudioStream  # noqa: F401
import time
import openai
from speech_to_text import s2t

# Initialize the Groq API client
voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
engine = OpenAIEngine(model="tts-1", voice=voices[0])
stream = TextToAudioStream(engine)
content = '''
<role> You are an AI real estate agent, your name is Rachel. You are calling a user called Alex and he is a potential customer. Try to impress him with how human-like sounding language  you can generate and ask him about opportunities to rent his place.</role>
<personality> You are good at your job, subtle and understand the potential customer's expectations </personality>
<techniques> You are charming but subtle. You are a professional and you know what you are doing. </techniques> 
<goal> Your goal is to find out what interests Alex and find him possible options for renting</goal>
<style> KEEP THE RESPONSES VERY SHORT AND CONVERSATIONAL.   </style>
'''
def chat_with_agent():
    print("Real Estate Agent Bot Cold Call Simulation. Type 'quit' to exit.")
    
    # Start the conversation with the bot introducing itself and making a proposition
    messages = [
        {
            "role": "system",
            "content": content
        },
        # {
        #     "role": "assistant",
        #     "content": "Hello! I'm reaching out from [Your Real Estate Company]. We've got some exciting new listings in your area that offer great amenities at competitive prices. Are you currently interested in exploring new home options?"
        # }
    ]

    while True:
        # Get user input
        # user_input = input("You: ")
        user_input = s2t()
        print(user_input.lower())
        if user_input.lower() == 'quit' or user_input.lower() == 'quit.':
            break
        
        # Append user's message to the conversation history
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Send the updated conversation to the API
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-70b-8192",
        )
        
        # Retrieve the response from the bot and print it
        bot_response = chat_completion.choices[0].message.content
        print("Agent:", bot_response)
        stream.feed(bot_response)
        stream.play()
        # Append the bot's response to the conversation history
        messages.append({
            "role": "assistant",
            "content": bot_response
        })
        time.sleep(0.2)

if __name__ == "__main__":
    chat_with_agent()
