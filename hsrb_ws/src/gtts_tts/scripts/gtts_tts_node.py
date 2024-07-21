#!/usr/bin/env python3
import rospy
from tmc_msgs.msg import Voice
from gtts import gTTS
import os

def text_to_speech(text, language):
    tts = gTTS(text=text, lang=language)
    tts.save("/tmp/tts_output.mp3")
    os.system("mpg321 /tmp/tts_output.mp3")

def main():
    rospy.init_node('gtts_tts_node', anonymous=True)
    
    pub = rospy.Publisher('/talk_request', Voice, queue_size=10)
    
    while not rospy.is_shutdown():
        # 获取用户输入
        sentence = input("Enter the text you want the robot to say: ")
        language = input("Enter the language (en for English, ja for Japanese): ")
        
        # 创建 Voice 消息
        voice_msg = Voice()
        voice_msg.interrupting = False
        voice_msg.queueing = False
        voice_msg.language = Voice.kEnglish if language == 'en' else Voice.kJapanese
        voice_msg.sentence = sentence
        
        # 发布消息
        rospy.loginfo("Publishing message to /talk_request")
        pub.publish(voice_msg)
        
        # 直接进行语音合成
        text_to_speech(sentence, language)

if __name__ == '__main__':
    main()
