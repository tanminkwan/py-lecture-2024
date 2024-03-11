import ffmpeg
import numpy as np

# Generate some example frames (replace this with your own frames)
height, width = 360, 640
num_frames = 50
frames_array = np.random.randint(0, 255, size=(num_frames, height, width, 3), dtype=np.uint8)

# Path to output video file
output_file = './media/noisy_output.mp4'

# Define ffmpeg output
ffmpeg_output = (
    ffmpeg
    .input('pipe:', format='rawvideo', pix_fmt='rgb24', s=f'{width}x{height}')
    .output(output_file, pix_fmt='yuv420p', vcodec='libx264', r=30)
    .overwrite_output()
    .run_async(pipe_stdin=True)
)

# Send frames to ffmpeg
for frame in frames_array:
    ffmpeg_output.stdin.write(
        frame
        .astype(np.uint8)
        .tobytes()
    )

ffmpeg_output.stdin.close()
ffmpeg_output.wait()

print("Video file created:", output_file)
