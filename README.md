## Impaired Home Automation

Advanced Studio Project @ AIT

6201 Mohammed Tantawy - 6678 Davide Bragagnolo

### Indoor Positioning System

in order to run the script, you must have

- a RaspberryPI with Camera Module
- Raspbian Stretch
- OpenCV module (see references)

start the positioning system with `python3 iha_ips_ws.py`
the robot will take the position at the socket address `<ip_of_your_raspberry>:8000`

### Other commands

get the real-time position in the console `python3 iha_ips_console.py`

get the real-time position in the web server `python3 iha_ips_web.py` position can be read at the address `http://<ip_of_your_raspberry>:8000`

get the position with the frame, useful to map the color of the object (you must run this in the Desktop Env, or in VNC) `python3 iha_ips_frame.py`

#### References

Install OpenCV from [PiWheels](https://blog.piwheels.org/new-opencv-builds/), just run:
`
sudo apt install libatlas3-base libwebp6 libtiff5 libjasper1 libilmbase12 libopenexr22 libilmbase12 libgstreamer1.0-0 libavcodec57 libavformat57 libavutil55 libswscale4 libqtgui4 libqt4-test libqtcore4`
`sudo pip3 install opencv-python`

How to track object with OpenCV: [https://www.instructables.com/id/Automatic-Vision-Object-Tracking/](https://www.instructables.com/id/Automatic-Vision-Object-Tracking/)