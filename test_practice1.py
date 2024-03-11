import ffmpeg
import numpy as np

input_file = 'SampleVideo_640x360_5mb.mp4'
output_file = 'output_'+ input_file


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

# Now you have all frames in the 'frames_array' variable
print("Type of Video :", type(video))
print("Shape of frames array:", video.shape)

half_width = int( width / 2 )
print("half_width :", half_width)

# Now you have all frames in the 'frames_array' variable
print("Type of Video :", type(video))
print("Shape of frames array:", video.shape)


def halver(input: np.ndarray, div_axis: int, concat_axis: int, invers: bool=False) -> tuple:
    
    split_list = np.split(input, 2, axis=div_axis)
    split_tuple = tuple(split_list)
    
    if invers:
        split_tuple = split_tuple[::-1]
    
    output = np.concatenate(split_tuple, axis=concat_axis)

    return output

"""
half_width = int( width / 2 )
print("half_width :", half_width)

video_part1 = video[:, :, :half_width, :]
video_part2 = video[:, :, half_width:, :]

# video_part1 video_part2를 concatenate하여 video_new 생성
video_new = np.concatenate((video_part1, video_part2), axis=1)
"""

video_new = halver(video, 2, 1)

# video_new의 shape 출력
print("Shape of video_new :", video_new.shape)

new_width = video_new.shape[2]
new_height = video_new.shape[1]

print("new_width, new_height :", new_width, new_height)

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

print("Video file created:", output_file)