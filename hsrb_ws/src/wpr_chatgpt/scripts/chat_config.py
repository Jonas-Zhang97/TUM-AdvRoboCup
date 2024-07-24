#!/usr/bin/env python3
# Name the robot / assistant:
robot_name = "AI"
# initial_prompt = "You are " + robot_name + " and are assertive, sassy and sarcastic that likes to make fun huaman who ask stupid questions. You also likes to continue the conversation by asking questions."

initial_prompt = """ I will tell you a command, extract the command into a sequence of states
we have the following states:
- Start
- Pick
- Nav
- Look For
- Look For wh
- Place
- Listen
- Audio Output
- End
expample command: 
output a list of the sequence. You shall only resonse in python list, but in a form of plain text. 
For example: states = [<your response>]


"""

# Select what type of mode to run on openai
mode = "ChatCompletion"

###  Chat GPT configuration stuff
model = "gpt-4o-mini" #"text-curie-001"
temperature=0.7
max_tokens=1000
top_p=0.3
frequency_penalty=0.1
presence_penalty=1.5

chat_history_length = 5

