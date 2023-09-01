from dataclasses import dataclass, field
from typing import List, Union
import numpy as np
from nptyping import NDArray, Shape, Float
from src.matrix_math import *

class Joint:
    """
    A rotational joint represented by a rotation matrix.
    """
    def __init__(self, radians: Float) -> None:
        self.__mat = rotation_matrix(radians)

    @property
    def angle(self) -> Float:
        return angle_from_rotation_matrix(self.__mat)

    @angle.setter
    def angle(self, radians: Float) -> None:
        self.__mat = rotation_matrix(radians)

    @property
    def matrix(self) -> RotationMatrix:
        return self.__mat

class Link:
    """
    A static link between two points represented by a translation matrix.
    """
    def __init__(self, length: Float) -> None:
        self.__mat = translation_matrix(length, 0.0)

    @property
    def length(self) -> Float:
        return length_from_translation_matrix(self.__mat)

    @length.setter
    def length(self, length: Float) -> None:
        self.__mat = translation_matrix(length, 0.0)

    @property
    def matrix(self) -> TranslationMatrix:
        return self.__mat


@dataclass
class Robot2D:
    """
    A robot is a configuration of successive joints and links.
    """
    origin: NDArray[Shape["2"], Float] = np.array([0.0, 0.0])
    configuration: List[Union[Joint, Link]] = field(default_factory=list)
    def __len__(self) -> int:
        """Returns the number of joints in the robot."""
        return len([j for j in self.configuration if isinstance(j, Joint)])

@dataclass
class Pose:
    """
    The position and orientation of a point in 2D space.
    """
    position: NDArray[Shape["2"], Float]
    orientation: Float
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, other: 'Pose'):
        return str(self) == str(other)

def forward_kinematics(robot: Robot2D, joint_index: int) -> Pose:
    """Returns the pose of the joint at the given index."""
    if joint_index == 0:
        return Pose(robot.origin, 0.0)
    
    """
    Calculate the transformation matrix Tₒ,ₑₑ from the origin (o) to the end-effector (ee).
    Start with identity matrix of size 3, i.e [[1,0,0],[0,1,0],[0,0,1]], then sum the matrices of each transformation
    """
    transformFromOriginToEE = np.identity(3) 
    for i in range(joint_index):
        transformFromOriginToEE = transformFromOriginToEE @ robot.configuration[i].matrix
    angleFromOriginToEE = angle_from_transformation_matrix(TransformationMatrix(transformFromOriginToEE))
    translationFromOriginToEE = position_from_transformation_matrix(TransformationMatrix(transformFromOriginToEE))
    return Pose(translationFromOriginToEE, angleFromOriginToEE)

def ee_forward_kinematics(robot: Robot2D) -> Pose:
    """Returns the pose of the end-effector of the robot."""
    ee_index = len(robot.configuration)
    return forward_kinematics(robot, ee_index)