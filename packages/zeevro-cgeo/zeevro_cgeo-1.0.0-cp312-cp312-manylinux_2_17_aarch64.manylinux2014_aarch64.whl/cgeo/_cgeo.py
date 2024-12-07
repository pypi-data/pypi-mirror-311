from __future__ import annotations

from collections.abc import Iterable
from math import atan2, cos, radians, sin, sqrt
import warnings


warnings.warn('Could not import cgeo C extension, Using slow fallback.')

RAD = radians

EARTH_RADIUS = 6378.137  # km


def great_circle_distance(s_lat: float, s_lng: float, d_lat: float, d_lng: float) -> float:
    """Calculate the geodesian (great-circle) distance between two points. Coordinates are given in degrees."""

    s_lat = RAD(s_lat)
    s_lng = RAD(s_lng)
    d_lat = RAD(d_lat)
    d_lng = RAD(d_lng)

    sin_s_lat = sin(s_lat)
    cos_s_lat = cos(s_lat)
    sin_d_lat = sin(d_lat)
    cos_d_lat = cos(d_lat)

    delta_lng = d_lng - s_lng
    sin_delta_lng = sin(delta_lng)
    cos_delta_lng = cos(delta_lng)

    # fmt: off
    return (
        atan2(
            sqrt(
                pow((cos_d_lat * sin_delta_lng), 2) +
                pow((cos_s_lat * sin_d_lat - sin_s_lat * cos_d_lat * cos_delta_lng), 2)
            ),
            sin_s_lat * sin_d_lat + cos_s_lat * cos_d_lat * cos_delta_lng
        )
        * EARTH_RADIUS
    )
    # fmt: on


def point_inside_polygon(x: float, y: float, poly: Iterable[tuple[float, float]]) -> bool:
    """Check whether a point is inside a polygon."""

    poly = list(poly)

    c = False
    for (ix, iy), (jx, jy) in zip(poly, [poly[-1], *poly[:-1]]):
        if ((iy > y) != (jy > y)) and (x < (jx - ix) * (y - iy) / (jy - iy) + ix):
            c = not c
    return c
