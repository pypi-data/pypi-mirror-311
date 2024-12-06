import gradio as gr
import numpy as np
from gradio_pointcloudeditor import PointCloudEditor

with gr.Blocks() as demo:
    point_size = gr.Slider(
        minimum=0.01, maximum=1.0, value=0.2, step=0.01, label="Point Size"
    )

    with gr.Row():
        up_axis = gr.Dropdown(
            choices=["X", "-X", "Y", "-Y", "Z", "-Z"],
            value="Y",  # Matches the default up_axis="Z" in pce
            label="Up Axis",
            info="Select the up direction"
        )
        forward_axis = gr.Dropdown(
            choices=["X", "-X", "Y", "-Y", "Z", "-Z"],
            value="-Z",  # Matches the default forward_axis="-Y" in pce
            label="Forward Axis",
            info="Select the forward direction"
        )

    with gr.Row():
        lock_scale_x = gr.Checkbox(value=False, label="Lock Scale X")
        lock_scale_y = gr.Checkbox(value=False, label="Lock Scale Y")
        lock_scale_z= gr.Checkbox(value=False, label="Lock Scale Z")

    pce = PointCloudEditor(up_axis="Y", forward_axis="-Z")
    input_textbox = gr.Textbox(
        label="Point Cloud Input",
        placeholder="Enter points as: x,y,z,r,g,b,x,y,z,r,g,b,...",
        interactive=True,
    )
    output_textbox = gr.Textbox(label="Point Cloud Output", interactive=False)

    # Input textbox to PCE connection
    input_textbox.change(fn=lambda x: x, inputs=input_textbox, outputs=pce)

    up_axis.change(fn=lambda x: gr.update(up_axis=x), inputs=up_axis, outputs=pce)
    forward_axis.change(fn=lambda x: gr.update(forward_axis=x), inputs=forward_axis, outputs=pce)

    # Replace the three individual change handlers with a single combined one
    def update_scale_locks(x, y, z):
        return gr.update(lock_scale_x=x, lock_scale_y=y, lock_scale_z=z)

    # Connect all checkboxes to the update function
    locks = [lock_scale_x, lock_scale_y, lock_scale_z]
    for lock in locks:
        lock.change(
            fn=update_scale_locks,
            inputs=locks,
            outputs=pce
        )

    # Point size slider to PCE connection
    point_size.change(
        fn=lambda x: gr.update(point_size=x), inputs=point_size, outputs=pce
    )

    # PCE to output textbox connection
    def format_output(data):
        positions = data["positions"]
        colors = data["colors"]

        if len(positions) != len(colors):
            print("Mismatched positions and colors lengths")
            return ""

        # Format with higher precision
        # Convert positions and colors to flat list alternating between position and color
        full_list = []
        for pos, col in zip(positions, colors):
            full_list.extend([*pos, *col])
        output = ",".join([str(item) for item in full_list])
        return output

    pce.edit(
        fn=format_output,
        inputs=pce,
        outputs=output_textbox,
        show_progress=False,  # Add this to see if it helps with updates
    )

    # Examples
    gr.Examples(
        examples=[
            "0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1",  # Three points with RGB colors
            "0,0,0,1,0,0,0,0.5,1,0.2,1,0.5,0,0,1,0.4,0.2,0.2,",  # Another set of points
            ",".join(
                [str(x) for x in (np.random.rand(6 * 20) * 2 - 1)]
            ),  # Random points
        ],
        inputs=input_textbox,
    )

if __name__ == "__main__":
    demo.launch()
