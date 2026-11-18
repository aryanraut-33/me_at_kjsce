import cv2
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# 1. Load Image
# -------------------------------
img = cv2.imread("road.png")  # replace with your filename
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# -------------------------------
# 2. Preprocessing (FULL IMAGE)
# -------------------------------
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# Contrast enhancement
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
gray = clahe.apply(gray)

# Noise reduction
blur = cv2.GaussianBlur(gray, (5,5), 0)

# 👉 NO ROI — use full image
roi = blur

# -------------------------------
# 3. Sobel
# -------------------------------
sobelx = cv2.Sobel(roi, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(roi, cv2.CV_64F, 0, 1, ksize=3)
sobel = cv2.magnitude(sobelx, sobely)

# -------------------------------
# 4. Prewitt
# -------------------------------
kernelx = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
kernely = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])

prewittx = cv2.filter2D(roi, -1, kernelx)
prewitty = cv2.filter2D(roi, -1, kernely)
prewitt = cv2.magnitude(prewittx.astype(float), prewitty.astype(float))

# -------------------------------
# 5. Canny Edge Detection
# -------------------------------
canny = cv2.Canny(roi, 100, 200)

# -------------------------------
# 6. Hough Transform
# -------------------------------
hough_img = img.copy()
lines = cv2.HoughLinesP(
    canny,
    rho=1,
    theta=np.pi/180,
    threshold=200,
    minLineLength=100,
    maxLineGap=50
)

if lines is not None:
    for x1, y1, x2, y2 in lines[:,0]:
        cv2.line(hough_img, (x1,y1), (x2,y2), (255,0,0), 2)



# -------------------------------
# 7. Plot Results
# -------------------------------
plt.figure(figsize=(14,10))

titles = [
    "Original Image",
    "Preprocessed (Full Image)",
    "Sobel (Too Many Gradients)",
    "Prewitt (Noisy Edges)",
    "Canny (Edges Only)",
    "Hough (Many Lines incl. Noise)"
]

images = [
    img,
    roi,
    sobel,
    prewitt,
    canny,
    hough_img
]

for i in range(6):
    plt.subplot(3,2,i+1)
    if len(images[i].shape) == 2:
        plt.imshow(images[i], cmap='gray')
    else:
        plt.imshow(images[i])
    plt.title(titles[i])
    plt.axis('off')

plt.tight_layout()
plt.show()