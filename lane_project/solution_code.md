# Level 1. 기본 차선 마스크 만들기

### 1.이미지 입력
```py
img = cv2.imread("road.jpg")
```
도로 사진 불러오기 

```py
img = cv2.resize(img, (900, 500))
```
사진 크기를 일정하게 맞춤 => 좌표 계산 안정적

### 2.Grayscale 변환
```py
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```
컬러 사진 흑백사진으로 바꾸기  

차선 검출에서는 색깔보다  
밝은 차선과 어두운 도로의 차이가 중요함. 따라서 흑백으로 바꾸기

### 3.Gaussian Blur 적용
```py
blur = cv2.GaussianBlur(gray, (5, 5), 0)
```
이미지를 살짝 흐리게 만듬

왜냐면 사진에는 작은 점이나, 잡음이 많음  
이 잡음을 줄여야 Canny가 차선을 더 잘 찾을수 있음

### 4.Canny Edge Detection
```py
edge = cv2.Canny(blur, 50, 150)
```
이미지에서 경계선 찾음

예를들어 도로는 어둡고, 차선은 하양기 때문에 그 경계 부분이 선으로 잡힘  
즉 이 단계에서 차선 후보들이 나타나기 시작

### 5.ROI 설정
```py
mask = np.zeros_like(edge)
```
검은색 마스크를 만듬
```py
polygon = np.array([[
    (0, height),
    (width, height),
    (int(width * 0.65), int(height * 0.55)),
    (int(width * 0.35), int(height * 0.55))
]], dtype=np.int32)
```
도로 아래쪽 영역을 사다리꼴로 잡음  

도로 사진에서는 차선이 보통 아래쪽에 크게 보이고, 멀리 갈 수록 좁아져서 사다리꼴 ROI를 사용함.
```py
cv2.fillPoly(mask, polygon, 255)
```
차선을 찾을 영역만 흰색으로 칠함
```py
roi = cv2.bitwise_and(edge, mask)
```
전체 edge 이미지 중에서 ROI안 쪽만 남김 즉,  
전체 이미지에서 차선이 있을 법한 도로 영역만 검사

### 도로위 숫자 60 제거
```py
cv2.rectangle(
    mask,
    (int(width * 0.25), int(height * 0.52)),
    (int(width * 0.72), int(height * 0.92)),
    0,
    -1
)
```
도로 중앙의 큰 60 숫자가 차선처럼 인식될 수 있음  
그래서 이 부분은 마스크에서 제거함  

즉, 숫자 60 부분은 차선을 찾을때 무시해라 라는 뜻이 됨

# Level 2. 차선 중심 계산하기
차선의 중앙이 어디인지 찾고, 차량이 얼마나 벗어났는지를 계산하는 단계

### 1.이미지 중앙 구하기
```py
height, width = edge.shape
image_center = width // 2
```
이미지 가로 길이가 900이면 중앙은 450  

이미지 중앙 = 차량이 바라보는 기준 중앙

### 2.차선 후보 픽셀의 x좌표 구하기
```py
left_lane_x = get_lane_x(left_lines, height)
right_lane_x = get_lane_x(right_lines, height)
```
