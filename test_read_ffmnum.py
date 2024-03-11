import ffmpeg
import numpy as np

input_file = './media/SampleVideo_640x360_5mb.mp4'

# Get video information
probe = ffmpeg.probe(input_file)
video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')

width = video_info['width']
height = video_info['height']

# Initialize an empty list to store frames
frames = []

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
