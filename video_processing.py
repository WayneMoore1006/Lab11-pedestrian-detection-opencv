import cv2
import imutils
from imutils.object_detection import non_max_suppression
import numpy as np

# ===============================
# LAB11 video_processing.py
# 功能：
# 1. 讀取影片
# 2. 每一幀縮放為寬度 400
# 3. 使用 HOG + SVM 偵測行人
# 4. 使用 NMS 去除重複框
# 5. 輸出偵測結果影片
# ===============================

video_path = "video/video.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("影片讀取失敗，請確認影片路徑是否正確：", video_path)
    exit()

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = None

frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    # 將每一幀寬度縮放為 400，保持比例
    frame = imutils.resize(frame, width=400)
    output = frame.copy()

    rects, weights = hog.detectMultiScale(
        frame,
        winStride=(4, 4),
        padding=(8, 8),
        scale=1.05
    )

    rects_nms = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects_nms, probs=None, overlapThresh=0.65)

    for (x1, y1, x2, y2) in pick:
        cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

    if out is None:
        h, w = output.shape[:2]
        out = cv2.VideoWriter("video_result.mp4", fourcc, 10.0, (w, h))

    out.write(output)

    print("處理第", frame_count, "幀，偵測到", len(pick), "個行人")

cap.release()

if out is not None:
    out.release()

print("影片行人偵測完成，結果已儲存為 video_result.mp4")
