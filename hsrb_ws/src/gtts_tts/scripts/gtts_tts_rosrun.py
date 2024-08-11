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
    
    # 从参数服务器获取参数
    sentence = rospy.get_param('~sentence', 'Hello, this is the default message.')
    language = rospy.get_param('~language', 'en')
    
    pub = rospy.Publisher('/talk_request', Voice, queue_size=10)
    
    # 创建 Voice 消息
    voice_msg = Voice()
    voice_msg.interrupting = False
    voice_msg.queueing = False
    voice_msg.language = Voice.kEnglish if language == 'en' else Voice.kJapanese
    voice_msg.sentence = sentence
    
    # 直接进行语音合成并播放
    text_to_speech(sentence, language)

    # 发布消息并检查是否成功
    rospy.loginfo("Publishing message to /talk_request")
    pub.publish(voice_msg)
    
    # 等待消息发布完成
    if pub.get_num_connections() > 0:
        rospy.loginfo("Message published successfully.")
        sys.exit(0)  # 成功返回 0
    else:
        rospy.logerr("Failed to publish message.")
        sys.exit(1)  # 失败返回 1

if __name__ == '__main__':
    main()
