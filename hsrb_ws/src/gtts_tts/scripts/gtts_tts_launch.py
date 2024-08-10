#!/usr/bin/env python3
import rospy
from tmc_msgs.msg import Voice
from std_msgs.msg import String  # Import String message type
from gtts import gTTS
import os
import sys

def text_to_speech(text, language):
    try:
        tts = gTTS(text=text, lang=language)
        tts.save("/tmp/tts_output.mp3")
        result = os.system("mpg321 /tmp/tts_output.mp3")
        
        # Check the return value of mpg321
        if result == 0:
            return True
        else:
            return False
    except Exception as e:
        rospy.logerr(f"Text-to-speech failed: {e}")
        return False

def main():
    rospy.init_node('gtts_tts_node', anonymous=True)
    
    sentence = rospy.get_param('~sentence', 'Hello, Operator!')
    language = rospy.get_param('~language', 'en')
    
    pub = rospy.Publisher('/talk_request', Voice, queue_size=10)
    status_pub = rospy.Publisher('/tts_status', String, queue_size=10)  # Create a publisher for the tts_status topic
    
    voice_msg = Voice()
    voice_msg.interrupting = False
    voice_msg.queueing = False
    voice_msg.language = Voice.kEnglish if language == 'en' else Voice.kJapanese
    voice_msg.sentence = sentence
    
    rospy.loginfo("Publishing message to /talk_request")
    pub.publish(voice_msg)
    
    # Perform text-to-speech synthesis and check success or failure
    success = text_to_speech(sentence, language)
    
    # Publish the tts_status topic based on the result
    if success:
        status_msg = String(data="TTS success")
        rospy.loginfo("TTS succeeded")
        status_pub.publish(status_msg)
        sys.exit(0)
    else:
        status_msg = String(data="TTS failed")
        rospy.loginfo("TTS failed")
        status_pub.publish(status_msg)
        sys.exit(1)

if __name__ == '__main__':
    main()
