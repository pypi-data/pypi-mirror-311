from gradio.components.base import Component


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
        
        super().__init__(value=value, **kwargs)

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

    
    def change(self,
        fn: Callable | None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        outputs: Component | Sequence[Component] | None = None,
        api_name: str | None | Literal[False] = None,
        scroll_to_output: bool = False,
        show_progress: Literal["full", "minimal", "hidden"] = "full",
        queue: bool | None = None,
        batch: bool = False,
        max_batch_size: int = 4,
        preprocess: bool = True,
        postprocess: bool = True,
        cancels: dict[str, Any] | list[dict[str, Any]] | None = None,
        every: float | None = None,
        trigger_mode: Literal["once", "multiple", "always_last"] | None = None,
        js: str | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        show_api: bool = True) -> Dependency:
        """
        Parameters:
            fn: the function to call when this event is triggered. Often a machine learning model's prediction function. Each parameter of the function corresponds to one input component, and the function should return a single value or a tuple of values, with each element in the tuple corresponding to one output component.
            inputs: List of gradio.components to use as inputs. If the function takes no inputs, this should be an empty list.
            outputs: List of gradio.components to use as outputs. If the function returns no outputs, this should be an empty list.
            api_name: Defines how the endpoint appears in the API docs. Can be a string, None, or False. If False, the endpoint will not be exposed in the api docs. If set to None, the endpoint will be exposed in the api docs as an unnamed endpoint, although this behavior will be changed in Gradio 4.0. If set to a string, the endpoint will be exposed in the api docs with the given name.
            scroll_to_output: If True, will scroll to output component on completion
            show_progress: If True, will show progress animation while pending
            queue: If True, will place the request on the queue, if the queue has been enabled. If False, will not put this event on the queue, even if the queue has been enabled. If None, will use the queue setting of the gradio app.
            batch: If True, then the function should process a batch of inputs, meaning that it should accept a list of input values for each parameter. The lists should be of equal length (and be up to length `max_batch_size`). The function is then *required* to return a tuple of lists (even if there is only 1 output component), with each list in the tuple corresponding to one output component.
            max_batch_size: Maximum number of inputs to batch together if this is called from the queue (only relevant if batch=True)
            preprocess: If False, will not run preprocessing of component data before running 'fn' (e.g. leaving it as a base64 string if this method is called with the `Image` component).
            postprocess: If False, will not run postprocessing of component data before returning 'fn' output to the browser.
            cancels: A list of other events to cancel when this listener is triggered. For example, setting cancels=[click_event] will cancel the click_event, where click_event is the return value of another components .click method. Functions that have not yet run (or generators that are iterating) will be cancelled, but functions that are currently running will be allowed to finish.
            every: Run this event 'every' number of seconds while the client connection is open. Interpreted in seconds.
            trigger_mode: If "once" (default for all events except `.change()`) would not allow any submissions while an event is pending. If set to "multiple", unlimited submissions are allowed while pending, and "always_last" (default for `.change()` and `.key_up()` events) would allow a second submission after the pending event is complete.
            js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
            concurrency_limit: If set, this is the maximum number of this event that can be running simultaneously. Can be set to None to mean no concurrency_limit (any number of this event can be running simultaneously). Set to "default" to use the default concurrency limit (defined by the `default_concurrency_limit` parameter in `Blocks.queue()`, which itself is 1 by default).
            concurrency_id: If set, this is the id of the concurrency group. Events with the same concurrency_id will be limited by the lowest set concurrency_limit.
            show_api: whether to show this event in the "view API" page of the Gradio app, or in the ".view_api()" method of the Gradio clients. Unlike setting api_name to False, setting show_api to False will still allow downstream apps as well as the Clients to use this event. If fn is None, show_api will automatically be set to False.
        """
        ...
    
    def edit(self,
        fn: Callable | None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        outputs: Component | Sequence[Component] | None = None,
        api_name: str | None | Literal[False] = None,
        scroll_to_output: bool = False,
        show_progress: Literal["full", "minimal", "hidden"] = "full",
        queue: bool | None = None,
        batch: bool = False,
        max_batch_size: int = 4,
        preprocess: bool = True,
        postprocess: bool = True,
        cancels: dict[str, Any] | list[dict[str, Any]] | None = None,
        every: float | None = None,
        trigger_mode: Literal["once", "multiple", "always_last"] | None = None,
        js: str | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        show_api: bool = True) -> Dependency:
        """
        Parameters:
            fn: the function to call when this event is triggered. Often a machine learning model's prediction function. Each parameter of the function corresponds to one input component, and the function should return a single value or a tuple of values, with each element in the tuple corresponding to one output component.
            inputs: List of gradio.components to use as inputs. If the function takes no inputs, this should be an empty list.
            outputs: List of gradio.components to use as outputs. If the function returns no outputs, this should be an empty list.
            api_name: Defines how the endpoint appears in the API docs. Can be a string, None, or False. If False, the endpoint will not be exposed in the api docs. If set to None, the endpoint will be exposed in the api docs as an unnamed endpoint, although this behavior will be changed in Gradio 4.0. If set to a string, the endpoint will be exposed in the api docs with the given name.
            scroll_to_output: If True, will scroll to output component on completion
            show_progress: If True, will show progress animation while pending
            queue: If True, will place the request on the queue, if the queue has been enabled. If False, will not put this event on the queue, even if the queue has been enabled. If None, will use the queue setting of the gradio app.
            batch: If True, then the function should process a batch of inputs, meaning that it should accept a list of input values for each parameter. The lists should be of equal length (and be up to length `max_batch_size`). The function is then *required* to return a tuple of lists (even if there is only 1 output component), with each list in the tuple corresponding to one output component.
            max_batch_size: Maximum number of inputs to batch together if this is called from the queue (only relevant if batch=True)
            preprocess: If False, will not run preprocessing of component data before running 'fn' (e.g. leaving it as a base64 string if this method is called with the `Image` component).
            postprocess: If False, will not run postprocessing of component data before returning 'fn' output to the browser.
            cancels: A list of other events to cancel when this listener is triggered. For example, setting cancels=[click_event] will cancel the click_event, where click_event is the return value of another components .click method. Functions that have not yet run (or generators that are iterating) will be cancelled, but functions that are currently running will be allowed to finish.
            every: Run this event 'every' number of seconds while the client connection is open. Interpreted in seconds.
            trigger_mode: If "once" (default for all events except `.change()`) would not allow any submissions while an event is pending. If set to "multiple", unlimited submissions are allowed while pending, and "always_last" (default for `.change()` and `.key_up()` events) would allow a second submission after the pending event is complete.
            js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
            concurrency_limit: If set, this is the maximum number of this event that can be running simultaneously. Can be set to None to mean no concurrency_limit (any number of this event can be running simultaneously). Set to "default" to use the default concurrency limit (defined by the `default_concurrency_limit` parameter in `Blocks.queue()`, which itself is 1 by default).
            concurrency_id: If set, this is the id of the concurrency group. Events with the same concurrency_id will be limited by the lowest set concurrency_limit.
            show_api: whether to show this event in the "view API" page of the Gradio app, or in the ".view_api()" method of the Gradio clients. Unlike setting api_name to False, setting show_api to False will still allow downstream apps as well as the Clients to use this event. If fn is None, show_api will automatically be set to False.
        """
        ...
