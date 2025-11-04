import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from cleaning_robot_msgs.action import CleaningTask
import math
import time

class CleaningActionServer(Node):

    def __init__(self):
        super().__init__("cleaning_action_server")
        self._action_server = ActionServer(
            self, CleaningTask, "cleaning_task", self.execute_callback
        )
        self.cmd_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.pose = None
        self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)

        # Параметры уборки
        self.cleaning_width = 0.5  
        self.linear_speed = 1.0
        self.angular_speed = 1.0

    def pose_callback(self, msg):
        self.pose = msg

    def execute_callback(self, goal_handle):
        goal = goal_handle.request
        self.get_logger().info(f"Received goal: {goal.task_type}")

        feedback_msg = CleaningTask.Feedback()
        result = CleaningTask.Result()
        total_distance = 0.0
        cleaned_points = 0

        while self.pose is None:
            rclpy.spin_once(self)
            time.sleep(0.1)

        if goal.task_type == "clean_square":
            start_x = goal.target_x
            start_y = goal.target_y
            total_distance, cleaned_points = self.clean_square_snake(
                start_x, start_y, goal.area_size, goal_handle, feedback_msg
            )
        elif goal.task_type == "return_home":
            total_distance = self.move_to(
                goal.target_x, goal.target_y, goal_handle, feedback_msg
            )
            cleaned_points = 0

        result.success = True
        result.cleaned_points = cleaned_points
        result.total_distance = total_distance
        goal_handle.succeed()
        self.get_logger().info(
            f"Goal completed. Distance: {total_distance:.2f}, Points: {cleaned_points}"
        )
        return result

    def clean_square_snake(
        self, start_x, start_y, square_size, goal_handle, feedback_msg
    ):
        total_distance = 0.0
        cleaned_points = 0

        half_size = square_size / 2.0
        left_bound = max(0.5, start_x - half_size)
        right_bound = min(10.5, start_x + half_size)
        bottom_bound = max(0.5, start_y - half_size)
        top_bound = min(10.5, start_y + half_size)

        self.get_logger().info(f"Cleaning square from ({start_x:.2f}, {start_y:.2f})")
        self.get_logger().info(
            f"Bounds: X[{left_bound:.2f}-{right_bound:.2f}], Y[{bottom_bound:.2f}-{top_bound:.2f}]"
        )

        current_x = left_bound
        current_y = bottom_bound

        total_distance += self.move_to(current_x, current_y, goal_handle, feedback_msg)

        direction = 1 
        lane_count = 0

        height = top_bound - bottom_bound
        num_lanes = int(height / self.cleaning_width)

        for lane in range(num_lanes + 1):
            if direction == 1:
                target_x = right_bound
            else:
                target_x = left_bound

            total_distance += self.move_to(
                target_x, current_y, goal_handle, feedback_msg
            )
            cleaned_points += int(
                abs(target_x - current_x) / 0.1
            ) 

            if goal_handle.is_active:
                progress = min(100, int((lane + 1) / (num_lanes + 1) * 100))
                feedback_msg.progress_percent = progress
                feedback_msg.current_cleaned_points = cleaned_points
                feedback_msg.current_x = self.pose.x
                feedback_msg.current_y = self.pose.y
                goal_handle.publish_feedback(feedback_msg)

            if lane < num_lanes:
                current_y += self.cleaning_width
                total_distance += self.move_to(
                    target_x, current_y, goal_handle, feedback_msg
                )
                cleaned_points += 5 

            direction *= -1
            lane_count += 1

        return total_distance, cleaned_points


    def move_to(self, target_x, target_y, goal_handle=None, feedback_msg=None):
        distance_traveled = 0.0
        last_pose = self.pose

        while math.hypot(target_x - self.pose.x, target_y - self.pose.y) > 0.1:
            if goal_handle and not goal_handle.is_active:
                return distance_traveled

            dx = target_x - self.pose.x
            dy = target_y - self.pose.y
            target_angle = math.atan2(dy, dx)
            angle_error = target_angle - self.pose.theta

            while angle_error > math.pi:
                angle_error -= 2 * math.pi
            while angle_error < -math.pi:
                angle_error += 2 * math.pi

            distance = math.hypot(dx, dy)

            msg = Twist()
            if abs(angle_error) > 0.1:
                msg.angular.z = max(
                    -self.angular_speed, min(self.angular_speed, angle_error)
                )
            else:
                msg.linear.x = min(self.linear_speed, distance)
                msg.angular.z = 0.0

            self.cmd_pub.publish(msg)

            if last_pose:
                distance_traveled += math.hypot(
                    self.pose.x - last_pose.x, self.pose.y - last_pose.y
                )
            last_pose = self.pose5

            if goal_handle and feedback_msg and goal_handle.is_active:
                feedback_msg.current_x = self.pose.x
                feedback_msg.current_y = self.pose.y
                goal_handle.publish_feedback(feedback_msg)

            rclpy.spin_once(self)
            time.sleep(0.05)

        stop_msg = Twist()
        self.cmd_pub.publish(stop_msg)
        time.sleep(0.1)

        return distance_traveled


def main(args=None):
    rclpy.init(args=args)
    server = CleaningActionServer()

    try:
        rclpy.spin(server)
    except KeyboardInterrupt:
        pass
    finally:
        server.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
