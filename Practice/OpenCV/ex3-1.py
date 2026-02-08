# 匯入 OpenCV 函式庫
import cv2

# 設定從哪顆鏡頭讀取圖像，在括弧中填入先前查詢到的 webcam 編號
webcam = cv2.VideoCapture(0)

# 讀取圖像
return_value, image = webcam.read()

# 儲存名為 ex3-1.png 的照片
cv2.imwrite("ex3-1.png", image)

# 刪除webcam避免圖像佔用資源
del(webcam)