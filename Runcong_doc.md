# Documentation: Pkgs Created by Runcong

This documentation will cover the following packages



- depth_segmentation_alternative: sam_ros, generate target object point cloud;
- gspeech: speech recognition
- state machine

## sam_ros:

```
rosrun sam_fp samros.py "beer"
rosrun sam_fp pcd_processing_node
```

where "beer" is the item that one want to segment. No argument for everything segmentation.



## Gspeech

Before use:



The package include speech recognition module. First type

```
arecord -l
```



 to find your audio input device, for example, card 4, device 0, then change self.sox_cmd in gspeech.py accordingly. Here, the self.sox_cmd should be

```py
self.sox_cmd = "sox -r 48000 -c 1 -t alsa hw:4,0 recording.flac silence 1 0.1 1% 1 1.5 1%"
```

 where hw:4,0 represent card 4, device 0.



The package include two python scripts. gspeech.py is suitable for python 2 and old version of google cloud , while the gspeech_new.py for python 3 and new google cloud api.