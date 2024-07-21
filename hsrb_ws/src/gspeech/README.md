gspeech
=======

ROS package for speech recognition based on Google Speech API



NOTE: This package needs a key to use the google speech to text API, each key can be used
      for 50 times (you can make 50 request per key to the google server), and each
      request is accepted if the audio duration is less than 15 seconds.

      For key generation see: http://www.chromium.org/developers/how-tos/api-keys
      Dont forget to add your key before using the gspeech node. 
NOTE: This package does not work now, seems that Google changed their APIs/policies or authentication  methods

UPD: Fixed, now working with API v2, you need an API Key from  Google Developer Console


Usage
-----
Before use:

First type 

```bash
arecord -l
```

to find your audio input device, for example, card 4, device 0, then change  self.sox_cmd in gspeech.py accordingly. Here, the self.sox_cmd should be

```python
self.sox_cmd = "sox -r 48000 -c 1 -t alsa hw:4,0  recording.flac silence 1 0.1 1% 1 1.5 1%"
```

where hw:4,0 represent card 4, device 0.

`rosrun gspeech gspeech.py `

To check what returns from speech recognition module:

```bash
rostopic echo /gspeech/speech
```



Some dependencies have to be install, the following installation is for ros 18.04 and python2, not tested yet, do NOT add directly to the dockerfile:

```dockerfile
RUN sudo apt install -y portaudio19-dev \
    && pip install --upgrade "pip<21.0" \
    && pip install --upgrade wheel \
    && pip install pyaudio==0.2.9 \
    && pip install "pyasn1>=0.4.6,<0.6.0" \
    && pip install "six>=1.13.0" \
    && pip install google-cloud==0.22.0 \
    && pip install google-cloud-speech \
    && pip install requests \
    && sudo apt install -y \
        ros-kinetic-audio-common \
        alsa-base alsa-utils \
        gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly\
        sox   
```

