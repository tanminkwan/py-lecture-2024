import os
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

def ndarray_2_video(video_new: np.ndarray, output_file: str)-> None:

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

def _cos_sim(A, B):
    return dot(A, B) / (norm(A) * norm(B))

def get_simularities_list(video: np.ndarray)->list[dict]:

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

def capture_frames_4_each_group(video: np.ndarray, simularity_groups: list, target_dir: str)->dict:

    # 각 group 별 처음과 끝 frame을 image capture
    min_frame_list = [ g['min_frame_number'] for g in simularity_groups ]
    max_frame_list = [ g['max_frame_number'] for g in simularity_groups ]
    frames_list = min_frame_list + max_frame_list

    capture_map = {x: f'{target_dir}/capture_{str(x)}.png' for x in frames_list}

    from PIL import Image

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    for frame_number in frames_list:
        Image.fromarray(video[frame_number]).save(capture_map[frame_number])

    return capture_map

def analyze_video(input_file:str, lower_similarity_limit:float=0.9,
                   capture_dir:str='static')->list[dict]:
    # mp4파일의 video를 ndarray 형식으로 변환
    v_array, tot_duration, nb_frames = video_2_ndarray(input_file)

    # frame별로 이전 frame과의 유사성을 구하여 list를 return
    simularities_list = get_simularities_list(v_array)

    # 유사도 limit 기준으로 frame들을 분할
    simularity_groups = divide_takes(simularities_list, tot_duration, nb_frames,\
                                          lower_similarity_limit)
    
    # 각 group 별 처음과 끝 frame을 image capture
    capture_map = capture_frames_4_each_group(v_array, simularity_groups,\
                                              target_dir=capture_dir)
    _captures_added = [ {**s, 
            'min_frame_path':capture_map[s['min_frame_number']],
            'max_frame_path':capture_map[s['max_frame_number']]                        
            } for s in simularity_groups ]

    return _captures_added