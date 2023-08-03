# RTK_GPS

- RTK GPS가 서버가 되어 NMEA 프로토콜을 이용한 GPS신호(위도, 경도 등)를 클라이언트(우리가 만든 프로그램)에게  TCP통신으로 전달함.
- NMEA 프로토콜 참고: https://techlog.gurucat.net/239

##Main.py##
지도(지도명에 미터단위의 실제 크기 포함)를 불러와 지형(그리도)에 가중치를 직접 부여 후 json 파일로 변환하는 코드임.

##MainMatching_GPS.py##
GPS 정보를 이용해 실시간 지도에서 나의 위치를 확인하는 코드임.

##MainRealAnnotation.py##
Main.py와 달리 GPS정보를 수신해 자동으로 지도의 영역 별 가중치를 부여 후 json으로 변환하는 코드임.
