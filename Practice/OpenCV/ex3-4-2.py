# 匯入函式庫
import cv2
import numpy as np

# 讀取圖像
img_gray = cv2.imread('ex3-2.png')
img_specific = cv2.imread('ex3-3.png')

# 將提取顏色的圖像轉換為灰階
img_specific_gray = cv2.cvtColor(img_specific, cv2.COLOR_BGR2GRAY)

# 下方數字 50 為域值，可修改域值範圍 (0 ~ 255) 來調整遮罩區域，並轉換為二元圖像
ret, mask = cv2.threshold(img_specific_gray, 50, 255, cv2.THRESH_BINARY)

# 將遮罩反向
mask_inv = cv2.bitwise_not(mask)

# 使用 bitwise_and() 和遮罩從灰階圖中排除已被提取顏色的區域
img_gray_bg = cv2.bitwise_and(img_gray, img_gray, mask = mask_inv)
# 使用 bitwise_and() 和遮罩設定提取顏色的區域
img_specific_fg = cv2.bitwise_and(img_specific, img_specific, mask = mask)

# 使用 add() 將兩張照片疊加
img_result = cv2.add(img_gray_bg, img_specific_fg)

# 透過 PutText() 在 OpenCV 視窗加入文字內容 
cv2.putText(img_result, 'Blue', (100, 200), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 7, cv2.LINE_AA)

# 存檔並展示結果
cv2.imwrite('ex3-4-2.png', img_result)
cv2.imshow('ex3-4-2', img_result)
cv2.waitKey(0)
cv2.destroyAllWindows()