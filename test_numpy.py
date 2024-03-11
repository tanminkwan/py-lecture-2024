import numpy as np

# 주어진 ndarray a 생성 (임의의 값으로 채워넣음)
a = np.random.randint(0, 255, size=(10, 72, 128, 3), dtype=np.uint8)

# a의 shape 출력
print("Shape of a:", a.shape)

# b와 c로 나누기
b = a[:, :, :64, :]
c = a[:, :, 64:, :]

# b와 c의 shape 출력
print("Shape of b:", b.shape)
print("Shape of c:", c.shape)

# b와 c를 concatenate하여 d 생성
d = np.concatenate((b, c), axis=1)

# d의 shape 출력
print("Shape of d:", d.shape)

e = np.split(a, 2, axis=2)

print(e[0].shape)
print(e[1].shape)