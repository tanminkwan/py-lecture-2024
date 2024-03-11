import numpy as np

black_frame = np.zeros((360, 640, 3))
dark_frame = np.full((360, 640, 3), 1, dtype=np.uint8)
dark2_frame = np.full((360, 640, 3), 2, dtype=np.uint8)
white_frame = np.full((360, 640, 3), 255, dtype=np.uint8)
white2_frame = np.full((360, 640, 3), 254, dtype=np.uint8)
red_frame = np.full((360, 640, 3), (255, 0, 0), dtype=np.uint8)
blue_frame = np.full((360, 640, 3), (0, 0, 255), dtype=np.uint8)
noisy_frame1 = np.random.randint(0, 255, size=(360, 640, 3), dtype=np.uint8)
noisy_frame2 = np.random.randint(0, 255, size=(360, 640, 3), dtype=np.uint8)

"""
black_vector = (black_frame.reshape(-1) / 255)[::10]
dark_vector = (dark_frame.reshape(-1) / 255)[::10]
dark2_vector = (dark2_frame.reshape(-1) / 255)[::10]
white_vector = (white_frame.reshape(-1) / 255)[::10]
white2_vector = (white2_frame.reshape(-1) / 255)[::10]
noisy_vector1 = (noisy_frame1.reshape(-1) / 255)[::10]
noisy_vector2 = (noisy_frame2.reshape(-1) / 255)[::10]
"""
black_vector = (black_frame.reshape(-1) / 255)
dark_vector = (dark_frame.reshape(-1) / 255)
dark2_vector = (dark2_frame.reshape(-1) / 255)
white_vector = (white_frame.reshape(-1) / 255)
white2_vector = (white2_frame.reshape(-1) / 255)
red_vector = (red_frame.reshape(-1) / 255)
blue_vector = (blue_frame.reshape(-1) / 255)
noisy_vector1 = (noisy_frame1.reshape(-1) / 255)
noisy_vector2 = (noisy_frame2.reshape(-1) / 255)

print(blue_frame)
print(blue_vector)

#import cv2
from PIL import Image
from numpy import dot
from numpy.linalg import norm

def cos_sim(A, B):
    return dot(A, B) / (norm(A) * norm(B))

print(norm(dark_vector))
print(norm(dark2_vector))
print(dot(dark_vector, dark2_vector))

print(norm(white_vector))
print(norm(white2_vector))
print(dot(white_vector, white2_vector))

print("%.9f" % cos_sim(dark_vector, dark2_vector))
print("%.9f" % cos_sim(white_vector, white2_vector))
print("%.9f" % cos_sim(dark2_vector, white2_vector))
print("%.9f" % cos_sim(red_vector, blue_vector))
print("%.9f" % cos_sim(red_vector, white_vector))
print("%.9f" % cos_sim(noisy_vector1, noisy_vector2))
print("%.9f" % cos_sim(noisy_vector1, noisy_vector1))
