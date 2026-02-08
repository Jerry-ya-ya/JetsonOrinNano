# 匯入函式庫
import cv2
import numpy as np

# 讀取圖片
img = cv2.imread('ex3-1.png')

# OpenCV 的顏色預設是 BGR 格式，這邊將其轉換為 HSV 格式
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 以 HSV 格式決定要提取的顏色範圍
# 這邊以藍色為示範
lower = np.array([100, 150, 80])
upper = np.array([130, 255, 255])

# 將 HSV 圖像的域值設定為想要提取的顏色
mask = cv2.inRange(hsv, lower, upper)

# 使用 bitwise_and() 來合併和遮罩 (mask) 原來的圖像
img_specific = cv2.bitwise_and(img, img, mask = mask)

# 存檔
cv2.imwrite('ex3-3.png', img_specific)

# 展示原圖
cv2.imshow('img', img)
# 展示遮罩
cv2.imshow('mask', mask)
# 展示抽取顏色後的圖像
cv2.imshow('ex3-3.png', img_specific)

# 等待按鍵
cv2.waitKey(0)
# 關閉所有視窗
cv2.destroyAllWindows()