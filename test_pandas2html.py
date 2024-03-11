from functions import list_2_html
from functions import video_2_ndarray, get_simularities_list, list_2_html

file_name = 'SampleVideo_640x360_5mb'
input_file = f'./media/{file_name}.mp4'

np_array, tot_duration, nb_frames = video_2_ndarray(input_file)
results = get_simularities_list(np_array)

@list_2_html
def add_image(results):

    takes = []
    for result in results:

        take = result.copy()

        image_name = 'snapshot_'+str(result['max_frame_number'])+'.png'

        take.update(dict(
            start = "{:.2f}".format(result['start']),
            duration = "{:.2f}".format(result['duration']),
            image = f'<img src="/static/{image_name}" width="100">',
        ))
        
        takes.append(take)

    return takes

pandas_html = add_image(results, tot_duration, nb_frames)

print(pandas_html)
