import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

URDF = "{{cookiecutter.robot_name}}.xacro"
PACKAGE = "{{cookiecutter.package_name}}"


def generate_launch_description():
    ld = LaunchDescription()

    pkg = get_package_share_directory(PACKAGE)

    robot_description_path = os.path.join(pkg, "urdf", URDF)
    doc = xacro.parse(inp=None, filename=robot_description_path)
    xacro.process_doc(doc)

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": doc.toxml()}],
    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
    )

    rviz_node = Node(
            package='rviz2',
            namespace='',
            executable='rviz2',
            name='rviz2'
            #arguments=['-d' + os.path.join(pkg, 'config', 'rviz.rviz')]
        )

    ld.add_action(robot_state_publisher)
    ld.add_action(joint_state_publisher_node)
    ld.add_action(rviz_node)
    return ld
