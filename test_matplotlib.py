import matplotlib.pyplot as plt
from functions import video_2_ndarray, get_simularities_list, divide_takes

file_name = 'SampleVideo_640x360_5mb'
input_file = f'./media/{file_name}.mp4'

np_array, tot_duration, nb_frames = video_2_ndarray(input_file)
results = get_simularities_list(np_array)

# prompt : 
# - matplotlib 를 사용하여 x축 : frame_number, y축: similarity 로 results 를 꺽은선 그래프로 나타내는 code를 작성
# - make code to save the shown graph image

# 꺾은선 그래프 그리기
frame_numbers = [result['frame_number'] for result in results]
similarities = [result['similarity'] for result in results]

plt.figure(figsize=(10, 6))
plt.plot(frame_numbers, similarities, marker='o', linestyle='-', color='b')
plt.xlabel('Frame Number')
plt.ylabel('Similarity')
plt.title('Similarity vs Frame Number')
plt.grid(True)

# 이미지 파일로 저장
plt.savefig(f'similarity_graph_{file_name}.png')

# 그래프 보여주기
plt.show()

cumsum_results = divide_takes(results, tot_duration, nb_frames, similarity=0.9)

# 막대 그래프 그리기
group_numbers = [result['group_number'] for result in cumsum_results]
frame_counts = [result['frame_count'] for result in cumsum_results]

plt.figure(figsize=(10, 6))
plt.bar(group_numbers, frame_counts, color='skyblue')
plt.xlabel('Take #')
plt.ylabel('Tot frames')
plt.title('Frame Count per Take')
plt.xticks(group_numbers)
plt.grid(axis='y')

# 이미지 파일로 저장
plt.savefig(f'takes_graph_{file_name}.png')

# 그래프 보여주기
plt.show()

