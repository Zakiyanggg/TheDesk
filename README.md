# TheDesk
Final Project of ESE519 Fall2021
We decided to design a system that can automatically locate your phone on a surface and the wireless charging base will move to the right position and start charging your phone or other wireless charging device. This could be applied to a bed side table or a working desk. Our initial idea is using Raspberry Pi to support the CV part and generate coordination information to the motor control system, which we prefer to use an UNO board. For sensors, we just need a webcam to capture the object on the table surface. We might upgrade the camera to stereo type in order to get more accurate location information. We need two step motors to drive the linear slide rails. Two sets of linear rails can let the charging pad move across the entire surface. A charging pad that supports most common fast charging devices. It might be hard to train the ML module to recognize a smart phone on a messy table and Raspberry pi only supports a few packages for computer vision modules includes TensorFlow Lite, Coco and etc. which the functionality is quite limited. We also need to design a system to collect the free wires flying around two rails, to make sure they won’t entangle. For safety features, We need to put switches that prevent the motors going too far that might damage the rails or gears. 

Dev:
https://devpost.com/software/the-desk
YT:
https://youtu.be/40HvZxAWwoY
