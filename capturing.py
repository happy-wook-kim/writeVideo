from time import sleep
import cv2
import datetime


def get_capture(file_name:str):
    url = 'rtmp://52.78.104.124:1935/live/cam1'
    url2 = 'http://52.78.104.124:1935/vod/mp4:sample.mp4/playlist.m3u8'

    cap = cv2.VideoCapture(url)
    # cap = cv2.VideoCapture(0)

    name = './video/cam1' + '_' + file_name + '.mp4'
    name_15f = './video/cam1' + '_' + file_name + '_15f' + '.mp4'
    name_30f = './video/cam1' + '_' + file_name + '_30f' + '.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(name, fourcc, 10.0, (int(cap.get(3)), (int(cap.get(4)))))
    # out_15f = cv2.VideoWriter(name_15f, fourcc, 15.0, (int(cap.get(3)), (int(cap.get(4)))))
    out_30f = cv2.VideoWriter(name_30f, fourcc, 30.0, (int(cap.get(3)), (int(cap.get(4)))))

    start = datetime.datetime.now()
    count = 1
    print('capture start time: ', start)
    while True:
        try:
            ret, frame = cap.read()
            h, w, _ = frame.shape
            count += 1
            if ret is True:
                # frame = np.clip(contrast * frame + brightness, 0, 255)
                cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
                cv2.imshow('cam1', frame)
                end = datetime.datetime.now()
                elapsed = end - start

                if count % 3 == 0:
                    out.write(frame)
                    # out_15f.write(frame)
                    out_30f.write(frame)
                
                if count % 6 == 0:
                    print('time elapsed', elapsed.seconds)

                if elapsed.seconds % 10 == 0 and elapsed.seconds > 0:
                    # i += 1
                    pass

                if cv2.waitKey(5) & 0xFF == 27:
                    break
                
                # 영상을 15분 기준으로 끊어서 저장한다.
                if elapsed.seconds > 900:
                    break

        except:
            break

    print('녹화한 영상: ',name)
    cap.release()
    cv2.destroyAllWindows()