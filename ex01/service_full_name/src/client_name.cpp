#include "rclcpp/rclcpp.hpp"
#include "service_full_name/srv/summ_full_name.hpp"
#include <chrono>
#include <cstdlib>
#include <memory>

using SummFullName = service_full_name::srv::SummFullName;
using namespace std::chrono_literals;

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);

  if (argc != 4) {
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"),
                "Usage: ros2 run service_full_name client_name <last_name> <name> <first_name>");
    return 1;
  }

  auto node = rclcpp::Node::make_shared("client_name");
  auto client = node->create_client<SummFullName>("SummFullName");

  while (!client->wait_for_service(1s)) {
    if (!rclcpp::ok()) {
      RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Interrupted while waiting for service. Exiting.");
      return 0;
    }
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Waiting for SummFullName service...");
  }

  auto request = std::make_shared<SummFullName::Request>();
  request->last_name = argv[1];
  request->name = argv[2];
  request->first_name = argv[3];

  auto result = client->async_send_request(request);

  // Wait for the result
  if (rclcpp::spin_until_future_complete(node, result) == rclcpp::FutureReturnCode::SUCCESS) {
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Full name: %s", result.get()->full_name.c_str());
  } else {
    RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Failed to call service SummFullName");
  }

  rclcpp::shutdown();
  return 0;
}
