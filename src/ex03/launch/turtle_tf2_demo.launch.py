from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    delay_arg = DeclareLaunchArgument(
        "delay", default_value="2.0", description="Time delay in seconds for following"
    )

    turtlesim_node = Node(package="turtlesim", executable="turtlesim_node", name="sim")

    broadcaster = Node(
        package="ex03",
        executable="turtle_tf2_broadcaster",
        name="turtle_tf2_broadcaster",
    )

    broadcaster2 = Node(
        package="ex03",
        executable="turtle_tf2_broadcaster2",
        name="turtle_tf2_broadcaster2",
    )

    spawner = Node(package="ex03", executable="spawn_turtle", name="spawn_turtle")

    listener = Node(
        package="ex03",
        executable="turtle_tf2_listener_delay",
        name="turtle_tf2_listener_delay",
        parameters=[{"delay": LaunchConfiguration("delay")}],
    )

    return LaunchDescription(
        [
            delay_arg,
            turtlesim_node,
            broadcaster,
            spawner,
            broadcaster2,
            listener,
        ]
    )
