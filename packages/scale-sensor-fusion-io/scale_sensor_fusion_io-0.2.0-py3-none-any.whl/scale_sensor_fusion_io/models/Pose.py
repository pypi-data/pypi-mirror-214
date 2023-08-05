from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

import numpy as np
import numpy.typing as npt
from pyquaternion import Quaternion as PyQuaternion
from scipy.spatial.transform import Rotation as R

@dataclass
class Point3D:
    x: float
    y: float
    z: float


@dataclass
class Quaternion:
    x: float
    y: float
    z: float
    w: float

class IPose(Protocol):
    position: Point3D
    heading: Quaternion


@dataclass
class Pose:
    """
    A data class representing a Pose in a 3D space. The pose includes both position and orientation.

    Attributes:
        position: A Point3D object representing the position in 3D space.
        heading: A Quaternion object representing the orientation in the 3D space.
    """
    position: Point3D
    heading: Quaternion

    @classmethod
    def to_transform(cls, pose: IPose) -> npt.NDArray:
        """
        Creates a homogeneous transformation matrix from a Pose.

        Args:
            pose: An object of type IPose from which to create the transformation matrix.

        Returns:
            A 4x4 NumPy ndarray representing the homogeneous transformation matrix.
        """
        transform_matrix = np.eye(4)
        transform_matrix[:3, :3] = PyQuaternion(**pose.heading.__dict__).rotation_matrix
        transform_matrix[:3, 3] = [
            pose.position.x,
            pose.position.y,
            pose.position.z,
        ]
        return transform_matrix

    @classmethod
    def from_transform(cls, transform_matrix: npt.NDArray) -> Pose:
        """
        Creates a Pose from a homogeneous transformation matrix.

        Args:
            transform_matrix: A 4x4 NumPy ndarray representing the homogeneous transformation matrix.

        Returns:
            A Pose object corresponding to the provided transformation matrix.
        """
        quaternion = PyQuaternion(matrix=transform_matrix[:3, :3])
        return Pose(
            position=Point3D(**{k: v for k, v in zip("xyz", transform_matrix[:3, 3])}),
            heading=Quaternion(
                x=quaternion.x, y=quaternion.y, z=quaternion.z, w=quaternion.w
            ),
        )

    @classmethod
    def from_pose_like(cls, pose_like: IPose) -> Pose:
        """
        Creates a Pose from another object of type IPose.

        Args:
            pose_like: An object of type IPose from which to create a Pose.

        Returns:
            A Pose object with the same attributes as the provided IPose object.
        """
        return Pose(position=pose_like.position, heading=pose_like.heading)

    @classmethod
    def from_rt(cls, rotation: R, translation: Iterable[float]) -> Pose:  # type: ignore[no-any-unimported]
        """
        Creates a Pose from a Rotation and a translation vector.

        Args:
            rotation: A scipy Rotation object representing the orientation.
            translation: An iterable of floats representing the translation vector in 3D space.

        Returns:
            A Pose object with the specified rotation and translation.
        """
        return Pose(
            position=Point3D(*translation),
            heading=Quaternion(**{k: v for k, v in zip("xyzw", rotation.as_quat())}),
        )


@dataclass
class GPSPose:
    lat: float
    lon: float
    bearing: float
