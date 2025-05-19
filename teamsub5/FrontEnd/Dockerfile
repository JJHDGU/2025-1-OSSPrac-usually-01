# Dockerfile

# 베이스 이미지 지정 : 이미지는 flask + nginx + uwsgi가 기본 설정된 이미지,
# Flask 어플리케이션을 실행하는데 필요한 모듈이 이미 포함된 이미지
FROM tiangolo/uwsgi-nginx-flask:python3.9

# 현재 디렉토리의 ./Subject3_1/app 디렉토리를 컨테이너의 /app 디렉토리에 복사
COPY Subject3_1/app /app