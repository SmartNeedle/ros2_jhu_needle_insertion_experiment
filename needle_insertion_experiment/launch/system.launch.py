from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.substitutions import FindPackageShare
import launch_yaml

pkg_system_integration     = FindPackageShare( 'needle_insertion_experiment' )
pkg_needle_shape_publisher = FindPackageShare( 'needle_shape_publisher' )
pkg_insertion_robot        = FindPackageShare( 'needle_insertion_robot' )
pkg_insertion_point        = FindPackageShare( 'insertion_point_publisher' )
pkg_stereo_camera          = FindPackageShare( 'pkg_stereo_camera' )

def generate_launch_description():
    ld = LaunchDescription()

    # arguments
    # - needle args
    arg_needle_sim = DeclareLaunchArgument(
        'sim_level_needle_sensing',
        default_value='1',
        description="Simulation level: 1 - demo needle sensors, 2 - real needle sensors."
        )

    arg_needle_numsignals = DeclareLaunchArgument(
        'needle_numSignals',
        default_value='200',
        description='Needle: The number of signals to gather per FBG window.'
        )

    arg_needle_optim_maxiter = DeclareLaunchArgument(
        'needle_optimMaxIterations',
        default_value="15",
        description="Needle: The maximum number of iterations for needle shape optimizer."
        )

    arg_needle_paramFile = DeclareLaunchArgument(
        'needle_needleParamFile',
        default_value="needle_params_2021-08-16_Jig-Calibration_best.json",
        description="Needle: JSON parameter file for FBG Needle"
    )

    # - interrogator
    arg_interrogator_ip = DeclareLaunchArgument(
        'interrogator_ipAddress',
        default_value="192.168.1.11",
        description="Interrogator: IP address of FBG interrogator"
    )

    # - robot
    arg_robot_ip = DeclareLaunchArgument(
        'robot_ipAddress',
        default_value="192.168.1.201",
        description="Robot: IP Address of Galil Controller"
    )
    arg_robot_ns = DeclareLaunchArgument(
        'robot_ns',
        default_value='stage',
        description="Robot: ROS Namespace for needle insertion robot"
    )

    # - camera
    arg_camera_ns = DeclareLaunchArgument(
        'camera_ns',
        default_value='camera',
        description="Camera: ROS namespace for stereo camera setup"
    )
    arg_camera_sync = DeclareLaunchArgument(
        'camera_syncStereo',
        default_value='true', 
        choices=['true', 'false'],
        description="Camera: Whether to publish synchronized stereo iamge pairs"
    )
    arg_camera_imgproc = DeclareLaunchArgument(
        'camera_useImageProc',
        default_value='true',
        choices=['true', 'false'],
        description="Camera: Whether to use image processing ROS publishing for image rectification or not."
    )


    # launch files
    # - needle shape-sensing
    launch_needle = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                pkg_system_integration, 'launch', 'needle.launch.py'
            ])
        ),
        launch_arguments={
            'sim_level_needle_sensing': LaunchConfiguration( 'sim_level_needle_sensing' ),
            'needleParamFile'         : LaunchConfiguration( 'needle_needleParamFile' ),
            'numSignals'              : LaunchConfiguration( 'needle_numSignals' ),
            'optimMaxIterations'      : LaunchConfiguration( 'needle_optimMaxIterations' ),
            'interrogatorIP'          : LaunchConfiguration( 'interrogator_ipAddress' ),
        }.items(),
    )

    # - needle insertion robot
    launch_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                pkg_system_integration, 'launch', 'stage.launch.py'
            ])
        ),
        launch_arguments={
            'ip': LaunchConfiguration('robot_ipAddress'),
            'ns': LaunchConfiguration('robot_ns'),
        }.items(),
    )

    # - needle insertion publisher
    launch_insertionpoint = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    pkg_insertion_point, 'launch', 'insertion_point_publisher.launch.py'
                ])
            ),
            launch_arguments={
                'ns': 'needle',
            }.items(),
            )

    launch_stereocamera = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                pkg_stereo_camera, 'launch', 'stereo_camera.launch.py'
            ]),
            launch_arguments={
                'ns'          : LaunchConfiguration('camera_ns'),
                'syncStereo'  : LaunchConfiguration('camera_syncStereo'),
                'useImageProc': LaunchConfiguration('camera_useImageProc'),
            }.items(),
        )
    )

    # launch description setup
    # - arguments
    ld.add_action( arg_needle_sim )
    ld.add_action( arg_needle_numsignals )
    ld.add_action( arg_needle_optim_maxiter )
    ld.add_action( arg_needle_paramFile )

    ld.add_action( arg_interrogator_ip )

    ld.add_action( arg_robot_ip )
    ld.add_action( arg_robot_ns )

    ld.add_action( arg_camera_ns )
    ld.add_action( arg_camera_sync )
    ld.add_action( arg_camera_imgproc )

    # - launch files
    ld.add_action( launch_needle )
    ld.add_action( launch_robot )
    ld.add_action( launch_insertionpoint )
    ld.add_action( launch_stereocamera )


    return ld

# generate_launch_description
