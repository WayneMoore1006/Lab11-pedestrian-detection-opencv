import cv2
import imutils
from imutils.object_detection import non_max_suppression
import numpy as np

# ===============================
# LAB11 行人偵測 sample.py
# 功能：
# 1. 讀取行人圖片
# 2. 將圖片寬度縮放為 400，並保持等比例
# 3. 使用 HOG + SVM 偵測行人
# 4. 使用 Non-Maximum Suppression 移除重複框
# 5. 用綠色框線框出所有偵測到的行人
# 6. 輸出 sample_result.jpg
# ===============================

# 讀取圖片
# 可以改成 img/input.jpg 或 img/pedestrian.jpg
image_path = "img/input.jpg"
image = cv2.imread(image_path)

# 檢查圖片是否讀取成功
if image is None:
    print("圖片讀取失敗，請確認圖片路徑是否正確：", image_path)
    exit()

print("成功讀取圖片：", image_path)

# 將圖片寬度縮放為 400，保持等比例
image = imutils.resize(image, width=400)

# 複製一份圖片，用來畫偵測框
output = image.copy()

# 建立 HOG 行人偵測器
hog = cv2.HOGDescriptor()

# 使用 OpenCV 內建的預設行人偵測 SVM 分類器
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# 執行行人偵測
rects, weights = hog.detectMultiScale(
    image,
    winStride=(4, 4),
    padding=(8, 8),
    scale=1.05
)

print("原始偵測框數量：", len(rects))

# 將偵測框格式從 x, y, w, h 轉換成 x1, y1, x2, y2
rects_nms = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])

# 使用 NMS 去除重複框
pick = non_max_suppression(rects_nms, probs=None, overlapThresh=0.65)

print("NMS 後行人數量：", len(pick))

# 將行人用綠色框線標示
for (x1, y1, x2, y2) in pick:
    cv2.rectangle(
        output,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        2
    )

# 儲存結果圖片
cv2.imwrite("sample_result.jpg", output)

print("行人偵測完成，結果已儲存為 sample_result.jpg")

