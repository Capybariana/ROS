import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class TextToCmdVel(Node):
    def __init__(self):
        super().__init__('text_to_cmd_vel')
       
        self.subscription = self.create_subscription(
            String,
            'cmd_text',
            self.listener_callback,
            10
        )
        self.subscription  

        # Публикация в /turtle1/cmd_vel
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info('TextToCmdVel node has been started.')

    def listener_callback(self, msg):
        cmd = msg.data.lower().strip()
        twist = Twist()

        if cmd == 'move_forward':
            twist.linear.x = 1.0
        elif cmd == 'move_backward':
            twist.linear.x = -1.0
        elif cmd == 'turn_left':
            twist.angular.z = 1.5
        elif cmd == 'turn_right':
            twist.angular.z = -1.5
        else:
            self.get_logger().warn(f'Unknown command: {cmd}')
            return

        self.publisher.publish(twist)
        self.get_logger().info(f'Command executed: {cmd}')

def main(args=None):
    rclpy.init(args=args)
    node = TextToCmdVel()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
