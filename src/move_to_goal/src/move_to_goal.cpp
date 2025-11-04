#include <cmath>
#include <memory>
#include <string>
#include <vector>
#include <iostream>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp/qos.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"

using std::placeholders::_1;

static double ang_normalize(double a) {
  // (-pi, pi]
  a = std::fmod(a + M_PI, 2.0 * M_PI);
  if (a < 0) a += 2.0 * M_PI;
  return a - M_PI;
}

class MoveToGoalNode : public rclcpp::Node {
public:
  MoveToGoalNode(double gx, double gy, double gth)
  : Node("move_to_goal"),
    goal_x_(gx),
    goal_y_(gy),
    goal_theta_(ang_normalize(gth))
  {
    // Параметры контроллера
    k_lin_ = 1.2;
    k_ang_ = 4.0;
    k_theta_ = 3.0;
    max_lin_ = 2.0;
    max_ang_ = 2.0;
    dist_tol_ = 0.05;
    theta_tol_ = 0.02;

    // QoS как у sensor data: BEST_EFFORT
    rclcpp::QoS qos(rclcpp::KeepLast(10));
    qos.best_effort();

    pose_sub_ = this->create_subscription<turtlesim::msg::Pose>(
      "/turtle1/pose", qos, std::bind(&MoveToGoalNode::pose_cb, this, _1));

    cmd_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);

    RCLCPP_INFO(get_logger(), "Goal: x=%.3f y=%.3f theta=%.3f rad", goal_x_, goal_y_, goal_theta_);
  }

private:
  enum class State { GO_TO_POINT, ROTATE_TO_THETA, STOP };

  void pose_cb(const turtlesim::msg::Pose & pose) {
    if (state_ == State::STOP) {
      stop_robot();
      rclcpp::shutdown();
      return;
    }

    const double x = pose.x;
    const double y = pose.y;
    const double th = pose.theta;

    const double dx = goal_x_ - x;
    const double dy = goal_y_ - y;
    const double dist = std::hypot(dx, dy);

    if (state_ == State::GO_TO_POINT) {
      const double target_heading = std::atan2(dy, dx);
      double ang_err = ang_normalize(target_heading - th);

      double v = k_lin_ * dist;
      double w = k_ang_ * ang_err;

      if (std::abs(ang_err) > 0.6) v *= 0.3; // сильный разворот — приглушим V

      v = std::clamp(v, -max_lin_, max_lin_);
      w = std::clamp(w, -max_ang_, max_ang_);

      if (dist < dist_tol_) {
        state_ = State::ROTATE_TO_THETA;
        RCLCPP_INFO(get_logger(), "Reached position. Rotating to final theta...");
        stop_robot();
        return;
      }

      publish_cmd(v, w);
    }
    else if (state_ == State::ROTATE_TO_THETA) {
      double theta_err = ang_normalize(goal_theta_ - th);
      double w = std::clamp(k_theta_ * theta_err, -max_ang_, max_ang_);
      double v = 0.0;

      if (std::abs(theta_err) < theta_tol_) {
        RCLCPP_INFO(get_logger(), "Goal orientation reached. Stopping.");
        state_ = State::STOP;
        stop_robot();
        rclcpp::shutdown();
        return;
      }
      publish_cmd(v, w);
    }
  }

  void publish_cmd(double v, double w) {
    geometry_msgs::msg::Twist msg;
    msg.linear.x = v;
    msg.angular.z = w;
    cmd_pub_->publish(msg);
  }

  void stop_robot() {
    publish_cmd(0.0, 0.0);
  }

  // целевые значения
  double goal_x_, goal_y_, goal_theta_;
  // гейны и лимиты
  double k_lin_, k_ang_, k_theta_, max_lin_, max_ang_;
  // допуски
  double dist_tol_, theta_tol_;
  // состояние
  State state_ = State::GO_TO_POINT;

  rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_sub_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_pub_;
};

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);

  // Уберём ROS-аргументы и оставим позиционные x y theta
  auto args_no_ros = rclcpp::remove_ros_arguments(argc, argv);
  if (args_no_ros.size() != 4) {
    std::cerr << "Usage:\n"
              << "  ros2 run move_to_goal move_to_goal <x> <y> <theta>\n"
              << "Example:\n"
              << "  ros2 run move_to_goal move_to_goal 5.5 5.5 1.57\n";
    rclcpp::shutdown();
    return 2;
  }

  try {
    const double x = std::stod(args_no_ros[1]);
    const double y = std::stod(args_no_ros[2]);
    const double th = std::stod(args_no_ros[3]);

    auto node = std::make_shared<MoveToGoalNode>(x, y, th);
    rclcpp::spin(node);
  } catch (const std::exception & e) {
    std::cerr << "Failed to parse arguments (x y theta must be numbers): " << e.what() << "\n";
    rclcpp::shutdown();
    return 2;
  }

  rclcpp::shutdown();
  return 0;
}
