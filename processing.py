import cv2
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--image", help="path to the image", default="img/Lenna.png")
args = parser.parse_args()

path = args.image

# 1. 讀取圖像
image = cv2.imread(path)

if image is None:
    print("圖片讀取失敗，請確認路徑是否正確：", path)
    exit()

print("成功讀取圖片：", path)

# 2. 儲存原始圖片
cv2.imwrite("./img/original.jpg", image)
print("已儲存 ./img/original.jpg")

# 3. 縮放圖片為 400 x 400
resized = cv2.resize(image, (400, 400))
cv2.imwrite("./img/resized.jpg", resized)
print("已儲存 ./img/resized.jpg")

# 4. ROI 擷取
x1, y1, x2, y2 = 100, 120, 300, 360
roi = resized[y1:y2, x1:x2]
cv2.imwrite("./img/roi.jpg", roi)
print("已儲存 ./img/roi.jpg")

# 5. 畫矩形框
rectangle_img = resized.copy()
cv2.rectangle(rectangle_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
cv2.imwrite("./img/rectangle.jpg", rectangle_img)
print("已儲存 ./img/rectangle.jpg")

# 6. 灰階處理
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
cv2.imwrite("./img/gray.jpg", gray)
print("已儲存 ./img/gray.jpg")

# 7. CLAHE 影像增強
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
clahe_img = clahe.apply(gray)
cv2.imwrite("./img/clahe.jpg", clahe_img)
print("已儲存 ./img/clahe.jpg")

print("圖像基本操作完成")
