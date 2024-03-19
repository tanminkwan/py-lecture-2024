import ffmpeg
import numpy as np

input_file = './media/SampleVideo_640x360_5mb_old.mp4'

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

def create_output(video_new: np.ndarray, output_file: str):

    new_width = video_new.shape[2]
    new_height = video_new.shape[1]

    # Define ffmpeg output
    ffmpeg_output = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt='rgb24', s=f'{new_width}x{new_height}')
        .output(output_file, pix_fmt='yuv420p', vcodec='libx264', r=20)
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

def modi_video(func):
    def wrapper(input_file, output_file):
        video = get_ndarray(input_file)
        result = func(video)
        create_output(result, output_file)
        return result
    return wrapper    

def halver(input: np.ndarray, div_axis: int, concat_axis: int, invers: bool=False) -> tuple:
    
    split_list = np.split(input, 2, axis=div_axis)
    split_tuple = tuple(split_list)
    
    if invers:
        split_tuple = split_tuple[::-1]
    
    output = np.concatenate(split_tuple, axis=concat_axis)

    return output

@modi_video
def practice1(video):
    return halver(video, 2, 1)

@modi_video
def practice2(video):

    new_video = video.copy()
    # R(빨간색) 값과 B(파란색) 값 바꾸기
    new_video[:, :, :, 0], new_video[:, :, :, 1] = video[:, :, :, 2], video[:, :, :, 0]

    return new_video

@modi_video
def practice3(video):

    new_video = video.copy()
    # RGB 값 바꾸기: 255 - 원래 값
    new_video = 255 - video

    return new_video

@modi_video
def practice4(video):

    new_video = video.copy()
    # width와 height 차원 바꾸기
    new_video = np.moveaxis(new_video, 1, 2)

    return new_video

@modi_video
def practice5(video):

    new_video = video.copy()
    # RGB 값 바꾸기: 255 - 원래 값
    new_video = new_video[150:]

    return new_video

practice5(input_file, 'test.mp4')
#video = get_ndarray(input_file)
#ndarray_2_video(video, 'test.mp4')