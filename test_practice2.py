import ffmpeg
import numpy as np

input_file = 'SampleVideo_640x360_5mb.mp4'

def get_ndarray(input_file: str)-> np.ndarray: 
    # Get video information
    probe = ffmpeg.probe(input_file)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')

    width = video_info['width']
    height = video_info['height']

    # Define ffmpeg input
    out, err = (
        ffmpeg
        .input(input_file)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run(capture_stdout=True)
    )

    video = (
        np
        .frombuffer(out, np.uint8)
        .reshape([-1, height, width, 3])
    )

    return video

def create_output(video_new: np.ndarray, input_file: str):

    new_width = video_new.shape[2]
    new_height = video_new.shape[1]

    # Path to output video file
    output_file = 'output_' + input_file

    # Define ffmpeg output
    ffmpeg_output = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt='rgb24', s=f'{new_width}x{new_height}')
        .output(output_file, pix_fmt='yuv420p', vcodec='libx264', r=30)
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )

    # Send frames to ffmpeg
    for frame in video_new:
        ffmpeg_output.stdin.write(
            frame
            .astype(np.uint8)
            .tobytes()
        )

    ffmpeg_output.stdin.close()
    ffmpeg_output.wait()

def halver(input: np.ndarray, div_axis: int, concat_axis: int, invers: bool=False) -> tuple:
    
    split_list = np.split(input, 2, axis=div_axis)
    split_tuple = tuple(split_list)
    
    if invers:
        split_tuple = split_tuple[::-1]
    
    output = np.concatenate(split_tuple, axis=concat_axis)

    return output

video_array     = get_ndarray(input_file)
new_video_array = halver(video_array, 2, 1)
create_output(new_video_array, input_file)