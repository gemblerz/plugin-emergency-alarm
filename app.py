import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from demo_interfaces.msg import Heartbeat, EmergencyAlert

class AlertManager(Node):
    def __init__(self):
        super().__init__('emergency_alert_manager')
        self.objects = dict()
        self.name = self.get_namespace()[1:]
        self.pub_heartbeat = self.create_publisher(Heartbeat, 'state', 10)
        self.pub_alert = self.create_publisher(EmergencyAlert, '/emergency', 10)
        self.sub_objectdetection  = self.create_subscription(String,'/object',self.detection_callback,10)
        timer_period = 1.  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info("Emergency alert system running!")

    def detection_callback(self, msg):
        self.objects[msg.data] = time.time()

    def timer_callback(self):
        # msg = Heartbeat()
        # msg.data = "BUSY"
        # self.pub_heartbeat.publish(msg)
        if "cat" in self.objects:
            # if a cat was detected within 5 seconds
            if time.time() - self.objects["cat"] < 5.:
                msg = EmergencyAlert()
                msg.message = "A cat is detected!"
                msg.is_emergency = True
                self.pub_alert.publish(msg)



if __name__ == '__main__':
    rclpy.init()
    am = AlertManager()
    rclpy.spin(am)
