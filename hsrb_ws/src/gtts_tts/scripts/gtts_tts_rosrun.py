#!/usr/bin/env python3
import rospy
from tmc_msgs.msg import Voice
from gtts import gTTS
import os
import sys

def text_to_speech(text, language):
    tts = gTTS(text=text, lang=language)
    tts.save("/tmp/tts_output.mp3")
    os.system("mpg321 /tmp/tts_output.mp3")

def main():
    rospy.init_node('gtts_tts_node', anonymous=True)
    
    # Get parameters from the parameter server
    sentence = rospy.get_param('~sentence', 'Hello, this is the default message.')
    language = rospy.get_param('~language', 'en')
    
    pub = rospy.Publisher('/talk_request', Voice, queue_size=10)
    
    # Create the Voice message
    voice_msg = Voice()
    voice_msg.interrupting = False
    voice_msg.queueing = False
    voice_msg.language = Voice.kEnglish if language == 'en' else Voice.kJapanese
    voice_msg.sentence = sentence
    
    # Perform text-to-speech synthesis and play the audio
    text_to_speech(sentence, language)

    # Publish the message and check if it was successful
    rospy.loginfo("Publishing message to /talk_request")
    pub.publish(voice_msg)
    
    # Wait for the message to be fully published
    if pub.get_num_connections() > 0:
        rospy.loginfo("Message published successfully.")
        sys.exit(0)  # Return 0 on success
    else:
        rospy.logerr("Failed to publish message.")
        sys.exit(1)  # Return 1 on failure

if __name__ == '__main__':
    main()
