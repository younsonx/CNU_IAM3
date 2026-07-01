import cv2
import numpy as np


img = cv2.imread("road.jpg")

if img is None:
    print("이미지를 찾을 수 없습니다. 파일 이름을 확인하세요.")

else:
    img = cv2.resize(img, (900, 500))
    result = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edge = cv2.Canny(blur, 50, 150)

    height, width = edge.shape
    image_center = width // 2

    mask = np.zeros_like(edge)

    polygon = np.array([[
        (0, height),
        (width, height),
        (int(width * 0.65), int(height * 0.55)),
        (int(width * 0.35), int(height * 0.55))
    ]], dtype=np.int32)

    cv2.fillPoly(mask, polygon, 255)

    cv2.rectangle(
        mask,
        (int(width * 0.25), int(height * 0.52)),
        (int(width * 0.72), int(height * 0.92)),
        0,
        -1
    )

    roi = cv2.bitwise_and(edge, mask)

    lines = cv2.HoughLinesP(
        roi,
        rho=1,
        theta=np.pi / 180,
        threshold=35,
        minLineLength=35,
        maxLineGap=90
    )

    left_lines = []
    right_lines = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            if x2 - x1 == 0:
                continue

            slope = (y2 - y1) / (x2 - x1)

            if abs(slope) < 0.4:
                continue

            length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            if length < 30:
                continue

            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2

            if int(width * 0.25) < mid_x < int(width * 0.72) and int(height * 0.52) < mid_y < int(height * 0.92):
                continue

            if slope < 0:
                left_lines.append((x1, y1, x2, y2))
                cv2.line(result, (x1, y1), (x2, y2), (255, 0, 0), 3)
            else:
                right_lines.append((x1, y1, x2, y2))
                cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 3)

    def get_lane_x(lines, y_target):
        x_list = []

        for x1, y1, x2, y2 in lines:
            if x2 - x1 == 0:
                continue

            slope = (y2 - y1) / (x2 - x1)

            if slope == 0:
                continue

            x = int(x1 + (y_target - y1) / slope)
            x_list.append(x)

        if len(x_list) == 0:
            return None

        return int(np.mean(x_list))

    left_lane_x = get_lane_x(left_lines, height)
    right_lane_x = get_lane_x(right_lines, height)

    lane_center = image_center
    lane_error = 0

    if left_lane_x is not None and right_lane_x is not None:
        lane_center = (left_lane_x + right_lane_x) // 2
        lane_error = image_center - lane_center

        cv2.line(result, (left_lane_x, height), (left_lane_x, int(height * 0.55)), (255, 0, 0), 3)
        cv2.line(result, (right_lane_x, height), (right_lane_x, int(height * 0.55)), (0, 255, 0), 3)

    elif left_lane_x is not None:
        lane_center = left_lane_x + 300
        lane_error = image_center - lane_center
        cv2.line(result, (left_lane_x, height), (left_lane_x, int(height * 0.55)), (255, 0, 0), 3)

    elif right_lane_x is not None:
        lane_center = right_lane_x - 300
        lane_error = image_center - lane_center
        cv2.line(result, (right_lane_x, height), (right_lane_x, int(height * 0.55)), (0, 255, 0), 3)

    cv2.line(result, (image_center, height), (image_center, int(height * 0.55)), (0, 0, 255), 2)
    cv2.line(result, (lane_center, height), (lane_center, int(height * 0.55)), (0, 255, 255), 2)

    cv2.putText(result, f"Image Center: {image_center}", (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.putText(result, f"Lane Center: {lane_center}", (30, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.putText(result, f"Lane Error: {lane_error} px", (30, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.imshow("ROI Result", roi)
    cv2.imshow("Lane Detection Result", result)

    cv2.imwrite("roi_result.png", roi)
    cv2.imwrite("lane_result.png", result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
