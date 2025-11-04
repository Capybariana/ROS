#include "rclcpp/rclcpp.hpp"
#include "service_full_name/srv/summ_full_name.hpp"
#include <memory>

using SummFullName = service_full_name::srv::SummFullName;
using std::placeholders::_1;
using std::placeholders::_2;

class ServiceName : public rclcpp::Node
{
public:
  ServiceName() : Node("service_name")
  {
    service_ = this->create_service<SummFullName>(
      "SummFullName", std::bind(&ServiceName::handle_service, this, _1, _2));
    RCLCPP_INFO(this->get_logger(), "Service SummFullName ready!");
  }

private:
  void handle_service(const std::shared_ptr<SummFullName::Request> request,
                      std::shared_ptr<SummFullName::Response> response)
  {
    response->full_name = request->last_name + " " + request->name + " " + request->first_name;
    RCLCPP_INFO(this->get_logger(), "Request: %s %s %s",
                request->last_name.c_str(),
                request->name.c_str(),
                request->first_name.c_str());
    RCLCPP_INFO(this->get_logger(), "Response: %s", response->full_name.c_str());
  }

  rclcpp::Service<SummFullName>::SharedPtr service_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ServiceName>());
  rclcpp::shutdown();
  return 0;
}
