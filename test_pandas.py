import ffmpeg
import numpy as np

input_file = 'SampleVideo_640x360_5mb.mp4'

probe = ffmpeg.probe(input_file)
video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
print(video_info)
width = video_info['width']
height = video_info['height']

tot_duration = float(video_info['duration'])
nb_frames = int(video_info['nb_frames'])


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

from numpy import dot
from numpy.linalg import norm
import numpy as np

def cos_sim(A, B):
    return dot(A, B) / (norm(A) * norm(B))

prev_frame = None

# 결과를 저장할 리스트 생성
results = []

for frame_number, frame in enumerate(video):

    current_vector = ( frame.reshape(-1) / 255 )[::10]
    
    if prev_frame is not None:
        similarity = cos_sim(prev_vector, current_vector)
        results.append({
            'frame_number': frame_number,
            'similarity': similarity
        })

    prev_frame = frame.copy()
    prev_vector = current_vector
    
import pandas as pd

# DataFrame 생성
df = pd.DataFrame(results)
csv = df.to_csv(path_or_buf = "pandas_results.csv", columns=['frame_number', 'similarity'], index=False)

# similarity 값이 0.9 이하인 열을 기준으로 group 분할
groups = []
for group_number, group_df in df.groupby((df['similarity'] < 0.9).cumsum()):
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
        'start' : "{:.2f}".format(start),
        'duration' : "{:.2f}".format(duration),
        #'image': f'<img src="{prev_frame_filename}" width="100"> <img src="{current_frame_filename}" width="100">',
        'min_similarity': min_similarity
    })

# group 정보로 DataFrame 생성
group_df = pd.DataFrame(groups)

# HTML 테이블 생성
#html_table = group_df.to_html(columns=['group_number', 'frame_count', 'start', 'duration', 'min_frame_number', 'max_frame_number', 'min_similarity'], index=False)
# HTML 테이블 출력
#print(html_table)
# csv 생성
csv = group_df.to_csv(path_or_buf = "pandas_cumsum.csv", columns=['group_number', 'frame_count', 'start', 'duration', 'min_frame_number', 'max_frame_number', 'min_similarity'], index=False)

