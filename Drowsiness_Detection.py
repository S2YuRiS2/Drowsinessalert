import dlib
import imutils
import cv2
from imutils.video import VideoStream
from scipy.spatial import distance as dist
from imutils import face_utils
from Alarm import sound_alarm
from Image_Processing import image_processing
import pymysql
import time

mysqldb = pymysql.connect(
    user = 'root',
    passwd= 'dbfldbqls12!',
    host = '127.0.0.1',
    db = 'sensor',
    charset = 'utf8'
)

cursor = mysqldb.cursor()
sql = "select co2_value, heartbeat_value from sensor"

cursor.execute(sql)
mysqldb.commit()
datas = cursor.fetchone()

# print(datas)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("LearningData/shape_predictor_68_face_landmarks.dat")
blink_cascade = cv2.CascadeClassifier('LearningData/BlinkCascade.xml')

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

COUNTER = 0

class Drowsiness_Detection:
    def __init__(self):
        print('init')
        while datas:
            co2_value = datas[0]
            heartbeat_value = datas[1]
            print(co2_value)
            print(heartbeat_value)

            time.sleep(2)
            if co2_value>=20.0 and heartbeat_value>=10:
                self.run()
        # self.run()

    def eye_aspect_ratio(self, eye):
        # 유클리드 거리 계산
        # A, B는 눈의 가로 길이(횡)을 계산
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # 눈의 세로 길이(종) 계산
        C = dist.euclidean(eye[0], eye[3])

        # 눈 종횡비율 계산
        ear = (A + B) / (2.0 * C)

        return ear

    def run(self):
        global blink_cascade
        global COUNTER
        cam = VideoStream(src=0).start()
        name = "Drowsiness Detection Test"

        while True:
            frame = cam.read()
            frame = imutils.resize(frame, width=640)
            frame = cv2.flip(frame, 1)
            cv2.namedWindow(name)
            cv2.moveWindow(name, 300, 100)
            L, gray = image_processing(frame)
            rects = detector(gray, 0)

            for i, rect in enumerate(rects):
                # 얼굴 탐지
                cv2.putText(frame, "Face #{}".format(i+1), (rect.left() - 10, rect.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0),2)
                cv2.rectangle(frame, (rect.left(),rect.top()),(rect.right(),rect.bottom()), (255, 255, 0), 2)
                shape = predictor(gray,rect)
                shape = face_utils.shape_to_np(shape)

                # 유클리드 거리 계산법으로 왼쪽, 오른쪽 눈 위치 추출
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = self.eye_aspect_ratio(leftEye)
                rightEAR = self.eye_aspect_ratio(rightEye)

                both_ear = (leftEAR + rightEAR) / 2.0

                left_EyeHull = cv2.convexHull(leftEye)
                right_EyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [left_EyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [right_EyeHull], -1, (0, 255, 0), 1)

                roi_gray = gray[rect.top():rect.bottom(),rect.left():rect.right()]
                roi_color = frame[rect.top():rect.bottom(),rect.left():rect.right()]

                if both_ear <= 0.2:
                    # 눈 깜빡임 탐지
                    blink = blink_cascade.detectMultiScale(roi_gray)
                    for (eyx, eyy, eyw, eyh) in blink:
                        cv2.rectangle(roi_color, (eyx, eyy), (eyx + eyw, eyy + eyh), (0, 0, 255), 2)
                        COUNTER += 1
                        if COUNTER == 30:
                            COUNTER = 0
                            sound_alarm()
                            cv2.putText(frame, "Drowsiness detection", (rect.left() - 10, rect.top() - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 255), 2)
                        elif COUNTER>30:
                            COUNTER = 0

                    cv2.putText(frame, "EAR : {:.2f}".format(both_ear), (520, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 30, 20), 2)

            cv2.imshow(name, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        cv2.destroyAllWindows()
        cam.stop()