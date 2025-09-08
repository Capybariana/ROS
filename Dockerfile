FROM osrf/ros:humble-desktop-full

# NVIDIA runtime подсказки (ускоряет авто-дискавери возможностей)
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics

# Часто нужные GUI/X/OpenGL зависимости для RViz2/Gazebo
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Gazebo classic + ROS плагины
    gazebo ros-humble-gazebo-ros-pkgs \
    # X11/OpenGL/GUI runtime deps (страховка для разных хостов)
    libgl1-mesa-glx libglu1-mesa mesa-utils \
    libxext6 libxrender1 libxrandr2 libxi6 libxinerama1 libxcursor1 \
    # dev-инструменты
    bash-completion less vim git \
    python3-colcon-common-extensions ros-dev-tools \
 && rm -rf /var/lib/apt/lists/*

# Рабочее место под ваш overlay workspace
WORKDIR /ws
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc && \
    echo "[ -f /ws/install/setup.bash ] && source /ws/install/setup.bash" >> /root/.bashrc

# Старт — обычный shell
CMD ["/bin/bash"]
