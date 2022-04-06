# System Architecture


## System Diagram
![alternative text](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.github.com/dlezcan1/ros2_needle_insertion_experiment/main/docs/system_diagram.txt)

## ROS 2 Messages

|Component    |Topic                            |Message  Type                        |Description                                                                                                                                                                                   |Coordinate Frame|
|------------|----------------------------------|-------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
|System      |/subject/state/target             |geometry_msgs/msg/Point              |The target point in the subject; defined on intraoperative images.                                                                                                                            |Stage           |
|Compensation|/needle/state/skin_entry          |geometry_msgs/msg/Point              |The needle entry point on the skin in the needle coordinate frame                                                                                                                             |Needle          |
|            |/needle/cmd/pose                  |geometry_msgs/msg/Pose               |The desired needle pose in the needle coordinate frame. In this implementation, the pose is defined only by the needle insertion length (Z) and the rotation about the Z-axis.                |Needle          |
|            |/stage/cmd/pose                   |geometry_msgs/msg/Pose               |The desired stage pose in the stage coordinate frame. In this implementation, the pose is defined only by x- and y- translations. (ztranslation and rotations are zero).                      |Stage           |
|            |/needle/compensation/delta        |geometry_msgs/msg/Pose               |The desired shift of the stage to compensate for the current deviation. In this implementation, the shift is defined only by x- and ytranslations.                                            |Needle          |
|Shape model |/needle/state/predicted_shape     |geometry_msgs/msg/PoseArray          |The predicted needle shape as an array of positions and directions (i.e., poses) of needle sections (0.5-mm increment). **Not Implemented**                                                   |Stage           |
|            |/needle/state/current_shape       |geometry_msgs/msg/PoseArray          |The estimated needle shape as an array of positions and directions (i.e., poses) of needle sections (0.5-mm increment).                                                                       |Stage           |
|            |/needle/sensor/raw                |std_msgs/msg/Float64MultiArray       |Raw FBG sensor data                                                                                                                                                                           |Needle          |
|            |/needle/sensor/processed          |std_msgs/msg/Float64MultiArray       |Processed FBG sensor data                                                                                                                                                                     |Needle          |
|            |/needle/state/curvatures          |std_msgs/msg/Float64MultiArray       |Curvatures measured from each of the active areas.                                                                                                                                            |Needle          |
|Stage       |/stage/state/needle_pose          |geometry_msgs/msg/PoseStamped        |The needle pose in the stage coordinate frame. In this implementation, the pose is defined by x- and z- positions, the needle insertion depth (y) and the rotation about the y-axis.          |Stage           |
|            |/stage/state/axis/x               |std_msgs/msg/Float32                 |The current position of the X-axis linear stage of the robot.                                                                                                                                 |Robot           |
|            |/stage/state/axis/y               |std_msgs/msg/Float32                 |The current position of the Y-axis linear stage of the robot.                                                                                                                                 |Robot           |
|            |/stage/state/axis/z               |std_msgs/msg/Float32                 |The current position of the Z-axis linear stage of the robot.                                                                                                                                 |Robot           |
|            |/stage/state/axis/linear_stage    |std_msgs/msg/Float32                 |The current position of the appended X-axis linear stage of the robot.                                                                                                                        |Robot           |
|            |/stage/state/command/x            |std_msgs/msg/Float32                 |Command of the position for the X-axis linear stage of the robot.                                                                                                                             |Robot           |
|            |/stage/state/command/y            |std_msgs/msg/Float32                 |Command of the position for the Y-axis linear stage of the robot.                                                                                                                             |Robot           |
|            |/stage/state/command/z            |std_msgs/msg/Float32                 |Command of the position for the Z-axis linear stage of the robot.                                                                                                                             |Robot           |
|            |/stage/state/command/linear_stage |std_msgs/msg/Float32                 |Command of the position for the appended X-axis linear stage of the robot.                                                                                                                    |Robot           |

## Coordinate Systems

| Frame  | X-Axis                           | Y-Axis                                      | Z-Axis                         | Positive Directions (X,Y,Z)                      |
|--------|----------------------------------|---------------------------------------------|--------------------------------|--------------------------------------------------|
| Needle | Orthonormal to Y-Z axes          | In upwards direction of the bevel-tip       | Along Needle's axis            | (Left from bevel, Up from bevel, forward/insert) |
| Robot  | Along needle's axis              | Along horizontal insertion plane            | Along vertical insertion plane | (forward/insert, left, up)                       |
| Stage  | Along horizontal insertion plane | Along needle's axis                         | Along vertical insertion plane | (right, forward/insert, up) *Need to check*      |
