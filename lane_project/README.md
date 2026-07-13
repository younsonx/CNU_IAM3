## 차선인식 프로젝트
요구사항  
```
<과제 목표>
도로 이미지 또는 주행 영상에서 차선을 검출하고,
차량이 차선 중심에서 얼마나 벗어났는지 lane error를 계산한다.

<사용할 코드 범위>
Part 2.2 그레이스케일 변환
Part 2.3 이진화
Part 2.4 Gaussian Blur
Part 2.6 Canny Edge Detection
Part 2.7 형태학적 연산
Part 3.7 Hough Transform
Part 4.2 VideoCapture
Part 4.3 프레임별 이미지 처리

<Level별 가이드라인>
Level 1. 기본 차선 마스크 만들기
구현해야 하는 것:
1. 이미지 또는 영상 프레임을 입력받는다.
2. Grayscale로 변환한다.
3. Gaussian Blur를 적용한다.
4. Threshold 또는 Canny를 적용한다.
5. ROI를 설정해서 화면 아래쪽 도로 영역만 남긴다.
6. 결과를 화면에 표시한다.

Level 2. 차선 중심 계산하기
구현해야 하는 것:
1. ROI 내부에서 차선 후보 픽셀의 x좌표를 구한다.
2. 차선 중심 x좌표를 계산한다.
3. 이미지 중앙 x좌표와 비교한다.
4. lane error를 계산한다.
5. 화면에 image center, lane center, error를 표시한다.

Level 3. Hough Line으로 차선 직선 검출하기
구현해야 하는 것:
1. Canny edge를 적용한다.
2. HoughLinesP로 선분을 검출한다.
3. 너무 수평인 선은 제외한다.
4. 기울기를 기준으로 왼쪽 차선/오른쪽 차선을 분리한다.
5. 검출된 선분을 원본 영상 위에 그린다.
6. 차선 중심과 lane error를 계산한다.
```

## 신호등인식 프로젝트
```
<과제 목표>
영상 또는 웹캠 화면에서 빨간불과 초록불을 검출하고,
현재 신호등 상태를 RED, GREEN, NONE 중 하나로 출력한다.

<사용할 코드 범위>
Part 2.4 Gaussian Blur
Part 2.7 형태학적 연산
Part 3.2 Contour 검출 기초
Part 3.3 윤곽선의 특징 계산
Part 3.6 Bounding Rectangle / 최소 외접 원
Part 3.8 실시간 색상 객체 추적
Part 4.2 VideoCapture
Part 4.3 프레임별 이미지 처리

<Level별 가이드라인>
Level 1. 빨간색/초록색 마스크 만들기
구현해야 하는 것:
1. BGR 이미지를 HSV로 변환한다.
2. 빨간색 HSV 범위를 설정한다.
3. 초록색 HSV 범위를 설정한다.
4. red_mask, green_mask를 만든다.
5. 마스크 결과를 화면에 표시한다.

Level 2. Contour로 신호등 후보 검출하기
구현해야 하는 것:
1. red_mask에서 contour를 찾는다.
2. green_mask에서 contour를 찾는다.
3. 가장 큰 contour의 면적을 계산한다.
4. 면적이 threshold 이상이면 신호등으로 판단한다.
5. 빨간색이면 RED, 초록색이면 GREEN, 없으면 NONE을 출력한다.

Level 3. 오검출 줄이기
추가 조건:
1. 화면 위쪽 영역에서만 신호등을 찾기
2. contour 면적이 너무 작으면 무시하기
3. bounding box의 가로세로 비율 확인하기
4. 원형에 가까운 contour만 신호등 후보로 보기
```
