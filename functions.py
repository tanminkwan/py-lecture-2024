import ffmpeg
import numpy as np
from numpy import dot
from numpy.linalg import norm

def video_2_ndarray(input_file: str)-> tuple: 
    # Get video information
    probe = ffmpeg.probe(input_file)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')

    width = video_info['width']
    height = video_info['height']

    tot_duration = float(video_info['duration'])
    nb_frames = int(video_info['nb_frames'])

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

    return video, tot_duration, nb_frames

def ndarray_2_video(video_new: np.ndarray, output_file: str):

    new_width = video_new.shape[2]
    new_height = video_new.shape[1]

    # Path to output video file
    #output_file = 'output_' + input_file

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

def modi_video(func):
    def wrapper(input_file, output_file):
        video, _, _ = video_2_ndarray(input_file)
        result = func(video)
        ndarray_2_video(result, output_file)
        return result
    return wrapper

def _cos_sim(A, B):
    return dot(A, B) / (norm(A) * norm(B))

def get_simularities_list(video: np.ndarray):

    results = []
    prev_frame = None

    for frame_number, frame in enumerate(video):

        current_vector = ( frame.reshape(-1) / 255 )[::10]
        
        if prev_frame is not None:
            similarity = _cos_sim(prev_vector, current_vector)
            results.append({
                'frame_number': frame_number,
                'similarity': similarity
            })

        prev_frame = frame.copy()
        prev_vector = current_vector
    
    return results

import pandas as pd

def divide_takes(results: list, tot_duration: float, nb_frames: int, similarity: float=0.9)-> list:
    # DataFrame 생성
    df = pd.DataFrame(results)
    
    # prompt :  
    # similarity 값이 0.9 이하인 열을 기준으로 group을 분할하고 분할된 group 별로
    # group 순번, min(frame_number), max(frame_number), mix(similarity) 4개 칼럼을 return출력한다
    groups = []
    for group_number, group_df in df.groupby((df['similarity'] <= similarity).cumsum()):
        min_frame_number = group_df['frame_number'].min()
        max_frame_number = group_df['frame_number'].max()
        min_similarity = group_df['similarity'].min()

        frame_count = max_frame_number - min_frame_number + 1
        start = tot_duration*(min_frame_number/nb_frames)
        duration = tot_duration*(frame_count/nb_frames)

        groups.append({
            'group_number': group_number,
            'min_frame_number': min_frame_number,
            'max_frame_number': max_frame_number,
            'frame_count' : frame_count,
            'start' : start,
            'duration' : duration,
            'min_similarity': min_similarity
        })

    return groups

def list_2_html(func):

    def wrapper(input_file):

        # mp4파일의 video를 ndarray 형식으로 변환
        v_array, tot_duration, nb_frames = video_2_ndarray(input_file)
        
        # frame별로 이전 frame과의 유사성을 구하여 list를 return
        simularities_list = get_simularities_list(v_array)

        # 유사도가 0.9 이하인 지점을 기준으로 분할하여 frame들을 grouping
        simularity_groups = divide_takes(simularities_list, tot_duration, nb_frames)

        # 각 group 별 처음과 끝 frame을 image capture
        min_frame_list = [ g['min_frame_number'] for g in simularity_groups ]
        max_frame_list = [ g['max_frame_number'] for g in simularity_groups ]
        frames_list = min_frame_list + max_frame_list

        _capture_frames(v_array, frames_list)

        # 유사도 기준 grouping list를 func 에 의해 가공
        new_simularity_groups = func(simularity_groups)

        # func 에 의해 가공된 list로 dataframe 생성 후 html 형식으로 출력
        df = pd.DataFrame(new_simularity_groups)
        html_table = df.to_html(index=False, escape=False)
        
        return html_table
    
    return wrapper

from PIL import Image

def _capture_frames(video: np.ndarray, frames_list: list):

    for frame_number in frames_list:
        Image.fromarray(video[frame_number]).save(f'./tmp/snapshot_{frame_number}.png')
        
    return True