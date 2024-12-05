from enum import Enum
from typing import Union, Optional

import numpy


class Path2D:
    """
    Class storing a 2D path.
    """

    points: list[list[float]]
    x: list[float]
    y: list[float]
    path_length_per_point: list[float]
    length: float
    orientation: list[float]
    unit_tangent_vector: list[list[float]]
    curvature: list[float]

    points_np: numpy.ndarray
    x_np: numpy.ndarray
    y_np: numpy.ndarray
    path_length_per_point_np: numpy.ndarray
    orientation_np: numpy.ndarray
    unit_tangent_vector_np: numpy.ndarray
    curvature_np: numpy.ndarray

    def __init__(
            self,
            points: Union[list[list[float]], numpy.ndarray] = None,
            x: Union[list[float], numpy.ndarray] = None,
            y: Union[list[float], numpy.ndarray] = None
    ):
        """
        A path can be initialized either from a list of points OR separate lists of x and y coordinates.

        :param points: List of points.
        :param x: List of x coordinates.
        :param y: List of y coordinates.
        """
        pass

    def compute_circle_fit_curvature(self, max_rmse: float = 0.15) -> list[float]:
        """
        Computes the curvature by decomposing the path into arc segments.

        :param max_rmse: The maximum RMSE (root mean squared error) that is not exceeded when
                         fitting the arc segments.
        :return: The curvature of the path.
        """
        pass

    def find_circle_segments(self, start: int, end: int, max_rmse: float = 0.15) -> list[tuple[int, int, float]]:
        """
        Decomposes the path into its circle segments,
        such that the maximum RMSE (root mean squared error) is not exceeded.

        :param start: Index of point to start from.
        :param end: Index of point to stop with.
        :param max_rmse: Maximum RMSE.
        :return: The list of arc segments.
        """
        pass

    def resampled_path(
            self,
            resampling_method: ResamplingMethod,
            interpolation_method: InterpolationMethod = InterpolationMethod.Linear,
            epsilon: float = 0.01
    ) -> Path2D:
        """
        Resamples the path equidistantly using the given interpolation method.

        :param resampling_method: Method of resampling.
        :param interpolation_method: Method of interpolation.
        :param epsilon: The distance within two points are considered equal.
        :return: Resampled path.
        """
        pass

    def smoothed_path_elastic_band(
            self,
            max_deviation: float,
            elastic_band_method: ElasticBandMethod = ElasticBandMethod.OrthogonalBounds
    ) -> Path2D:
        """
        Smoothes the path using an algorithm from Autoware [1]. A QP has to be solved for that.
        CLARABEL [2] is used as the solver.

        [1] https://autowarefoundation.github.io/autoware.universe/refs-tags-v1.0/planning/path_smoother/docs/eb/

        [2] https://clarabel.org/stable/

        :param max_deviation: Maximum deviation from the original path.
        :param elastic_band_method: Type of constraining the deviation to the original path.
        :return: The smoothed path.
        """
        pass

    def smoothed_path_chaikin(self, num_iterations: int) -> Path2D:
        """
        Smoothes the path using the Chaikin's path smoothing algorithm.

        :param num_iterations: Number of iterations used for Chaikin's path smoothing algorithm.
        :return: The smoothed path.
        """
        pass

    def index_from_point(self, point: Union[list[float], numpy.ndarray], epsilon: float = 0.01) -> Optional[int]:
        """
        Returns the index of the nearest point on the path in front of the given point.
        If the point outside the path, None is returned.

        :param point: Point of interest.
        :param epsilon: The distance within two points are considered equal.
        :return: The index of the nearest point.
        """
        pass

    def path_length_from_point(
            self,
            point: Union[list[float], numpy.ndarray],
            epsilon: float = 0.01
    ) -> Optional[float]:
        """
        Returns the path length from the first point to the given point.
        If the point outside the path, None is returned.

        :param point: Point of interest.
        :param epsilon: The distance within two points are considered equal.
        :return: The path length.
        """
        pass

    def sub_path(self, start: int = None, end: int = None, epsilon: float = 0.01) -> Path2D:
        """
        Returns the sub path from start to end.
        If start is None, the path begins at the beginning.
        The same holds for end.
        The new path is not necessarily equidistant.

        :param start: Beginning of the sub path.
        :param end: End of the sub path.
        :param epsilon: The distance within two points are considered equal.
        :return: The sub path.
        """
        pass

    def detect_corrupted_point_order(self, sus_angle: float = 2.8) -> list[int]:
        """
        Returns the list of all indices where the path turns sharper than sus_angle.

        :param sus_angle: Every turn sharper than this angle is suspicious.
        :return: Indices of suspicious points.
        """
        pass

    def repair_corrupted_point_order(self, sus_angle: float = 2.8) -> Path2D:
        """
        Repairs corrupted point order by removing points that progress in the wrong direction.

        :param sus_angle: Every turn sharper than this angle is suspicious.
        :return: Repaired path.
        """
        pass

    def add_associated_values(self, values: Union[list[float], numpy.ndarray]) -> int:
        """
        Adds an associated value.

        :param values: The values that should be added as associated to the path.
        :return: The handle for accessing the associated values again.
        """
        pass

    def associated_values(self, handle: int) -> list[float]:
        """
        Returns the respective associated values.

        :param handle: The handle of the associated values.
        :return: The associated values.
        """

    def associated_values_np(self, handle: int) -> numpy.ndarray:
        """
        Returns the respective associated values.

        :param handle: The handle of the associated values.
        :return: The associated values.
        """


class ResamplingMethod(Enum):
    """
    Enum representing resampling method.
    """

    @staticmethod
    def by_number_points(number_points: int) -> ResamplingMethod:
        """
        The path will be equidistantly resampled using the given number of points.

        :param number_points: Number of points.
        """
        pass

    @staticmethod
    def by_sampling_distance(sampling_distance: float, drop_last: bool = True) -> ResamplingMethod:
        """
        The path will be resampled using the given sampling_distance.
        The distance between the last and second last point will differ from sampling distance.

        :param sampling_distance: Sampling distance.
        :param drop_last: Omits the last point when true.
        """
        pass


class InterpolationMethod(Enum):
    """
    Enum representing the interpolation method used for resampling.
    """

    Cubic: InterpolationMethod
    Linear: InterpolationMethod


class ElasticBandMethod(Enum):
    """
    Enum representing the elastic band constraint for the elastic band path smoothing.
    """

    SquareBounds: ElasticBandMethod
    """
    The new points will be constrained to squares around the original points.
    """

    OrthogonalBounds: ElasticBandMethod
    """
    The new points will be constrained to the line which is orthogonal to the original's point orientation. 
    """
