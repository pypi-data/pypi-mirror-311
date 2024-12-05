from typing import Any, Dict

from super_scad.d3.private.PrivateCube import PrivateCube
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Vector3 import Vector3


class Cuboid(ScadWidget):
    """
    Class for cuboids.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: Vector3 | None = None,
                 width: float | None = None,
                 depth: float | None = None,
                 height: float | None = None,
                 center: bool = False):
        """
        Object constructor.

        :param size: The size of the cuboid.
        :param width: The width (the size along the x-axis) of the cuboid.
        :param depth: The depth (the size along the y-axis) of the cuboid.
        :param height: The height (the size along the y-axis) of the cuboid.
        :param center: Whether the cuboid is centered at the origin.
        """
        ScadWidget.__init__(self)

        self._size: Vector3 | None = size
        """
        The size of the cuboid.
        """

        self._width: float | None = width
        """
        The width (the size along the x-axis) of the cuboid.
        """

        self._depth: float | None = depth
        """
        The depth (the size along the y-axis) of the cuboid.
        """

        self._height: float | None = height
        """
        The height (the size along the y-axis) of the cuboid.
        """

        self._center: bool = center
        """
        Whether the cuboid is centered at the origin.
        """

        self.__validate_arguments(locals())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __validate_arguments(args: Dict[str, Any]) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.

        :param args: The arguments supplied to the constructor.
        """
        validator = ArgumentValidator(args)
        validator.validate_exclusive({'size'}, {'width', 'depth', 'height'})
        validator.validate_required({'size', 'width'},
                                    {'size', 'depth'},
                                    {'size', 'height'},
                                    {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the cuboid is centered at the origin.
        """
        return self._center

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size(self) -> Vector3:
        """
        Returns the size of the cuboid.
        """
        if self._size is None:
            self._size = Vector3(x=self.width, y=self.depth, z=self.height)

        return self._size

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def width(self) -> float:
        """
        Returns the width of the cuboid.
        """
        if self._width is None:
            self._width = self._size.x

        return self._width

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def depth(self) -> float:
        """
        Returns the depth of the cuboid.
        """
        if self._depth is None:
            self._depth = self._size.y

        return self._depth

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height of the cuboid.
        """
        if self._height is None:
            self._height = self._size.z

        return self._height

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivateCube(size=self.size, center=self.center)

# ----------------------------------------------------------------------------------------------------------------------
