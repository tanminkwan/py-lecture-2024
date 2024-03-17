## 실습.1 - 1. 개요
1. 주요 도구 : ffmpeg, numpy
2. 실습 내용 : 
    - ffmpeg를 사용하여 mp4 type의 video data 추출한다.
    - numpy 를 사용하여 array 형태의 video를 가공한다.
    - array 형태의 video data를 mp4 type으로 저장한다.

3. 사전 준비 :
    - ffmpeg 설치

        [ffmpeg download link](https://www.gyan.dev/ffmpeg/builds/)

        설치 후 <설치 위치>/bin directory를 path 에 등록
    - python library ffmpeg-python, numpy 설치

        `pip install ffmpeg-python numpy`        

4. Video data 구조
    - 4차원 배열 구조
        - frame 별 > pixel 별 > 각 sub pixel들의 값을 표현하는 방법

            4차원 배열로 표시 : (frame 순번, height, width, 0~2(R,G,B))
            height와 width 순서를 바꿔서 표시하기도 함
        - Video data 의 size

            sub pixel은 0~255 사이 자연수이므로 하나의 sub pixel data는 8bit에 저장 가능
            = frame 개수 X height X width X 3 (byte)
        - widthXheight = 640X368, 759 frames 인 video의 배열 형태

            `video.shape = (759, 368, 640, 3)`
## 실습.1 - 2. mp4 파일에서 video data 추출
1. 함수 정의
    - 사용할 library : ffmpeg, numpy
    - 함수 이름 : mp4_2_ndarray
    - input parameter : video 파일이름, 
    - return : numpy array(ndarray)
2. LLM 에 code 요청
    - 모델 선택 : `MIXTRAL` 또는 `SDS-LLAMA2-70B`
    - prompt :

        ```
        import ffmpeg
        import numpy as np
        
        def mp4_2_ndarray(input_file: str)-> np.ndarray: 
            """
            to-do
            """
        ---
        위는 
        mp4 type의 video file이름을 input_file 으로 받아서 numpy array type의 video data를 return
        하는 python code야.         
        parameters : 
        return : numpy ndarray
            - shape : (frame, height, width, RGB)
            - dtype : uint8
        사용할 library : ffmpeg, numpy
        사용하면 안되는 library : cv2, moviepy
        
        to-do 영역을 완성해줘.
        ```
3. 함수 품질 확인
    - LLM이 출력한 함수를 실행
    - Error 여부, output의 정확성 확인

        코드 사례) 사용 모델 : GPT-3.5 Turbo
        ```python
        import ffmpeg
        import numpy as np

        # LLM 이 응답한 code
        def mp4_2_ndarray(input_file: str)-> np.ndarray: 
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
        
        # 함수 test code (직접 작성)
        video = mp4_2_ndarray('./media/SampleVideo_640x360_5mb.mp4')
        print("video.type : ",type(video))     
        print("video.shape : ",video.shape)
        print("video.dtype : ",video.dtype)
        ```
        예상결과)
        ```
        video.type :  <class 'numpy.ndarray'>
        video.shape :  (759, 368, 640, 3)
        video.dtype :  uint8
        ```
    - 오류가 발생하는 경우 원래 LLM에 다시 질의 하거나 LLM 모델을 바꿔 다시 질의 한다.
4. 함수 저장
    - my_functions.py 에 import 구문과 mp4_2_ndarray 함수 추가
    - 함수가 정상 호출되는지 확인

        코드)
        ```python
        # 함수 test code (직접 작성)
        from my_functions import mp4_2_ndarray

        video = mp4_2_ndarray('./media/SampleVideo_640x360_5mb.mp4')
        print("video.type : ",type(video))     
        print("video.shape : ",video.shape)        
        print("video.dtype : ",video.dtype)
        ```
        예상결과)
        ```
        video.type :  <class 'numpy.ndarray'>
        video.shape :  (759, 368, 640, 3)
        video.dtype :  uint8
        ```
## 실습.1 - 3. array 형태의 video data를 mp4 파일로 저장
1. 함수 정의
    - 사용할 library : ffmpeg, numpy
    - 함수 이름 : ndarray_2_mp4
    - input parameter : video data, 출력할 video 파일이름
    - return : 없음
2. LLM 에 code 작성 요청
    - 모델 선택 : `MIXTRAL` 또는 `SDS-LLAMA2-70B`
    - prompt :

        ```
        import ffmpeg
        import numpy as np
        
        def ndarray_2_mp4(video: np.ndarray, output_file: str):
            """
            to-do
            """
        ---
        위는 
        numpy array type의 video data(video)를 mp4 type의 video file(output_file)로 변환
        하는 python code야.
        input parameter : 
            - video : 함수 mp4_2_ndarray 의 return 값
            - output_file : 출력할 video 파일이름
        return : 없음
        to-do 영역을 완성해줘.
        mp4 file을 만들 때 함수 ffmpeg.input 를 사용해.
        사용할 library : ffmpeg, numpy
        사용하면 안되는 library : cv2, moviepy
        사용하면 안되는 function : VideoWriter
        ```
3. 함수 품질 확인
    - LLM이 출력한 함수를 실행
    - Error 여부, output의 정확성 확인

        코드 사례) 사용 모델 : GPT-3.5 Turbo
        ```python
        import ffmpeg
        import numpy as np

        # LLM 이 응답한 code
        def ndarray_2_mp4(video_new: np.ndarray, output_file: str):

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
        
        # 함수 test code (직접 작성)
        video = mp4_2_ndarray('./media/SampleVideo_640x360_5mb.mp4')
        ndarray_2_mp4(video, './media/my_output.mp4')
        ```
        예상결과)
        Error 없음. ./media/my_output.mp4 파일이 생성됨
    - 생성된 mp4 파일을 play 하여 원본 video와 내용이 동일한지 확인한다.
    - 오류가 발생하거나 예상 결과와 다른 경우 원래 LLM에 다시 질의 하거나 LLM 모델을 바꿔 다시 질의 한다.
        
        그래도 문제가 지속되는 경우, 이전 질의/응답 내용을 포함시켜 다시 질의 하거나 더 강력한 code generation 용 LLM(GPT-4.0 등)을 사용한다.
4. 함수 저장
    - my_functions.py 에 ndarray_2_mp4 함수 추가
    - 함수가 정상 호출되는지 확인

        코드)
        ```python
        # 함수 test code (직접 작성)
        from my_functions import mp4_2_ndarray, ndarray_2_mp4

        video = mp4_2_ndarray('./media/SampleVideo_640x360_5mb.mp4')
        ndarray_2_mp4(video, './media/my_output.mp4')     
        ```
        예상결과)
        - Error 없음. 
        - ./media/my_output.mp4 파일이 생성됨
        - ./media/my_output.mp4 play 했을 때 원본과 내용 동일
        