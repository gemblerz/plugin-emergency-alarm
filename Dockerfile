FROM kwelbeck/base-ros2-with-empty-overlay:latest


RUN mkdir -p $ROS_WS/src
WORKDIR $ROS_WS/src
COPY ros-packages .
RUN vcs import < repos
WORKDIR $ROS_WS
SHELL ["/bin/bash", "-c"]
RUN source $ROS_ROOT/setup.bash && colcon build --symlink-install && source $ROS_WS/install/setup.bash

COPY . /app/
WORKDIR /app
ENTRYPOINT ["/app/ros_entrypoint.sh"]
CMD ["python3", "/app/app.py"]