from typing import Any, Dict

from super_scad.d3.private.PrivateCube import PrivateCube
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget


class Cube(ScadWidget):
    """
    Widget for creating cubes. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#cube.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: float,
                 center: bool = False):
        """
        Object constructor.

        :param size: The size of the cube.
        :param center: Whether the cube is centered at the origin.
        """
        ScadWidget.__init__(self)

        self._size: float = size
        """
        The size of the cube.
        """

        self._center: bool = center
        """
        Whether the cube is centered at the origin.
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
        validator.validate_required({'size'}, {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the cube is centered at the origin.
        """
        return self._center

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size(self) -> float:
        """
        Returns the size of the cube.
        """
        return self._size

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivateCube(size=self.size, center=self.center)

# ----------------------------------------------------------------------------------------------------------------------
