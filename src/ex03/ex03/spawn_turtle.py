import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
import time


class TurtleSpawner(Node):
    def __init__(self):
        super().__init__("spawn_turtle")
        self.cli = self.create_client(Spawn, "spawn")

        # Ждём, пока сервис появится
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for spawn service...")

        # Дадим turtlesim время полностью запуститься
        time.sleep(2.0)

        self.req = Spawn.Request()
        self.req.x = 5.0
        self.req.y = 1.0
        self.req.name = "turtle2"

        self.future = self.cli.call_async(self.req)
        self.future.add_done_callback(self.done_callback)

    def done_callback(self, future):
        try:
            result = future.result()
            self.get_logger().info(f"Spawned {result.name}")
        except Exception as e:
            self.get_logger().error(f"Failed to spawn: {e}")


def main():
    rclpy.init()
    node = TurtleSpawner()
    rclpy.spin(node)
    rclpy.shutdown()
