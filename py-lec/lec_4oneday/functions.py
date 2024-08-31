import os
import ffmpeg
import numpy as np
from numpy import dot
from numpy.linalg import norm

"""
2차원 list를 1차원(벡터) list로 변환하는 함수
"""
def two2one(twod: list) -> list:
    oned = []
    for sublist in twod:
        oned.extend(sublist)
    return oned
"""
2차원 list의 각 item에 특정 숫자(float)를 곱하는 함수
"""
def list_mul_scalar(twod: list, scalar: float) -> list:
    return [[x * scalar for x in sublist] for sublist in twod]

"""
prompt : 
===
3X3 list를 argumnet로 받아
matplot을 이용해 
3x3 정사각형 도형을 그려
가운데 숫자를 넣어
-9 ~ -1 은 청색으로 -9가 가장진하게 0은 하얀색  1 ~ 9 는 녹색으로 표시
위를 만족하는 함수 짜줘
"""
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def visualize_ndlist(ndlist, vmin=-9, vmax=9):
    # 1차원 리스트를 2차원 리스트로 변환 (한 줄로)
    if isinstance(ndlist[0], list):
        data = np.array(ndlist)  # 이미 2차원 리스트인 경우
    else:
        data = np.array([ndlist])  # 1차원 리스트인 경우, 2차원으로 변환

    # 사용자 정의 색상맵 설정
    cmap = mcolors.LinearSegmentedColormap.from_list(
        'custom_cmap', 
        ['blue', 'white', 'green'], 
        N=19  # -9 to 9 range
    )

    # 값의 범위를 -9부터 9까지로 설정
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

    # 크기를 1/4로 줄여서 출력
    if isinstance(ndlist[0], list):
        plt.figure(figsize=(2, 2))
    else:
        pass

    # 색상맵을 적용하여 데이터 시각화
    plt.imshow(data, cmap=cmap, norm=norm, interpolation='none')

    # 각 셀에 숫자 넣기
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            # 값이 정수인 경우와 소수인 경우 다르게 처리
            if isinstance(data[i, j], float):
                text = f"{data[i, j]:.2f}"  # 소수점 두 자리까지 출력
            else:
                text = str(data[i, j])  # 정수일 경우 그대로 출력
            plt.text(j, i, text, ha='center', va='center', color='black')

    # 축 숨기기
    plt.axis('off')

    # 그래프 출력
    plt.show()

"""
prompt : 
===
visualize_ndlist code를 활용해
argument 두개를 받고 두개의 그림을 좌우로 배치해줘
"""
def visualize_ndlists_side_by_side(ndlist1, ndlist2):
    # 두 리스트를 넘파이 배열로 변환
    data1 = np.array(ndlist1)
    data2 = np.array(ndlist2)

    # 사용자 정의 색상맵 설정
    cmap = mcolors.LinearSegmentedColormap.from_list(
        'custom_cmap', 
        ['blue', 'white', 'green'], 
        N=19  # -9 to 9 range
    )

    # 값의 범위를 -9부터 9까지로 설정
    norm = mcolors.Normalize(vmin=-9, vmax=9)

    # 두 개의 서브플롯을 생성하여 좌우로 배치
    fig, axes = plt.subplots(1, 2, figsize=(5, 2))

    # 첫 번째 리스트 시각화
    axes[0].imshow(data1, cmap=cmap, norm=norm, interpolation='none')
    for i in range(data1.shape[0]):
        for j in range(data1.shape[1]):
            axes[0].text(j, i, str(data1[i, j]), ha='center', va='center', color='black')
    axes[0].axis('off')

    # 두 번째 리스트 시각화
    axes[1].imshow(data2, cmap=cmap, norm=norm, interpolation='none')
    for i in range(data2.shape[0]):
        for j in range(data2.shape[1]):
            axes[1].text(j, i, str(data2[i, j]), ha='center', va='center', color='black')
    axes[1].axis('off')

    # 그래프 출력
    plt.show()

"""
prompt : 
===
import ffmpeg
import numpy as np
        
def video_2_ndarray(input_file: str)-> tuple: 
    
    #to-do
    
---
위는 
mp4 type의 video file이름을 input_file 으로 받아서 video data를 return
하는 python code야.         
parameters : 
    input_file
    - type : string
return : 
    video data
    - type : numpy ndarray
    - shape : (frame, height, width, RGB)
    - dtype : uint8
    전체 재생시간
    - type : float
    전체 frame 수
    - type : integer

사용할 library : ffmpeg, numpy
사용하면 안되는 library : cv2, moviepy
        
to-do 영역을 완성해줘.
===
응답 모델 : ChatGPT-3.5
"""
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

"""
prompt : 
===
import ffmpeg
import numpy as np
        
def ndarray_2_video(video: np.ndarray, output_file: str)-> None:
    #to-do
---
위는 
numpy array type의 video data(video)를 mp4 type의 video file(output_file)로 변환
하는 python code야.

input parameter : 
    - video : 함수 mp4_2_ndarray 의 return 값
    - output_file : 출력할 video 파일이름
return : 없음

mp4 file을 만들 때 함수 ffmpeg.input 를 사용해.
사용할 library : ffmpeg, numpy
사용하면 안되는 library : cv2, moviepy
사용하면 안되는 function : VideoWriter

to-do 영역을 완성해줘.
===
응답 모델 : ChatGPT-3.5
"""
def ndarray_2_video(video_new: np.ndarray, output_file: str)-> None:

    new_width = video_new.shape[2]
    new_height = video_new.shape[1]

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

def get_simularities_list(video: np.ndarray)->list:

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

        activity_intensity = 1 - group_df[group_df['similarity'] >\
                                min_similarity]['similarity'].mean()**100

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
            'activity_intensity' : activity_intensity,
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
                   capture_dir:str='static')->list:
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