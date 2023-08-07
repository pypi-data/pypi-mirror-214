from typing import Union

from .has_coordinates import CoordinatesT, HasCoordinates


def get_coordinates(
    coordinates_like: Union[HasCoordinates[CoordinatesT], CoordinatesT], /
) -> CoordinatesT:
    return (
        coordinates_like._coordinates
        if isinstance(coordinates_like, HasCoordinates)
        else coordinates_like
    )
