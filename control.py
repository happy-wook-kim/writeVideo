from datetime import datetime
from time import sleep
from capturing import get_capture
import cv2
from upload_vids import Uploads
import threading

now = datetime
start = now.now().timestamp();
count = 0

while True:
    end = now.now().timestamp();
    
    elapsed = end - start;
    # print(elapsed)
    
    if elapsed > 0.01:
        # 스트리밍 녹화 시작 시간을 기준으로 년, 월, 일, 시간, 분, 초 데이터를 받는다.
        year = str(now.now().today().year)
        month = str(now.now().today().month).zfill(2)
        day = str(now.now().today().day).zfill(2)
        hour = str(now.now().today().hour).zfill(2)
        minute = str(now.now().today().minute).zfill(2)
        second = str(now.now().today().second).zfill(2)
        # file_name = str(now.now().today()).rsplit('.', 1)[0]
        # 파일명을 원하는 형태로 만든다.
        file_name = year + "_" + month + "_" + day + "_" + hour + ":" + minute + ":" + second
        try:
            # 스트리밍 영상 녹화 쓰레드
            t = threading.Thread(get_capture(file_name))
            t.start()
            print('capture thread start')
        except:
            # 통신에러 등 에러가 발생했을 때 10초 대기 후 while문을 다시 돈다.
            print('스트리밍 영상 캡처에 에러가 발생하였습니다. 2초 후 다시 동작을 시도합니다.')
            sleep(2)
        else:
            # 스트리밍 영상 녹화 후 서버로 전송
            # 대기 시간 초기화
            start = now.now().timestamp()
            elapsed = end - start

            name = './video/cam1' + '_' + file_name + '.mp4'
            # name_15f = './video/cam1' + '_' + file_name + '_15f' + '.mp4'
            name_30f = './video/cam1' + '_' + file_name + '_30f' + '.mp4'
            
            print('전송할 영상: ', name, "\n" , 'opencv 읽는 영상: ', name)
            # video = cv2.VideoCapture(name)
            
            # 서버로 영상 전송
            upload = Uploads(name, '')
            try:
                upload_thread = threading.Thread(upload.upload_video(name))
                upload_thread.start()
                # upload_thread_15f = threading.Thread(upload.upload_video(name_15f))
                # upload_thread_15f.start()
                upload_thread_30f = threading.Thread(upload.upload_video(name_30f))
                upload_thread_30f.start()
            except (FileNotFoundError):
                print('동영상 파일을 찾을 수 없습니다.')
            except ConnectionError:
                print('통신 에러 발생')
                sleep(1)
            except:
                print('영상 전송에 에러가 발생하였습니다.')
                sleep(1) 
        finally:
            count += 1
