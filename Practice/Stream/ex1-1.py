# OpenCV 與攝影機串流

# 匯入 OpenCV 套件
# cv2 是 OpenCV 在 Python 中的名稱
import cv2

# 開啟預設攝影機
# 0 代表電腦的第一個攝影機
cap = cv2.VideoCapture(0)

# 建立無限迴圈
# 讓攝影機畫面可以持續更新，直到使用者手動離開
while True:
    # 從攝影機讀取一張畫面
    # ret:
    #   是否成功讀取(True / False)
    # frame:
    #   攝影機目前拍到的影像(frame)
    ret, frame = cap.read()
    
    # 顯示影像視窗
    # "Camera" 是視窗名稱
    # frame 是要顯示的畫面
    cv2.imshow("Camera", frame)

    # waitKey(1)
    # 等待鍵盤輸入 1 毫秒
    # ord('q')
    # 將字母 q 轉成 ASCII 數值
    # 如果按下 q 鍵
    # 就離開 while 迴圈
    if cv2.waitKey(1) == ord('q'):
        break

# 釋放攝影機資源
# 告訴電腦攝影機已經使用完畢
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()