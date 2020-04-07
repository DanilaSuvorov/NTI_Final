# coding: utf8

import rospy
from clever import srv
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

# Взлет на высоту 1 м
navigate(x=0, y=0, z=1, frame_id='body', auto_arm=True)

# Ожидание 3 секунды
rospy.sleep(3)

# 1
navigate(x=0.295, y=0.295, z=0, frame_id='body')
rospy.sleep(3)

# 2
navigate(x=0.59, y=0, z=0, frame_id='body')
rospy.sleep(3)

# 3
navigate(x=-0.59, y=0.59, z=0, frame_id='body')
rospy.sleep(3)

# 4
navigate(x=0.59, y=0.59, z=0, frame_id='body')
rospy.sleep(3)

# 5
navigate(x=-0.59, y=0.59, z=0, frame_id='body')
rospy.sleep(3)

# 6
navigate(x=0.59, y=0, z=0, frame_id='body')
rospy.sleep(3)

# 7
navigate(x=-0.59, y=0.59, z=0, frame_id='body')
rospy.sleep(3)

# 8
navigate(x=0.59, y=0, z=0, frame_id='body')
rospy.sleep(3)

# 9
navigate(x=-0.295, y=0.59, z=0, frame_id='body')
rospy.sleep(3)

# возвращение домой
navigate(x=-0.59, y=-2.655, z=0, frame_id='body')
rospy.sleep(3)
navigate(x=0, y=0, z=-1, frame_id='body', auto_arm=True)

# Посадка
land()