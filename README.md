# Programmers Autonomous-Driving Dev course. Final_Project_TeamB
[K-Digital-Training] 자율주행 최종 경진대회

## Member Roles

| 이름         | 담당                                         |
| ------------ | :------------------------------------------- |
| 허석(팀장) | SLAM과 Stanley를 이용한 Path tracking 및 모드 통합 구현 |
| 김민경       | 신호등 인식 및 장애물 회피 기능 구현 |
| 이우석       | 평행 주차 및 모드 통합 기능 구현 |
| 조영진       | SLAM, YOLO, AR tag 인식, 주차, 로터리 기능 구현 |

## Goal
---
![image](https://user-images.githubusercontent.com/65532515/134897572-cd5bc826-b7aa-4ae9-9293-1c176a6c41f7.png)
### 1. 직선구간
  - 출발
    - 신호등 인식하여 파란불에 출발
  - 차선 변경
    - 2차선 출발, 1차선에서 주행중인 차량을 피해 차선 변경 후 트랙 주행
### 2. 교차로 구간
  - 정지선
    - 교차로 진입시 정지선 인식 및 저이
  - 신호등
    - 신호인식 후 주행
  - T주차
    - AR태그 인식 후 T주차 진행 (전면, 후면 가능)
  - 타겟정차
    - 미션 수행을 위해 사람, 고양이 순으로 각 이미지 앞 5초간 정차
    - 5초 이상 정차하지 않을 경우 정차로 인정 불가
### 3. 곡선 구간
  - 차선인식
    - 차선을 인식하여 곡선 주행
    - 블럭을 넘어뜨리지 않고 주행
### 4. 경사로 구간
  - 진입
    - 경사로 내 주행
  - 정지선
    - 경사로 퇴출 후 정지선 인식 및 정지
### 5. 로터리 구간
  - 회전 주행
    - 회전중인 차량 피해 진입 후 충돌하지 않고 주행
### 6. 장애물 구간
  - 갓길 정차된 장애물 차량 피해 좁은길 주행 (차선 이탈 임시 허용)
### 7. 평행주차 구간
  - AR태그 인식 후 비어있는 공간을 찾아 평행 주차

## Environment
---
- Ubuntu 18.04
- ROS Melodic
- 1/10 scale model car
- Nvidia TX 2

## Structure
---
~~~
final_project
  └─ calibration
  │    └─ ost.txt
  │    └─ ost.yaml
  └─ config
  │    └─ mapping.lua
  │    └─ xycar_localization_v1.lua
  └─ launch
  │    └─ TEAM_BOLD.launch           
  └─ maps
  │    └─ xycar_map_9_17_final.pbstream
  └─ path
  │    └─ reference_path_final1.pkl
  │    └─ reference_path_final2.pkl
  │    └─ reference_path_final3.pkl
  │    └─ draw_path.py
  │    └─ map_drawer.py
  │    └─ rosbag_to_map.py
  └─ rviz
  │    └─ localization.rviz
  │    └─ offline_mapping.rviz
  │    └─ offline_mapping_youngjin.rviz
  └─ src
  │    └─ Control
  │    │    └─ T_Parking.py
  │    │    └─ motor.py
  │    │    └─ parallel.py
  │    │    └─ pid.py
  │    │    └─ stanley.py
  │    │    └─ stanley_follower.py
  │    └─ Perception
  │    │    └─ avoid_obstacle.py
  │    │    └─ interrupt.py
  │    │    └─ rotary_lidar.py
  │    │    └─ stopline.py
  │    │    └─ traffic_sign.py
  │    │    └─ yolo.py
  │    └─ TEAM_BOLD.py
  │    └─ xycar.py
  └─ urdf
  │    └─ xycar.urdf          
~~~

## Usage
---
~~~bash
$ roslaunch final_project TEAM_BOLD.launch
~~~

## Procedure
---
### mapping
![image (2)](https://user-images.githubusercontent.com/65532515/134633108-9ed5957a-f9e4-4f48-b7af-3e2ac3cf81aa.png)
- mapping 전용 lua 파일을 이용하여 주행할 맵을 매핑한다.
### localization
![image](https://user-images.githubusercontent.com/65532515/134635003-8f8fad1a-d4a3-4ae6-8a53-b621d457782a.png)
- 위에서 제작한 맵을 토대로 localization을 진행한다. 
### path planning & control
![image](https://user-images.githubusercontent.com/65532515/134119319-62f924a7-be56-4271-8923-5a333136f601.png)
- 맵의 x, y 좌표와 차의 현재 위치(x, y)좌표를 비교하여 heading error와 cross track error(cte) 를 구하고, steering angle 값을 도출하여 reference path대로 따라갈 수 있도록 path planning 진행.
### Stopline
![image](https://user-images.githubusercontent.com/65532515/134637921-ea0ce2f4-2841-41a2-8f3a-794d42f41662.png)
- localization을 통한 차량의 현재위치를 구해 reference path 상의 정지선 위치에서 정차하도록 구현.
### Traffic Sign
![image](https://user-images.githubusercontent.com/65532515/134639892-8dbe0e81-a148-4a3f-915a-42c75a65f61e.png)
- 신호등에서 원 3개를 인식하여, 그 중 맨 오른쪽 원(파란 불)의 명도가 높을 시 출발
- 불이 켜진 원의 색깔을 인식하여 신호 판별.
- 신호등에서 원의 위치를 파악하여 신호 판별.
### T_parking
![image](https://user-images.githubusercontent.com/65532515/134636638-3afb65bd-5c98-4a9f-81e9-0ddcf431cffb.png)
- AR 태그를 인식해 차량의 yaw값을 구해 그 값에 10.0 만큼 곱한 값을 angle값을 사용하여 주차공간에 주차.
### Target Stop
![image](https://user-images.githubusercontent.com/65532515/134637519-e8cdd67f-f211-4e86-acc0-1eb0a69b6a18.png)
- Approach 1 : localization을 통한 차량의 현재위치를 구해 reference path 상의 타겟위치에서 5초간 정차하도록 구현.
- Approach 2 : yolo를 이용하여 bounding_boxes 토픽의 Class값이 person, cat이고, 확률이 30%이상이면 5초간 정차하도록 구현.
### Slope
![image](https://user-images.githubusercontent.com/65532515/134640162-a825e691-13e7-439e-8e2b-34637f598846.png)
- imu 데이터를 이용해 오르막길로 인식되면 모터 출력을 강하게 하여 올라간 후 내리막길로 인식되면 모터 출력을 0으로 하여 정차를 원할히 할 수 있도록 함.
### Rotary
![image](https://user-images.githubusercontent.com/65532515/134640778-f2e804e9-a716-4f79-8413-c2bdbe77de4c.png)
- 라이다의 오른쪽 45° 값을 받아 1.5이하이면 차가 지나간 것으로 인식하여 출발

## Limitations & Try
---
### Stanley
- localization이 잘 되지 않아 path를 잘 따라가지 못함
  - lua파일 파라미터 튜닝 부족과 연산량이 많았기 때문으로 추정.
    - 시도한 방안
      - stanley_follower파일에서 stanley 연산을 위해 map 좌표를 넣어줄 때 모두 다 넣어주지 않고, 현재위치의 앞 뒤 일정 구간을 슬라이싱하여 넣어줌
        - stanley연산을 할 때 min_index값이 계속 같은 값으로 들어가 슬라이싱 하는 구간을 업데이트 할 수 없어 사용하지 못함.
    - 효과가 있었던 해결 방안
    
      ![image](https://user-images.githubusercontent.com/65532515/134892345-78420557-a668-4282-8997-fc1dac7a5265.png)
      - stanley 메소드에서 map에서 현재위치와 가장 가까운 index를 계산할 때 찾는 간격을 넓혀 연산량을 줄임.
  - 오프라인 맵 환경이 수시로 달라져 정확한 localization을 하기에 어려운 환경이었음.
### T-Parking
- 차량의 yaw값을 이용하였는데, ar태그의 왼쪽, 오른쪽에 있어도 yaw값만 맞으면 주차가 잘 된것으로 인식하는 문제가 있었음.
  - ar태그의 DX, DZ값을 이용해 arctan(DX/DZ) 만큼 각도 값으로 주어 후진하도록 수정.
### Obstacle Avoidance & Rotary Mission
- 라이다의 노이즈값 (0값)이 매우 많아 장애물을 정확히 측정할 수 없는 문제가 있었음.
  - 라이다 측정값 중 0인 값을 필터링하여 해결.
### Traffic Sign
- 각 신호등의 위치마다 화면 밝기와 화면 상 신호등의 위치가 다른 문제점이 있었음
  - 각 신호등마다 roi를 달리하고 화면 밝기 문제에서 사각형이 인식이 잘 안되는 문제는 opencv의 convexhull을 이용하여 해결.

## What I've learned
---
- SLAM을 이용한 자율주행을 경험해보니, 연산량을 줄이는 작업이 굉장히 중요하고, 파라미터 튜닝이 굉장히 중요하다는 점을 배웠다.
- 라이다를 이용한 장애물 회피주행이나, 로터리 미션등을 수행하면서, 센서의 노이즈값을 줄이는 과정이 매우 중요하다는 점을 배웠다.
