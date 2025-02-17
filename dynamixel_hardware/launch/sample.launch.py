#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('dynamixel_hardware')
    urdf_file = os.path.join(pkg_share, 'urdf', 'sample.urdf')
    controller_yaml = os.path.join(pkg_share, 'config', 'sample_controller.yaml')

    with open(urdf_file, 'r') as infp:
        robot_description = infp.read()

    return LaunchDescription([
        Node(package='robot_state_publisher',
             executable='robot_state_publisher',
             output='both',
             parameters=[{
                 'robot_description': robot_description
             }]),
        Node(package='controller_manager',
             executable='ros2_control_node',
             output='screen',
             parameters=[{
                 'robot_description': robot_description
             }, controller_yaml]),
        Node(package='controller_manager',
             executable='spawner',
             arguments=['joint_state_broadcaster'],
             output='screen'),
        Node(package='controller_manager',
             executable='spawner',
             arguments=['head_trajectory_controller'],
             output='screen'),
    ])


if __name__ == '__main__':
    generate_launch_description()
