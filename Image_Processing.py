import cv2

def image_processing(frame) :
    # 원본 영상 그레이스케일 적용
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 원본 영상 lab 색공간 이미지로 변환
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    # 채널 분리
    # l : 밝기, a : 녹색에서 마젠타까지 색상구성 요소, b : 파란색에서 노란색까지의 색상 구성 요소
    l, a, b = cv2.split(lab)

    # median 필터 적용
    median = cv2.medianBlur(l,99)
    # 밝기 채널 반전
    invert = cv2.bitwise_not(median)
    # 그레이스케일 영상과 합성하여 선명한 영상 생성
    composed = cv2.addWeighted(gray, 0.75, invert, 0.25, 0)

    return l, composed

