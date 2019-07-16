#!/usr/bin/python
import rospy
from geometry_msgs.msg import WrenchStamped
from std_msgs.msg import String

class CollectData(object):
    def __init__(self):
        rospy.Subscriber('leptrino/force_torque', WrenchStamped, self.sensor_callback)
        rospy.Subscriber('/subjectA/record_device', String, self.response_callback)
        self.sensor_data = None
        self.save_to_file_flag = False
        self.initial_time = time.time()
        self.file = None

    def sensor_callback(self, msg):
        self.sensor_data = msg

    def response_callback(self, msg):
        self.save_to_file_flag = True
        self.file = open(msg.data, "w")
        self.file.write("time,force_x,force_y,force_z,torque_x,torque_y,torque_z\n")
         
    def update(self):
        if self.sensor_data:
            time = self.sensor_data.header.stamp.sec
            force_x = self.sensor_data.wrench.force.x
            force_y = self.sensor_data.wrench.force.y
            force_z = self.sensor_data.wrench.force.z
            torque_x = self.sensor_data.wrench.torque.x
            torque_y = self.sensor_data.wrench.torque.y
            torque_z = self.sensor_data.wrench.torque.z
            if self.save_to_file_flag:
                self.file.write(str(time)+",")
                self.file.write(str(force_x)+",")
                self.file.write(str(force_y)+",")
                self.file.write(str(force_z)+",")
                self.file.write(str(torque_x)+",")
                self.file.write(str(torque_y)+",")
                self.file.write(str(torque_z)+"\n")
                if time.time() - self.initial_time > 10:
                    self.save_to_file_flag = False
                    self.file.close()
            else:
                self.initial_time = time.time()
        
if __name__ == '__main__':
    rospy.init_node('collect_data', anonymous=True)
    rate = rospy.Rate(1200) #10hz
    node = CollectData()
    try:
        while not rospy.is_shutdown():
            node.update()
            rate.sleep()

    except rospy.ROSInterruptException:
        node.file.close()
