import cv2
import numpy as np

cap = cv2.VideoCapture(0)

mode = "color"

while True:
    ret, frame = cap.read()

    if not ret:
        print("無法讀取攝影機")
        break

    if mode == "color":
        output = frame
        title = "Color Mode"

    elif mode == "gray":
        output = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        title = "Gray Mode"

    elif mode == "extract":
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 這裡預設抽藍色
        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([130, 255, 255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        output = cv2.bitwise_and(frame, frame, mask=mask)
        title = "Color Extraction Mode"

    elif mode == "edge":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        output = cv2.Canny(gray, 100, 200)
        title = "Canny Edge Mode"

    cv2.imshow("OpenCV Workshop", output)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('1'):
        mode = "color"
        print("切換到：全彩模式")

    elif key == ord('2'):
        mode = "gray"
        print("切換到：灰階模式")

    elif key == ord('3'):
        mode = "extract"
        print("切換到：抽色模式")

    elif key == ord('4'):
        mode = "edge"
        print("切換到：邊緣偵測模式")

    elif key == ord('q'):
        print("結束程式")
        break

cap.release()
cv2.destroyAllWindows()