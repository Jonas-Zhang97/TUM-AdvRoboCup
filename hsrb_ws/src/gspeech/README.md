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

Before use:

The package include speech recognition module. First type

arecord -l
to find your audio input device, for example, card 4, device 0, then change self.sox_cmd in gspeech.py accordingly. Here, the self.sox_cmd should be

self.sox_cmd = "sox -r 48000 -c 1 -t alsa hw:4,0  recording.flac silence 1 0.1 1% 1 1.5 1%"
where hw:4,0 represent card 4, device 0.


-----
`rosrun gspeech gspeech.py `

To check published msg from aruco_detector:

```shell
rostopic echo /aruco_marker_info
```
To check what returns from speech recognition module:
```shell
rostopic echo /gspeech/speech
```

