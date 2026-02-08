# 匯入函式庫
import cv2
import numpy as np

# 讀取圖像
img = cv2.imread('ex3-1.png')

# 將圖片轉換為灰階
img_gray =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# 存檔
cv2.imwrite('ex3-2.png', img_gray)

# 開啟視窗顯示圖像
cv2.imshow('ex3-2',img_gray)

# 不刷新圖像
cv2.waitKey(0)

# 釋放資源
cv2.destroyAllWindows()

# 執行後終端出現
# Gtk-Message: 22:14:10.599: Failed to load module "canberra-gtk-module"
# 不影響計算結果可以忽略