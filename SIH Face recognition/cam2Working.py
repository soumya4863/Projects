from datetime import datetime
from datetime import date
import cv2
def capture1():
    url = 'http://192.168.246.61:8080/video'

    status=""
    cap = cv2.VideoCapture(url)
    while(True):
        ret, frame = cap.read()
        if frame is not None:
            cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            cv2.imshow('frame',frame)
        q = cv2.waitKey(1)
        if q == ord('s'): 
            dat = datetime.now()
            print(date.today())
            EXTENSION = 'png'
            file_name_format = "{:%Y-%m-%d_%H-%M-%S}.{:s}"
            file_name = file_name_format.format(dat, EXTENSION)
            img=frame
            cv2.imwrite(f'loginPage/test/{file_name}',img)
            cap.release()
            status="captured"
            break
        elif q == ord("q"):
            status="Did not capture photo "
            break

    cv2.destroyAllWindows()
    return status

def capture(name,rollno):
    url = 'http://192.168.246.61:8080/video'

    status=""
    cap = cv2.VideoCapture(url)
    while(True):
        ret, frame = cap.read()
        if frame is not None:
            cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            cv2.imshow('frame',frame)
        q = cv2.waitKey(1)
        if q == ord('s'): 
            dat = rollno+"_"+name
            EXTENSION = 'png'
            file_name_format = "{}.{:s}"
            file_name = file_name_format.format(dat, EXTENSION)
            img=frame
            cv2.imwrite(f'loginPageimages/{file_name}',img)
            cap.release()
            status="captured"
            break
        elif q == ord("q"):
            status="Did not capture photo "
            break
                    
        
    cv2.destroyAllWindows()
    return status