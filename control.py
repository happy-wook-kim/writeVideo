from datetime import datetime
from time import sleep
from typing import final
from test import get_capture
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
        year = str(now.now().today().year)
        month = str(now.now().today().month).zfill(2)
        day = str(now.now().today().day).zfill(2)
        hour = str(now.now().today().hour).zfill(2)
        minute = str(now.now().today().minute).zfill(2)
        second = str(now.now().today().second).zfill(2)
        # file_name = str(now.now().today()).rsplit('.', 1)[0]
        file_name = year + "_" + month + "_" + day + "_" + hour + ":" + minute + ":" + second
        
        try:
            # 스트리밍 영상 녹화 쓰레드
            t = threading.Thread(get_capture(file_name))
            t.start()
        except:
            # 통신에러 등 에러가 발생했을 때 10초 대기 후 while문을 다시 돈다.
            print('스트리밍 영상 캡처에 에러가 발생하였습니다. 10초 후 다시 동작을 시도합니다.')
            sleep(10)
        else:
            # 스트리밍 영상 녹화 후 서버로 전송
            # 대기 시간 초기화
            start = now.now().timestamp()
            elapsed = end - start

            name = './video/cam1' + '_' + file_name + '.mp4'
            
            print('전송할 영상: ', name, "\n" , 'opencv 읽는 영상: ', name)
            video = cv2.VideoCapture(name)
            
            # 서버로 영상 전송
            a = Uploads(name, '')
            try:
                upload_thread = threading.Thread(a.upload_video(name))
                upload_thread.start()
            except (FileNotFoundError):
                print('동영상 파일을 찾을 수 없습니다.')
            except ConnectionError:
                print('통신 에러 발생')
                sleep(2)
            except:
                print('영상 전송에 에러가 발생하였습니다.')
                sleep(2) 
        finally:
            count += 1
