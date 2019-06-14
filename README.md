## Impaired Home Automation

Advanced Studio Project @ AIT

6201 Mohammed Tantawy - 6678 Davide Bragagnolo

### Indoor Positioning System

This project has been created for a project during our Bachelor of IT course. This is intended to be used with the [IHA Robot](https://github.com/imphomeauto/robot-wheelchair)

### Instructions

in order to run the script, you must have

- a RaspberryPI with Camera Module
- Raspbian Stretch
- OpenCV module (see references)
- position of the camera and configure properly the color for the object (READ CONFIGURATION)

start the positioning system with `python3 ips.py`
the robot will take the position at the socket address `<ip_of_your_raspberry>:8000`

### Configuration

The Camera needs to be positioned at about 90cm from the ground that looks the floor/ground.

The robot (object to recognize the position) needs to have a color that be easily recognizable by the OpenCV script, depending on the ambient/room light and floor/ground color. During our tests, we found that the best colors are fluo orange or fluo green.

The IPS script uses HSV colors, to configure the color:
- connect the Raspberry with a monitor + keyboard + mouse (or connect with VNC)
- open a terminal and launch the script `python3 iha_ips_frame.py` it will open a window frame with the camera view
- with the mouse, click on the object to get the position, on the bottom left of the frame you will see the color in RGB format, for example R(12) G(180) B(65)
- close the window and launch another script from the terminal, the script to launch is `python3 references/bgr_hsv_converter.py B G R` and replace `B G R` with the colors, using the previous example the script will be `python3 references/bgr_hsv_converter.py 65 180 12`
- the script will return 2 values, for example `[65, 100, 100]` and `[85, 255, 255]`
- edit the `ips.py` script and adjust the colors inside the class Pos() method run()

#### Other commands

get the real-time position in the console `python3 iha_ips_console.py`

get the real-time position in the web server `python3 iha_ips_web.py` position can be read at the address `http://<ip_of_your_raspberry>:8000`

get the position with the frame, useful to map the color of the object (you must run this in the Desktop Env, or in VNC) `python3 iha_ips_frame.py`

##### References

Install OpenCV from [PiWheels](https://blog.piwheels.org/new-opencv-builds/), just run:
`
sudo apt install libatlas3-base libwebp6 libtiff5 libjasper1 libilmbase12 libopenexr22 libilmbase12 libgstreamer1.0-0 libavcodec57 libavformat57 libavutil55 libswscale4 libqtgui4 libqt4-test libqtcore4`
`sudo pip3 install opencv-python`

How to track object with OpenCV: [https://www.instructables.com/id/Automatic-Vision-Object-Tracking/](https://www.instructables.com/id/Automatic-Vision-Object-Tracking/)