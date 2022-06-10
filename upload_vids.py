import requests, cv2
import datetime
from requests.adapters import HTTPAdapter, Retry
from requests.sessions import Session

# import test

# server_url = "http://10.10.20.137:8000"
server_url = "http://192.168.20.131:8000"

class Uploads:
    def __init__(self, url, key):
        self.url = url
        self.key = key

    def upload_video(self, name):
        print('upload start')
        at_that_time = datetime.datetime
        start = at_that_time.now().timestamp()
        
        # 파일을 rb (바이너리 리드)형태로 열람한다.
        # file = open('./Guy.mp4', 'rb')
        # file = open('./36_hours.mp4', 'rb')
        # file = open('./Strangers.mp4', 'rb')
        file = open(name, 'rb')
        
        # python 딕셔너리 형식으로 파일 설정
        upload_file = {'files': file}

        with Session() as session:
            connect = 3
            read = 3
            backoff_factor = 0.3
            RETRY_AFTER_STATUS_CODES = (400, 403, 500, 503)

            retry = Retry(
                total=connect,
                connect=connect,
                read=read,
                backoff_factor=backoff_factor,
                status_forcelist=RETRY_AFTER_STATUS_CODES,
            )

            adapter = HTTPAdapter(max_retries=retry)
            # http:// 로 시작하면 adapter 내용을 적용
            session.mount("http://", adapter)
            # https:// 로 시작하면 adapter 내용을 적용
            session.mount("https://", adapter)

            try:
                # post 요청 수행
                session.post(url='http://192.168.20.131:8000/uploadfiles', files = upload_file)
            except:
                print('업로드에 실패하였습니다.')
            else:  
                end = at_that_time.now().timestamp()
                elapsed = end - start
                print(elapsed)
                print('upload finish')
