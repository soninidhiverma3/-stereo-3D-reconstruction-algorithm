
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load stereo images
I1 = cv2.imread('/content/bikeL.png', 0)  # Load as grayscale
I2 = cv2.imread('/content/bikeR.png', 0)

# Load intrinsic matrices
cam0=([[5299.313, 0, 1263.818], [0, 5299.313 ,977.763],[ 0, 0, 1]])
cam1=([[5299.313, 0, 1438.004],[ 0, 5299.313, 977.763],[ 0, 0, 1]])
K1 = np.array(cam0)
K2 = np.array(cam1)

# Compute Fundamental matrix
F, _ = cv2.findFundamentalMat(K1, K2, cv2.FM_8POINT)

# Compute disparity map
stereo = cv2.StereoBM_create(numDisparities=64, blockSize=15)
disparity = stereo.compute(I1, I2)

# Compute depth map
baseline = 177.288  # Assumed baseline distance between cameras
focal_length = K1[0, 0]  # Assuming the focal length is at (0,0) in the intrinsic matrix
depth_map = np.ones_like(disparity, dtype=float) * baseline * focal_length / disparity

# Generate 3D point cloud
h, w = I1.shape
y, x = np.indices((h, w))
points = np.stack([x, y, depth_map], axis=-1)

# Flatten and reshape the point cloud
point_cloud = points.reshape(-1, 3)

# Visualize results
plt.figure(figsize=(30, 8))

plt.subplot(131)
plt.imshow(disparity, cmap='plasma')
plt.colorbar()
plt.title('Disparity Map')

plt.subplot(132)
plt.imshow(depth_map, cmap='jet', alpha=0.8)
plt.colorbar()
plt.title('Depth Map')

plt.subplot(133)
plt.scatter(points[:, 0], points[:, 1], c=points[:, 2], cmap='prism')
plt.gca().invert_yaxis()
plt.colorbar()
plt.title('3D Point Cloud')

plt.tight_layout()
plt.show()
