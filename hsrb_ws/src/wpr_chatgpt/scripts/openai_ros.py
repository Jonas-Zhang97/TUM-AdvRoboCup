#!/usr/bin/env python3
# coding=utf-8
import os
from openai import OpenAI
key = "EnterYourOwnKey"

client = OpenAI(api_key=key)   
import rospy
from std_msgs.msg import String
import chat_config

import re


class openai_handler:

    # initialize chatgpt and ROS
    def __init__(self, _initial_prompt) -> None:
       # openai.api_key = os.getenv("OPENAI_API_KEY")                                                      
        #"<api-key>" #sk-proj-OyZbI9topMSe5mS8i67TT3BlbkFJ4SP3jtXrRMgmysRZQ9gf
        self.initial_prompt = _initial_prompt
        self.new_response = False
        self.response = ""
        self.prompt = ""

        # ROS 
        rospy.init_node('openai_handler', anonymous=True)
        self.response_pub = rospy.Publisher('openai/response', String, queue_size=0)
        # self.fullcode_pub = rospy.Publisher('openai/fullcode', String, queue_size=0)
        rospy.Subscriber("openai/prompt", String, self.prompt_sub)
        self.rate = rospy.Rate(10) # 10hz
        self.chat_history = [{"role": "system", "content": self.initial_prompt}]
        rospy.loginfo("Waiting for command ...")



    # prompt_sub:
    #   When a prompt is recieved, organise it and send a request to the API on demand.      
    def prompt_sub(self, data):

        rospy.loginfo(rospy.get_caller_id() + "OpenAI: Prompt: %s", data.data)
        self.prompt = data.data

        # Log the history
        self.chat_history.append( {"role": "user", "content": self.prompt} )

        # If the chat log is longer than specified, remove the oldest (but not the context)
        if(len(self.chat_history) > chat_config.chat_history_length):
            del self.chat_history[1]

        # Get a response
        self.new_response, self.respone= self.get_response(self.prompt)

    # get_response:
    #   generate and send a request to the openai api, get request and return the useful stuff    
    def get_response(self, _prompt):

        success = False
        #################################################################
        # ChatCompletion:          this mode is used to chat with the robot while keeping the context
        if chat_config.mode == "ChatCompletion":
            response = client.chat.completions.create(model=chat_config.model,
            messages=self.chat_history,
            max_tokens=chat_config.max_tokens,
            presence_penalty=chat_config.presence_penalty)
            print(response)
            text_response = response.choices[0].message.content
            # rospy.logwarn('text_response', text_response)
            self.chat_history.append( {"role": "assistant", "content": text_response} )
            success = True

            # full_code = self.extract_python_code(text_response)                # extract python code from the answer of chatgpt                       
            # rospy.loginfo("full_code: %s",full_code)						                         


            # object = self.extract_object(text_response)                       # extract object from the answer of chatgpt                        
            # rospy.loginfo("object: %s",object)	

            # try:
            #     response = client.chat.completions.create(model=chat_config.model,
            #     messages=self.chat_history,
            #     max_tokens=chat_config.max_tokens,
            #     presence_penalty=chat_config.presence_penalty)
            #     rospy.logwarn(response)
            #     text_response = response.choices[0].message.content
            #     rospy.logwarn('text_response', text_response)
            #     self.chat_history.append( {"role": "assistant", "content": text_response} )
            #     success = True

            #     full_code = self.extract_python_code(text_response)                # extract python code from the answer of chatgpt                       
            #     rospy.loginfo("full_code: %s",full_code)						                         


            #     object = self.extract_object(text_response)                       # extract object from the answer of chatgpt                        
            #     rospy.loginfo("object: %s",object)						                                  
            # except Exception as e: 
            #     rospy.logerr("Error with openai ChatCompletion response")
            #     text_response = "Sorry, something went wrong. Please try again later."
            #     success = False

        #################################################################
        # Completion:
        elif chat_config.mode == "Completion":

            # Format the prompt so it replies like a robot in a chat.
            p = self.initial_prompt + " Human:" + _prompt + " " + chat_config.robot_name + ":"  
            p.replace("\n", "")
            
            try:
                response = client.completions.create(model=chat_config.model,
                prompt=_prompt,
                temperature=chat_config.temperature,
                max_tokens=chat_config.max_tokens,
                top_p=chat_config.top_p,
                frequency_penalty=chat_config.frequency_penalty,
                presence_penalty=chat_config.presence_penalty,
                stop=[" Human:", " " + chat_config.robot_name + ":"])
                text_response = response.choices[0].text.replace("\n", "")
                success = True
            except Exception as e:
                rospy.logerr("Error with openai Completion response")
                text_response = "Sorry, something went wrong. Please try again later."
                success = False

        else:
            text_response = "Sorry, the configuration of the system is wrong. Please contact someone"
            success = False

        rospy.loginfo(rospy.get_caller_id() + "OpenAI: Response: %s", text_response)

        return success, text_response








    # main:
    #   Keep alive, check for new responses and publish the text to the response topic (openai/response)    
    def main(self):

        while not rospy.is_shutdown():

            if(self.new_response):
                self.response_pub.publish(self.respone)
                # self.fullcode_pub.publish(self.code_generated)                                            
                self.new_response = False

                # publish the object to rosparam
                # rospy.set_param('object', self.object_generated)                                                 

            self.rate.sleep()


     # extract python code from the answer of chatgpt       
    def extract_python_code(self, content):
        code_block_regex = re.compile(r"```(.*?)```", re.DOTALL) # re.DOTALL is needed to match across newlines
        code_blocks = code_block_regex.findall(content)     # returns a list of strings
        if code_blocks:
            full_code = "\n".join(code_blocks)              # join the list of strings into one string

            if full_code.startswith("python"):              # remove the "python" prefix
                full_code = full_code[7:]       # 7 is the length of "python"

                return full_code                # return the code
            else:
                return None 
     # extract object from the answer of chatgpt
    def extract_object(self, content):  
        code_block_regex_obj = re.compile(r"<(.*?)>", re.DOTALL)
        code_blocks_obj = code_block_regex_obj.findall(content)
        if code_blocks_obj:
            object = "\n".join(code_blocks_obj)

            if object.startswith("object:"):
                object = object[7:]
                return object
            else:
                return None





if __name__ == "__main__":

    o_h = openai_handler(chat_config.initial_prompt)
    o_h.main()


