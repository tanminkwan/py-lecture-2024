import os
import ffmpeg
import numpy as np
from numpy import dot
from numpy.linalg import norm

"""
2차원 list를 1차원(벡터) list로 변환하는 함수
"""
def flatten(twod: list) -> list:
    return [item for sublist in twod for item in sublist]

"""
2차원 list의 각 item에 특정 숫자(float)를 곱하는 함수
"""
def scale_matrix(twod: list, scalar: float) -> list:
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
다음 조건을 만족하는 `visualize_matrices` 함수를 만들어줘:

### 기능:
- 여러 개의 3×3 크기의 2차원 리스트(ndarray)를 받아서 한 줄에 `num_on_a_row` 개씩 시각화한다.
- 각 그림의 제목(title)에는 자동으로 해당 변수명을 추출하여 표시한다.
- 컬러맵은 `blue → white → green`의 그라디언트를 사용한다.
- 값의 범위는 `vmin=-9`, `vmax=9`로 설정한다.
- 1차원 리스트를 입력받으면, 한 줄짜리 2차원 리스트로 변환하여 출력한다.
- 서브플롯을 활용하여 여러 개의 행렬을 보기 좋게 배치한다.

### 입력 파라미터:
- `ndlist_array`: 3×3 크기의 2차원 리스트를 원소로 가지는 리스트 (리스트의 리스트)
- `vmin`: 색상 스케일의 최소값 (기본값: -9)
- `vmax`: 색상 스케일의 최대값 (기본값: 9)
- `num_on_a_row`: 한 줄에 배치할 그림 개수 (기본값: 1)

### 구현 시 참고 사항:
- `inspect` 모듈을 사용하여 호출자의 프레임에서 변수명을 자동으로 추출한다.
- `matplotlib`을 사용하여 `imshow()`를 활용해 시각화한다.
- 값이 실수(float)일 경우 소수점 두 자리까지 표시하고, 정수(int)일 경우 그대로 표시한다.
- 서브플롯을 생성할 때 빈 공간이 남을 경우 해당 부분의 축을 비활성화한다.
- `tight_layout()`을 사용하여 플롯이 겹치지 않도록 조정한다.

**사용용 예시**:
만약 다음과 같은 변수가 존재한다면:
matrix_a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
matrix_b = [[-3, -2, -1], [0, 1, 2], [3, 4, 5]]
visualize_matrices([matrix_a, matrix_b], num_on_a_row=2)
"""
import inspect
def get_variable_names(value, call_frame):
    """
    주어진 값에 해당하는 변수명을 찾는 함수
    
    Parameters:
    -----------
    value : any
        찾고자 하는 값
    call_frame : frame
        검사할 프레임
    
    Returns:
    --------
    str
        찾은 변수명 또는 기본값
    """
    for var_name, var_val in call_frame.f_locals.items():
        if var_val is value:
            return var_name
    return "Unknown"

def visualize_matrices(ndlist_array, vmin=-9, vmax=9, num_on_a_row=1):
    """
    2차원 리스트들을 시각화하고 각 그림에 자동으로 추출한 변수명을 title로 표시하는 함수
    
    Parameters:
    -----------
    ndlist_array : list of lists
        시각화할 2차원 리스트들의 리스트
    vmin : int, default=-9
        색상 스케일의 최소값
    vmax : int, default=9
        색상 스케일의 최대값
    num_on_a_row : int, default=1
        한 줄에 표시할 그림의 개수
    """
    # 호출자의 프레임 가져오기
    caller_frame = inspect.currentframe().f_back
    
    # 변수명 자동 추출
    var_names = []
    for ndlist in ndlist_array:
        var_name = get_variable_names(ndlist, caller_frame)
        var_names.append(var_name)
    
    # 사용자 정의 색상맵 설정
    cmap = mcolors.LinearSegmentedColormap.from_list(
        'custom_cmap', 
        ['blue', 'white', 'green'], 
        N=19  # -9 to 9 range
    )
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

    # 총 리스트 개수 및 행, 열 계산
    total_items = len(ndlist_array)
    num_rows = (total_items + num_on_a_row - 1) // num_on_a_row

    # 서브플롯 생성
    fig, axes = plt.subplots(num_rows, num_on_a_row, figsize=(5 * num_on_a_row, 3 * num_rows))
    axes = np.array(axes).reshape(-1)  # 1차원 배열로 평탄화

    for idx, (ndlist, var_name) in enumerate(zip(ndlist_array, var_names)):

        # 배열 변환
        # 1차원 리스트를 2차원 리스트로 변환 (한 줄로)
        if isinstance(ndlist[0], list):
            data = np.array(ndlist)  # 이미 2차원 리스트인 경우
        else:
            data = np.array([ndlist])  # 1차원 리스트인 경우, 2차원으로 변환

        # 시각화 처리
        axes[idx].imshow(data, cmap=cmap, norm=norm, interpolation='none')
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                # 값이 정수인 경우와 소수인 경우 다르게 처리
                if isinstance(data[i, j], float):
                    text = f"{data[i, j]:.2f}"  # 소수점 두 자리까지 출력
                else:
                    text = str(data[i, j])  # 정수일 경우 그대로 출력
                axes[idx].text(j, i, text, ha='center', va='center', color='black')  
        # 제목 추가 및 축 제거
        axes[idx].set_title(var_name)
        axes[idx].axis('off')

    # 남아 있는 빈 플롯 제거
    for ax in axes[len(ndlist_array):]:
        ax.axis('off')

    # 그래프 출력
    plt.tight_layout()
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