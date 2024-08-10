import subprocess


result = subprocess.call(['roslaunch', 'gtts_tts', 'gtts_tts.launch', 
                          'sentence:=This is a test sentence', 'language:=en'])


if result == 0:
    print("roslaunch succeeded")
else:
    print(f"roslaunch failed with return code: {result}")
