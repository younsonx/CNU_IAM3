import cv2
import numpy as np


def detect_traffic_light(frame):
    result = frame.copy()
    height, width = frame.shape[:2]

    # 신호등 탐지 ROI
    roi_y_start = int(height * 0.15)
    roi_y_end = int(height * 0.95)
    roi = frame[roi_y_start:roi_y_end, :]

    blur = cv2.GaussianBlur(roi, (5, 5), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # RED 범위
    lower_red1 = np.array([0, 30, 50])
    upper_red1 = np.array([20, 255, 255])

    lower_red2 = np.array([145, 30, 50])
    upper_red2 = np.array([180, 255, 255])

    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    # GREEN 범위
    lower_green = np.array([35, 40, 50])
    upper_green = np.array([95, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    kernel = np.ones((5, 5), np.uint8)

    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)

    def find_best_light(mask):
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        best_area = 0
        best_box = None
        best_circle = None

        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area < 30:
                continue

            x, y, w, h = cv2.boundingRect(cnt)

            ratio = w / h
            if ratio < 0.4 or ratio > 2.2:
                continue

            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue

            circularity = 4 * np.pi * area / (perimeter * perimeter)

            if circularity < 0.15:
                continue

            (cx, cy), radius = cv2.minEnclosingCircle(cnt)

            if area > best_area:
                best_area = area
                best_box = (x, y + roi_y_start, w, h)
                best_circle = (int(cx), int(cy + roi_y_start), int(radius))

        return best_area, best_box, best_circle

    red_area, red_box, red_circle = find_best_light(red_mask)
    green_area, green_box, green_circle = find_best_light(green_mask)

    state = "NONE"

    if red_area > green_area and red_box is not None:
        state = "RED"
        x, y, w, h = red_box
        cx, cy, r = red_circle

        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 3)
        cv2.circle(result, (cx, cy), r, (0, 0, 255), 3)

    elif green_area > red_area and green_box is not None:
        state = "GREEN"
        x, y, w, h = green_box
        cx, cy, r = green_circle

        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.circle(result, (cx, cy), r, (0, 255, 0), 3)

    cv2.putText(result, f"Traffic Light: {state}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 3)

    cv2.putText(result, f"Red Area: {int(red_area)}", (30, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.putText(result, f"Green Area: {int(green_area)}", (30, 125),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return result, red_mask, green_mask, state


file_name = input("이미지 파일명을 입력하세요: ")

img = cv2.imread(file_name)

if img is None:
    print("이미지를 찾을 수 없습니다. 파일 이름과 위치를 확인하세요.")

else:
    img = cv2.resize(img, (600, 800))

    result, red_mask, green_mask, state = detect_traffic_light(img)

    print("현재 신호등 상태:", state)

    cv2.imshow("Red Mask", red_mask)
    cv2.imshow("Green Mask", green_mask)
    cv2.imshow("Detection Result", result)

    save_name = "result_" + state.lower() + ".png"
    cv2.imwrite(save_name, result)

    print("결과 이미지 저장 완료:", save_name)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
