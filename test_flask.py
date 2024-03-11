import os
from flask import Flask
import pandas as pd
from functions import video_2_ndarray, get_simularities_list, list_2_html

app = Flask(import_name=__name__, 
            static_url_path='/static',
            static_folder="./tmp"
            )

@list_2_html
def analize_video(simularity_groups):
    """
    params : 
        - results : 
    """
    takes = []
    for group in simularity_groups:

        take = group.copy()

        priv_frame_number = group['min_frame_number']-1 if group['min_frame_number']>1 else 1
        first_frame_number = group['min_frame_number']
        
        image_name1 = 'snapshot_'+str(priv_frame_number)+'.png'
        image_name2 = 'snapshot_'+str(first_frame_number)+'.png'

        take.update(dict(
            start = "{:.2f}".format(group['start']),
            duration = "{:.2f}".format(group['duration']),
            image1 = f'<img src="/static/{image_name1}" width="150">',
            image2 = f'<img src="/static/{image_name2}" width="150">',
        ))
        
        takes.append(take)

    return takes

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/video_list')
def video_list():

    # 디렉토리 경로
    directory = './media'

    # 디렉토리 내의 모든 파일 목록 가져오기
    files = os.listdir(directory)

    # mp4 파일 이름만 추출 (확장자 제외)
    video_list = [file.rsplit('.', 1)[0] for file in files if file.endswith('.mp4')]

    df = pd.DataFrame({'Video Name': video_list})

    # Modify the column to include links
    df['Video Name'] = df['Video Name'].apply(lambda x: f'<a href="/report/{x}">{x}</a>')

    # Creating the HTML table
    pandas_html = df.to_html(index=False, escape=False)

    return pandas_html

@app.route('/report/<file_name>')
def report(file_name):

    input_file = f'./media/{file_name}.mp4'

    pandas_html = analize_video(input_file)

    return pandas_html

# run command
# flask --app test_flask run --debug
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)