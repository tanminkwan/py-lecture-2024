import gradio as gr
import numpy as np
import os
import traceback
from functions import video_2_ndarray, ndarray_2_video

# Global video array that stays resident
video_array = None

def initialize_video():
    """Initialize the global video array from the sample video"""
    global video_array
    try:
        video_array, _, _ = video_2_ndarray('../media/SampleVideo_640x360_5mb.mp4')
        return f"Video initialized successfully. Shape: {video_array.shape}"
    except Exception as e:
        return f"Error initializing video: {str(e)}"

def process_video_code(code):
    """Process the input code and generate new video"""
    global video_array
    
    if video_array is None:
        return None, "Error: Video not initialized. Please restart the application."
    
    try:
        # Clear any existing output files
        if os.path.exists('new_video.mp4'):
            os.remove('new_video.mp4')
        
        # Create local namespace with necessary variables
        local_vars = {
            'video_array': video_array,
            'np': np,
            'ndarray_2_video': ndarray_2_video
        }
        
        # Execute the user code
        exec(code, globals(), local_vars)
        
        # Check if new_video_array was created
        if 'new_video_array' not in local_vars:
            return None, "Error: Code must create a variable named 'new_video_array'"
        
        new_video_array = local_vars['new_video_array']
        
        # Generate the output video
        ndarray_2_video(new_video_array, 'new_video.mp4')
        
        if os.path.exists('new_video.mp4'):
            return 'new_video.mp4', "Video processed successfully!"
        else:
            return None, "Error: Failed to generate output video file"
            
    except Exception as e:
        error_message = f"Error processing video:\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        return None, error_message

def clear_outputs():
    """Clear previous outputs when new code is entered"""
    if os.path.exists('new_video.mp4'):
        try:
            os.remove('new_video.mp4')
        except:
            pass
    return None, ""

# Sample code for the interface
sample_code = """# Sample code: Split video horizontally and stack vertically
width_half = video_array.shape[2] // 2
left_array = video_array[:, :, :width_half, :]
right_array = video_array[:, :, width_half:, :]
new_video_array = np.append(left_array, right_array, axis=1)"""

# Initialize video on startup
init_message = initialize_video()

# Create Gradio interface
with gr.Blocks(title="Video Processor") as demo:
    gr.Markdown("# Video Processing Tool")
    gr.Markdown(f"**Initialization Status:** {init_message}")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Input Code")
            gr.Markdown("Write Python code to process `video_array`. Results must be stored in `new_video_array`.")
            
            code_input = gr.Code(
                value=sample_code,
                language="python",
                label="Video Processing Code",
                lines=15
            )
            
            process_btn = gr.Button("Process Video", variant="primary")
            
        with gr.Column(scale=1):
            gr.Markdown("### Output")
            
            video_output = gr.Video(
                label="Processed Video",
                width=640,
                height=700
            )
    
            status_output = gr.Textbox(
                label="Status",
                lines=5,
                max_lines=10
            )
            
    # Event handlers
    def on_code_change():
        return clear_outputs()
    
    def on_process_click(code):
        return process_video_code(code)
    
    # Connect events
    code_input.change(
        fn=on_code_change,
        outputs=[video_output, status_output]
    )
    
    process_btn.click(
        fn=on_process_click,
        inputs=[code_input],
        outputs=[video_output, status_output]
    )
    
    # Add some example codes
    gr.Markdown("### Example Codes")
    
    examples = [
        ["# Flip video horizontally\nnew_video_array = np.flip(video_array, axis=2)"],
        ["# Flip video vertically\nnew_video_array = np.flip(video_array, axis=1)"],
        ["# Rotate video 180 degrees\nnew_video_array = np.rot90(video_array, k=2, axes=(1, 2))"],
        ["# Extract first half of frames\nnew_video_array = video_array[:len(video_array)//2]"],
        ["# Crop center 50% of video\nh, w = video_array.shape[1], video_array.shape[2]\nstart_h, start_w = h//4, w//4\nend_h, end_w = start_h + h//2, start_w + w//2\nnew_video_array = video_array[:, start_h:end_h, start_w:end_w, :]"]
    ]
    
    gr.Examples(
        examples=examples,
        inputs=[code_input],
        label="Click to load example"
    )

if __name__ == "__main__":
    demo.launch()