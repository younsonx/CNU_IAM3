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
