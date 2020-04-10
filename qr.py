# coding: utf8
import cv2
import rospy
import numpy as np
from clever import srv
from pyzbar import pyzbar
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from clever.srv import SetLEDEffect
from std_srvs.srv import Trigger

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
cap = rospy.wait_for_message('main_camera/image_raw', Image)


bad_num = []
bad_value = []


bridge = CvBridge()


# Image subscriber callback function
def image_callback(data):
    cv_image = bridge.imgmsg_to_cv2(data, 'bgr8')  # OpenCV image
    barcodes = pyzbar.decode(cv_image)
    for barcode in barcodes:
        b_data = barcode.data.encode("utf-8")
        b_type = barcode.type
        (x, y, w, h) = barcode.rect
        xc = x + w / 2
        yc = y + h / 2
        cv2.putText(cv_image, "QR-код!", (xc, yc), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        print("Был найден {} со значением {} с центром в точках x={}, y={}".format(b_type, b_data, xc, yc))
        if b_data == "COVID - 2019":
            set_effect(r=255, g=0, b=0)  # пометка зараженного
            print("Заражен")
            rospy.sleep(5)
        bad_value.append(b_data)


image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback, queue_size=1)


# Взлет
navigate(x=0, y=0, z=0.6, frame_id='body', speed=0.5, auto_arm=True)

rospy.sleep(10)

# 1
navigate(x=0.295, y=0.295, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 2
navigate(x=0.295, y=0.885, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 3
navigate(x=0.295, y=1.475, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 4
navigate(x=0.295, y=2.065, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 5
navigate(x=0.59, y=2.655, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 6
navigate(x=0.885, y=2.065, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 7
navigate(x=0.885, y=1.475, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 8
navigate(x=0.885, y=0.885, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 9
navigate(x=0.885, y=0.295, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# возвращение домой
navigate(x=0, y=0, z=0, speed=0.65, frame_id='aruco_map')
rospy.sleep(5)

# Посадка
land()

# Проверка на правильность всех данных
print(bad_num)
print(bad_value)