import numpy as np
from nptyping import NDArray, Shape, Float
from typing import NewType

RotationMatrix = NewType("RotationMatrix", NDArray[Shape["2, 2"], Float])
def rotation_matrix(angle: Float) -> RotationMatrix:
    """Returns a 2D rotation matrix for the given angle."""
    return RotationMatrix(np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ]))

def pretty_print_rotation_matrix(mat: RotationMatrix):
    a = np.arccos(mat[0, 0])
    b = np.arcsin(mat[0, 1])
    c = np.arcsin(mat[1, 0])
    d = np.arccos(mat[1, 1])
    print(f"|cos({a:.3f}) -sin({b:.3f})|")
    print(f"|sin({c:.3f}) cos({d:.3f})|")


def angle_from_rotation_matrix(mat: RotationMatrix) -> Float:
    """Returns the angle of the given rotation matrix."""
    return np.arctan2(mat[1, 0], mat[0, 0])

TranslationMatrix = NewType("TranslationMatrix", NDArray[Shape["3, 3"], Float])
def translation_matrix(x: Float, y: Float) -> TranslationMatrix:
    """Returns a 2D translation matrix for the given position."""
    return TranslationMatrix(np.array([
        [1.0, 0.0, x],
        [0.0, 1.0, y],
        [0.0, 0.0, 1.0]
    ]))

def pretty_print_translation_matrix(mat: TranslationMatrix):
    print(f"|1.0   0.0   {mat[0, 2]:.3f}|")
    print(f"|0.0   1.0   {mat[1, 2]:.3f}|")
    print(f"|0.0   0.0   1.0|")

def length_from_translation_matrix(mat: TranslationMatrix) -> Float:
    """Returns the length of the given translation matrix."""
    return mat[0, 2]

TransformationMatrix = NewType("TransformationMatrix", NDArray[Shape["3, 3"], Float])
def transformation_matrix(x: Float, y: Float, angle: Float) -> TransformationMatrix:
    """
    Returns a 2D transformation matrix for the given position and angle.
    This is equivalent to a translation matrix followed by a rotation matrix.
    """
    return TransformationMatrix(np.array([
        [np.cos(angle), -np.sin(angle), x],
        [np.sin(angle), np.cos(angle), y],
        [0.0, 0.0, 1.0]
    ]))

def pretty_print_transformation_matrix(mat: TransformationMatrix):
    a = np.arccos(mat[0, 0])
    b = np.arcsin(mat[0, 1])
    c = np.arcsin(mat[1, 0])
    d = np.arccos(mat[1, 1])
    print(f"|cos({a:.3f})   -sin({b:.3f})   {mat[0, 2]:.3f}|")
    print(f"|sin({c:.3f})   cos({d:.3f})    {mat[1, 2]:.3f}|")
    print(f"|0.0            0.0             1.0            |")

def angle_from_transformation_matrix(mat: TransformationMatrix) -> Float:
    """Returns the angle of the given transformation matrix."""
    return np.arctan2(mat[1, 0], mat[0, 0])

def position_from_transformation_matrix(mat: TransformationMatrix) -> NDArray[Shape["2"], Float]:
    """Returns the position of the given transformation matrix."""
    return np.array([mat[0, 2], mat[1, 2]])