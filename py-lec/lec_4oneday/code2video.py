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

def read_files_from_directory(directory_path="./downloaded_files"):
    """Read all text files from the specified directory recursively"""
    examples = []
    
    if not os.path.exists(directory_path):
        return [["# No downloaded_files directory found\n# Please create the directory and add example files\nnew_video_array = video_array.copy()"]]
    
    # Supported text file extensions
    text_extensions = ['.py', '.txt', '.md', '.rst', '.sh', '.bat', '.yaml', '.yml', '.json', '.xml', '.html', '.css', '.js', '.sql', '.ini', '.cfg', '.conf']
    
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_name, file_ext = os.path.splitext(file)
                
                # Check if file has a supported text extension
                if file_ext.lower() in text_extensions or file_ext == '':
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Get just the filename for display
                        filename = os.path.basename(file_path)
                        
                        # Add filename as comment and content
                        example_content = f"# {filename}\n{content}"
                        examples.append([example_content])
                        
                    except Exception as e:
                        # If UTF-8 fails, try other encodings
                        try:
                            with open(file_path, 'r', encoding='cp949') as f:
                                content = f.read()
                            filename = os.path.basename(file_path)
                            example_content = f"# {filename}\n{content}"
                            examples.append([example_content])
                        except:
                            # If all encodings fail, add error message
                            filename = os.path.basename(file_path)
                            error_content = f"# {filename}\n# Error: Could not read file (encoding issue)\nnew_video_array = video_array.copy()"
                            examples.append([error_content])
    
    except Exception as e:
        examples = [[f"# Error reading directory: {str(e)}\nnew_video_array = video_array.copy()"]]
    
    # If no files found, return default example
    if not examples:
        examples = [["# No readable files found in downloaded_files directory\n# Add .py, .txt, or other text files to see them here\nnew_video_array = video_array.copy()"]]
    
    return examples

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
            
            # Dynamic examples section
            gr.Markdown("### Example Files from downloaded_files/")
            
            # Create examples component
            examples_component = gr.Examples(
                examples=read_files_from_directory(),
                inputs=[code_input],
                label="Click to load file content"
            )
            

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
    
    # Refresh button
    refresh_btn = gr.Button("🔄 Refresh Examples", variant="secondary")
    
    def refresh_examples():
        """Refresh the examples by reading files again"""
        new_examples = read_files_from_directory()
        return gr.Examples(
            examples=new_examples,
            inputs=[code_input],
            label="Click to load file content"
        )
    
    # Note: Due to Gradio limitations, we need to recreate the interface to refresh examples
    # So we'll provide a message instead
    '''
    def on_refresh_click():
        return "Examples refreshed! Please restart the application to see updated file list."
    
    refresh_btn.click(
        fn=on_refresh_click,
        outputs=[status_output]
    )
    '''
    gr.Markdown("""
    ### Instructions for Examples:
    1. Create a `downloaded_files/` directory in the same location as this script
    2. Add text files (.py, .txt, .md, etc.) with video processing code
    3. Files will be automatically loaded as examples
    4. Subdirectories are supported - all files will be found recursively
    5. Each file's content will be shown with its relative path as a comment
    """)

if __name__ == "__main__":
    demo.launch()