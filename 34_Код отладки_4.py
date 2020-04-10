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

bridge = CvBridge()

lower_green = np.array([50, 50, 70])
upper_green = np.array([103, 255, 255])

lower_red = np.array([10, 50, 50])
upper_red = np.array([179, 255, 255])

lower_yellow = np.array([22, 93, 0])
upper_yellow = np.array([45, 255, 255])


def findcol(lower_color, upper_color, color_name):
    # Take each frame
    cap = rospy.wait_for_message('main_camera/image_raw', Image)
    img = bridge.imgmsg_to_cv2(cap, 'bgr8')

    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_color, upper_color)

    result = ""

    if mask.any():
        result = color_name

    return result


def allcolor():
    if findcol(lower_green, upper_green, '-') == '-':
        people.append('-')
    elif findcol(lower_red, upper_red, '+') == '+':
        people.append("+")
        set_effect(r=128, g=0, b=128)  # пометка зараженного
        print("Тест сброшен")
        rospy.sleep(5)
    elif findcol(lower_yellow, upper_yellow, '?') == '?':
        people.append('?')
        set_effect(r=128, g=0, b=128)  # пометка зараженного
        print("Тест сброшен")
        rospy.sleep(5)


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

people = []
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
navigate(x=0.295, y=0.885, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 3
navigate(x=0.295, y=1.475, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 4
navigate(x=0.295, y=2.065, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 5
navigate(x=0.59, y=2.655, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 6
navigate(x=0.885, y=2.065, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 7
navigate(x=0.885, y=1.475, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 8
navigate(x=0.885, y=0.885, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# 9
navigate(x=0.885, y=0.295, z=0.6, speed=0.8, frame_id='aruco_map')
allcolor()
rospy.sleep(5)

# возвращение домой
navigate(x=0, y=0, z=0, speed=0.65, frame_id='aruco_map')
rospy.sleep(5)

# Посадка
land()
print(people)

rospy.sleep(120)  # ожидание на базе

bad_num = []
bad_value = []

for x in range(len(people)):
    if people[x] == "?" or people[x] == "+":
        bad_num.append(x)

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


# Функция полета по конкретным пациентам
def target(num):
    if num == 1:
        navigate(x=0.295, y=0.295, z=0.6, speed=0.8, frame_id='aruco_map')
        rospy.sleep(5)
    elif num == 2:
        navigate(x=0.295, y=0.885, z=0.6, speed=0.8, frame_id='aruco_map')
        rospy.sleep(5)
    elif num == 3:
        navigate(x=0.295, y=1.475, z=0.6, speed=0.8, frame_id='aruco_map')
        rospy.sleep(5)
    elif num == 4:
        navigate(x=0.295, y=2.065, z=0.6, speed=0.8, frame_id='aruco_map')
        rospy.sleep(5)
    elif num == 5:
        navigate(x=0.59, y=2.655, z=0.6, speed=0.8, frame_id='aruco_map')
        rospy.sleep(5)
    elif num == 6:
        navigate(x=0.885, y=2.065, z=0.6, speed=0.8, frame_id='aruco_map')
        rospy.sleep(5)
    elif num == 7:
        navigate(x=0.885, y=1.475, z=0.6, speed=0.8, frame_id='aruco_map')
        rospy.sleep(5)
    elif num == 8:
        navigate(x=0.885, y=0.885, z=0.6, speed=0.8, frame_id='aruco_map')
        rospy.sleep(5)
    else:
        navigate(x=0.885, y=0.295, z=0.6, speed=0.8, frame_id='aruco_map')
        rospy.sleep(5)


# Второй взлет
# Взлет
navigate(x=0, y=0, z=0.6, frame_id='body', speed=0.5, auto_arm=True)

# Ожидание 10 секунд
rospy.sleep(10)

for n in bad_num:
    target(n)

# возвращение домой
navigate(x=0, y=0, z=0, speed=0.8, frame_id='aruco_map')

# Проверка на правильность всех данных
print(bad_num)
print(bad_value)
