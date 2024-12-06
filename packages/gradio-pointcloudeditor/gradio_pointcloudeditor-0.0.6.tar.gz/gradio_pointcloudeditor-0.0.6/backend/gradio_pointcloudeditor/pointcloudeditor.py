from typing import Optional, Dict, List, Union, Literal
import numpy as np
from gradio.components.base import Component
from gradio.events import Events
from gradio.data_classes import GradioModel
from gradio.exceptions import Error

# Add new type for coordinate axes
CoordinateAxis = Literal["X", "Y", "Z", "-X", "-Y", "-Z"]

class PointCloudData(GradioModel):
    positions: List[List[float]]  # [[x, y, z], ...]
    colors: List[List[float]]  # [[r, g, b], ...]

class PointCloudEditor(Component):
    """
    Creates a point cloud editor that allows users to view, edit, and manipulate 3D point cloud data.
    Points are represented as [x, y, z, r, g, b] where colors are in range [0,1].
    """

    EVENTS = [Events.change, Events.edit]
    data_model = PointCloudData

    def __init__(
        self,
        value: Optional[Union[Dict, List, str]] = None,
        *,
        point_size: float = 0.2,
        clear_color: Optional[List[float]] = None,
        label: Optional[str] = None,
        show_label: bool = True,
        up_axis: CoordinateAxis = "Y",
        forward_axis: CoordinateAxis = "Z",
        lock_scale_x: bool = False,
        lock_scale_y: bool = False,
        lock_scale_z: bool = False,
        **kwargs
    ):
        """
        Parameters:
            value: Initial point cloud data in one of these formats:
                  - Dict with 'positions' and 'colors' lists
                  - Flat list [x,y,z,r,g,b,...]
                  - Comma-separated string "x,y,z,r,g,b,..."
            point_size: Size of points in the point cloud (default: 0.2)
            clear_color: Color to clear the background color to (default: None (Gradio default))
            label: Component label
            show_label: If True, show label
            up_axis: The axis to use as "up" direction (default: "Y")
            forward_axis: The axis to use as "forward" direction (default: "Z")
            lock_scale_x: If True, prevents scaling along the x axis
            lock_scale_y: If True, prevents scaling along the y axis
            lock_scale_z: If True, prevents scaling along the z axis
        """
        self.point_size = point_size
        self.clear_color = clear_color
        self.up_axis = up_axis
        self.forward_axis = forward_axis
        self.lock_scale_x = lock_scale_x
        self.lock_scale_y = lock_scale_y
        self.lock_scale_z = lock_scale_z

        # Validate coordinate system
        self._validate_coordinate_system()
        
        # Convert input value to standard format
        if value is not None:
            value = self._standardize_input(value)
        
        super().__init__(value=value, label=label, show_label=show_label, **kwargs)

    def _validate_coordinate_system(self):
        """Validates that the coordinate system axes are valid and orthogonal."""
        # Check that all axes are different
        axes = {self.up_axis.replace('-', ''),  
                self.forward_axis.replace('-', '')}
        if len(axes) != 2:
            raise Error("Coordinate system axes must be different (ignoring signs)")

        # All validations passed
        return True

    def _standardize_input(self, value: Union[Dict, List, str]) -> Dict[str, List[List[float]]]:
        """Converts various input formats to standard dict format"""
        if isinstance(value, str):
            # Convert string to list of floats
            try:
                value = [float(x.strip()) for x in value.split(',')]
            except ValueError:
                return {"positions": [], "colors": []}

        if isinstance(value, (list, np.ndarray)):
            # Convert flat list to numpy array for easier reshaping
            points = np.array(value, dtype=float).reshape(-1, 6)
            return {
                "positions": points[:, :3].tolist(),
                "colors": points[:, 3:].tolist()
            }
        
        # check if value has attrs positions and colors
        if hasattr(value, "positions") and hasattr(value, "colors"):
            return {"positions": value.positions, "colors": value.colors}
        
        if isinstance(value, dict):
            # Validate dict format
            if "positions" in value and "colors" in value:
                return value
            
        return {"positions": [], "colors": []}

    def preprocess(self, payload: GradioModel) -> Dict[str, List[List[float]]]:
        """Convert any input format to standard dict format"""
        return self._standardize_input(payload)

    def postprocess(self, value: Union[Dict, str, List]) -> Dict[str, List[List[float]]]:
        """Ensure output is in standard dict format"""
        return self._standardize_input(value)

    def example_inputs(self) -> Dict[str, List[List[float]]]:
        """Provides example inputs for the component."""
        return {
            "positions": [
                [0, 0, 0],  # Origin
                [1, 0, 0],  # X axis
                [0, 1, 0],  # Y axis
            ],
            "colors": [
                [1, 0, 0],  # Red
                [0, 1, 0],  # Green
                [0, 0, 1]   # Blue
            ]
        }
