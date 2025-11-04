import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from tf2_ros import Buffer, TransformListener, LookupException, ConnectivityException, ExtrapolationException
from rclpy.duration import Duration
import math

class TurtleFollower(Node):
    def __init__(self):
        super().__init__('turtle_tf2_listener_delay')
        self.declare_parameter('delay', 2.0)
        self.delay = self.get_parameter('delay').get_parameter_value().double_value
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.pub = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        try:
            now = self.get_clock().now()
            past = now - Duration(seconds=self.delay)
            trans = self.tf_buffer.lookup_transform('turtle2', 'turtle1', past.to_msg())
        except (LookupException, ConnectivityException, ExtrapolationException) as ex:
            self.get_logger().warn(f'Cannot transform: {ex}')
            return

        msg = Twist()
        msg.angular.z = 4.0 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
        msg.linear.x = 0.5 * math.sqrt(
            trans.transform.translation.x**2 + trans.transform.translation.y**2
        )
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = TurtleFollower()
    rclpy.spin(node)
    rclpy.shutdown()
