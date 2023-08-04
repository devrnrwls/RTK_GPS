# RTK_GPS

- 사용한 GTK GNSS 수신기: https://www.ppsoln.com/RTAP2U
- RTK GNSS 수신기가 서버가 되어 NMEA 프로토콜을 이용한 GPS신호(위도, 경도 등)를 클라이언트(우리가 만든 프로그램)에게  TCP통신으로 전달함.
- NMEA 프로토콜 참고: https://techlog.gurucat.net/239
- bearing 참고: https://www.movable-type.co.uk/scripts/latlong.html
- 미터 당 위도, 경도 값 참고: https://blog.naver.com/jinohpark79/221170630625

##지도 이미지 자르기
최초 지도를 만들때 실제 지도 크기(m단위)를 추정해서 자르고 우분투 그림판에서 "(실제지도크기 / 가로 이미지) = 픽셀 당 실제지도크기"(나머지 부분은 잘라버림)를 고려해야 향후 그리드가 이쁘게 나옴

##Main.py##
지도(지도명에 미터단위의 실제 크기 포함)를 불러와 지형(그리도)에 가중치를 직접 부여 후 json 파일로 변환하는 코드임.

##MainMatching_GPS.py##
GPS 정보를 이용해 실시간 지도에서 나의 위치를 확인하는 코드임.

##MainRealAnnotation.py##
Main.py와 달리 GPS정보를 수신해 자동으로 지도의 영역 별 가중치를 부여 후 json으로 변환하는 코드임.
