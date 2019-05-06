## Impaired Home Automation

Advanced Studio Project @ AIT

6201 Mohammed Tantawy - 6678 Davide Bragagnolo

### Indoor Positioning System

in order to run the script, you must have

- a RaspberryPI with Camera Module
- Raspbian Stretch
- OpenCV module (see references)

start the script with `python3 iha_ips_console.py`

open the browser to  `http://<ip_of_your_raspberry>:8000`

#### References

Install OpenCV from [PiWheels](https://blog.piwheels.org/new-opencv-builds/), just run:
`
sudo apt install libatlas3-base libwebp6 libtiff5 libjasper1 libilmbase12 libopenexr22 libilmbase12 libgstreamer1.0-0 libavcodec57 libavformat57 libavutil55 libswscale4 libqtgui4 libqt4-test libqtcore4`
`sudo pip3 install opencv-python`

How to track object with OpenCV: [https://www.instructables.com/id/Automatic-Vision-Object-Tracking/](https://www.instructables.com/id/Automatic-Vision-Object-Tracking/)