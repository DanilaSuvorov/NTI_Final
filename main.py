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


# Определяет, есть ли цвет на фотографии
def findcol(lower_color, upper_color, color_name):
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_color, upper_color)
    res = []
    # Bitwise-AND mask and original image
    cv2.bitwise_and(frame, mask, res)
    result = ""
    for i in res:
        if i == 1:
            result = color_name
            break
    return result


# Заполняет массив и помечает потенциально зараженных
def allcolor():
    if findcol(hsv_mingreen, hsv_maxgreen, '-') == '-':
        people.append('-')
    elif findcol(lower_red, upper_red, '+') == '+':
        people.append("+")
        set_effect(r=128, g=0, b=128)  # пометка зараженного
    elif findcol(lower_yellow, upper_yellow, '?') == '?':
        people.append('?')
        set_effect(r=128, g=0, b=128)  # пометка зараженного


rospy.init_node('flight')

# Настройка телеметрии и объявление переменных
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
cap = cv2.VideoCapture(0)
hsv_mingreen = np.array((53, 0, 0), np.uint8)
hsv_maxgreen = np.array((83, 255, 255), np.uint8)
lower_red = np.array([0, 70, 50])
upper_red = np.array([10, 255, 255])
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
people = ["", "", "", "", "", "", "", "", ""]
result = ""
ans = ""

# Первый взлет
# Взлет
navigate(x=0, y=0, z=0.6, frame_id='body', speed=0.5, auto_arm=True)

rospy.sleep(10)

# 1
navigate(x=0.295, y=0.295, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 2
navigate(x=0.885, y=0.295, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 3
navigate(x=0.295, y=0.885, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 4
navigate(x=0.885, y=0.885, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 5
navigate(x=0.295, y=1.475, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 6
navigate(x=0.885, y=1.475, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 7
navigate(x=0.295, y=2.065, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 8
navigate(x=0.885, y=2.065, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 9
navigate(x=0.59, y=2.655, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# возвращение домой
navigate(x=0, y=0, z=0, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# Посадка
land()

# Проверка массива на правильность заполнения
print(people)

# ожидание на базе
rospy.sleep(120)

bad_num = []
bad_value = []

for x in range(len(people)):
    if people[x] == "?" or people[x] == "+":
        bad_num.append(x)

rospy.init_node('barcode_test')

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

rospy.spin()

# Второй взлет
# Взлет
navigate(x=0, y=0, z=0.6, frame_id='body', speed=0.5, auto_arm=True)

# Ожидание 10 секунд
rospy.sleep(10)

# 1
navigate(x=0.295, y=0.295, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 2
navigate(x=0.885, y=0.295, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 3
navigate(x=0.295, y=0.885, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 4
navigate(x=0.885, y=0.885, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 5
navigate(x=0.295, y=1.475, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 6
navigate(x=0.885, y=1.475, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 7
navigate(x=0.295, y=2.065, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 8
navigate(x=0.885, y=2.065, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# 9
navigate(x=0.59, y=2.655, z=0.6, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# возвращение домой
navigate(x=0, y=0, z=0, speed=0.8, frame_id='aruco_map')
rospy.sleep(5)

# Посадка
land()

# Проверка на правильность всех данных
print(bad_num)
print(bad_value)
