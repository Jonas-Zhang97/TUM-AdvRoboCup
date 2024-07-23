import tkinter as tk
from tkinter import ttk
import openai
import rospy
from std_msgs.msg import String
import threading

import speech_recognition as sr
import pyaudio
import subprocess




def send_message():
    message = entry.get()  
    display.insert(tk.END, "User: {}\n".format(message))
    entry.delete(0, tk.END)  # clean input
    display.see(tk.END) 
    # Publish user input as a ROS topic
    pub.publish(message)


def voice_input():
    def start_recording():
        voice_input_button.config(text="Recording...")

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)

        try:
            message = recognizer.recognize_google(audio)
            entry.delete(0, tk.END)  # Clear the current text in the entry widget
            entry.insert(tk.END, message)  # Insert the recognized text into the entry widget
        except sr.UnknownValueError:
            display.insert(tk.END, "AI: Sorry, say again.\n")
        except sr.RequestError as e:
            display.insert(tk.END, "AI: Sorry, an error occurred while processing your speech: {}\n".format(str(e)))

        voice_input_button.config(text="Voice Input")

    voice_input_button.config(text="Recording...")
    threading.Thread(target=start_recording).start()


def receive_message(data):
    message = data.data
    display.insert(tk.END, "AI: {}\n".format(message))
    display.see(tk.END)  # Scroll to the bottom of the text display

def reset_dialog():
    display.delete(1.0, tk.END)

def ros_spin():
    rospy.spin()


# def start_openai_ros_node():
#     subprocess.Popen(['rosrun','wpr_chatgpt','openai_ros.py'])



rospy.init_node('gui_chatgpt')

# Create a ROS publisher
pub = rospy.Publisher('openai/prompt', String, queue_size=10)
# Create a ROS subscriber
rospy.Subscriber('openai/response', String, receive_message)


# Initialize PyAudio
audio = pyaudio.PyAudio()


# MAIN INTERFACE
window = tk.Tk()
window.title("Chatbot")
window.geometry("1200x1500")

group_name = "Group1"
group_members = "Jia Li, Zhihao Yu, Runcong Wang"  
group_info = tk.Label(window, text="Group Name: {}\nGroup Members: {}".format(group_name, group_members))
group_info.pack()

# Create text display area
display = tk.Text(window, height=35)
display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create voice input buttonu
entry = tk.Entry(window,  width=100 )
entry.pack(padx=20, pady=20, fill=tk.X)
entry.configure(font=("Arial", 12))


# Create button volume
button_frame = tk.Frame(window)
button_frame.pack(padx=20, pady=20, fill=tk.X, expand=True)

# Create reset button
reset_button = tk.Button(button_frame, text="Reset Dialog", command=reset_dialog, width=15, height=2)
reset_button.pack(side=tk.LEFT, padx=5, expand=True)


# Create voice input button
is_recording = False
voice_input_button = tk.Button(button_frame, text="Voice Input", command=voice_input, width=15, height=2)
voice_input_button.pack(side=tk.LEFT, padx=5, expand=True)


#create send button
send_button = tk.Button(button_frame, text="Send Message", command=send_message, width=15, height=2)
send_button.pack(side=tk.LEFT, padx=5, expand=True)


# Start the ROS spin thread
ros_spin_thread = threading.Thread(target=ros_spin)
ros_spin_thread.start()


# Run the main loop
window.mainloop()
