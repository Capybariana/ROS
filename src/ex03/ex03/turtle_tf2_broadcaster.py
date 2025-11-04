import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
import tf_transformations
import tf2_ros
from geometry_msgs.msg import TransformStamped

class TurtleBroadcaster(Node):
    def __init__(self):
        super().__init__('turtle_tf2_broadcaster')
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.handle_turtle_pose, 10)
        self.br = tf2_ros.TransformBroadcaster(self)

    def handle_turtle_pose(self, msg):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'turtle1'
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0
        q = tf_transformations.quaternion_from_euler(0, 0, msg.theta)
        t.transform.rotation.x, t.transform.rotation.y, t.transform.rotation.z, t.transform.rotation.w = q
        self.br.sendTransform(t)

def main():
    rclpy.init()
    node = TurtleBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()
