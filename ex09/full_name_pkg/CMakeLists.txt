cmake_minimum_required(VERSION 3.8)
project(full_name_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

# Генерация сообщений и сервиса
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/FullNameMessage.msg"
  "srv/FullNameSumService.srv"
)

# Проверка тестов
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # пропускаем проверку авторских прав
  set(ament_cmake_copyright_FOUND TRUE)
  # пропускаем cpplint (только для git)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
