import ffmpeg
import numpy as np

input_file = './media/SampleVideo_640x360_5mb.mp4'

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

print("video.shape : ",video.shape)
print("video.type : ",type(video))

#import cv2
from PIL import Image
from numpy import dot
from numpy.linalg import norm
import numpy as np

def cos_sim(A, B):
    return dot(A, B) / (norm(A) * norm(B))

# 이전 프레임 설정
prev_frame = None

# 각 프레임별로 처리
for frame_number, frame in enumerate(video):

    #print('frame.shape : ',frame.shape)
    #print('frame : ',frame)
    # 현재 프레임 설정
    # 직렬화, 0-1 사이로, 10의 배수 번째 항목들로만 downsize
    current_vector = ( frame.reshape(-1) / 255 )[::10]
    
    # 10의 배수 번째 항목들로만 downsize
    #current_frame_downsized = current_frame[::10]
    
    # 이전 프레임과 현재 프레임 간의 코사인 유사도 계산
    if prev_frame is not None:
        similarity = cos_sim(prev_vector, current_vector)
        if similarity < 0.9:
            print("Cosine Similarity between current and previous frame: %.9f" % similarity)

            #prev_frame_img = prev_frame.reshape((height, width, 3))
            #current_frame_downsized_img = current_frame_downsized.reshape((height, width, 3))

            # 이미지 저장
            #cv2.imwrite(f"prev_frame_{frame_number}.png", prev_frame)
            Image.fromarray(prev_frame).save(f"prev_frame_{frame_number}.png")
            #cv2.imwrite(f"current_frame_{frame_number}.png", frame)
            Image.fromarray(frame).save(f"current_frame_{frame_number}.png")
            print(f"Saved images for frame {frame_number}")

            """
            # 이미지 출력
            cv2.imshow('Previous Frame', prev_frame_img)
            cv2.imshow('Current Frame (Downsized)', current_frame_downsized_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            """
            
    # 이전 프레임을 현재 프레임으로 업데이트
    prev_frame = frame.copy()
    prev_vector = current_vector