import os
import pickle

import cv2
import numpy as np

import utils


def check_parking_space(img, img_prepro, pos_list):
    space_count = 0
    for pos in pos_list:
        x, y = pos
        # 抓出每個車位
        img_crop = img_prepro[y:y+utils.HEIGHT, x:x+utils.WIDTH]
        count = cv2.countNonZero(img_crop)

        if count < 1000:
            color = utils.GREEN
            thickness = 3
            space_count += 1
        else:
            color = utils.RED
            thickness = 2

        # utils.write_text(img=img, scale=0.5,
        #                  color=color, offset=1, thickness=1,
        #                  pos=(x, y+utils.HEIGHT-3),
        #                  text=str(count))
        utils.draw_rectangle(img=img, start_point=pos,
                             color=color, thickness=thickness)

    # 車位總數
    text = f'Free: {space_count}/{len(pos_list)}'
    utils.write_text(img=img, pos=(80, 50), text=text)


def preprocess_img(img):
    # black and white
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 消除雜訊 cv2.GaussianBlur(image, kernel, sigma)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    #
    img_threshold = cv2.adaptiveThreshold(img_blur, 255,
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV,
                                          21, 13)
    img_median = cv2.medianBlur(img_threshold, 5)
    kernel = np.ones((3, 3), np.int8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

    return img_dilate


if __name__ == "__main__":

    root_dirname = os.path.dirname(os.path.dirname(__file__))
    VIDEO_FILE_PATH = f"{root_dirname}/data/{utils.CAR_PARK_VIDEO_FNAME}"
    CAR_PARK_POS_PATH = f"{root_dirname}/data/{utils.CAR_PARK_POS_FNAME}"

    pos_list = []
    with open(CAR_PARK_POS_PATH, "rb") as f:
        pos_list = pickle.load(f)

    # cv2.namedWindow("image")
    # cv2.resizeWindow("image", 640, 240)
    # def empty(a):
    #     pass
    # cv2.createTrackbar("a", "image", 2, 100, empty)
    # cv2.createTrackbar("b", "image", 2, 30, empty)
    # cv2.createTrackbar("blur", "image", 2, 30, empty)

    cap = cv2.VideoCapture(VIDEO_FILE_PATH)
    while True:

        # 讓影片重複播放
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        success, img = cap.read()
        # a = cv2.getTrackbarPos("a", "image")
        # a = max(3, a)
        # if (a % 2 == 0):
        #     a  += 1
        # b = cv2.getTrackbarPos("b", "image")
        # blur = cv2.getTrackbarPos("blur", "image")

        img_prepro = preprocess_img(img)
        check_parking_space(img, img_prepro, pos_list)

        cv2.imshow("Car Park", img)

        key = cv2.waitKey(10)
        if key == ord("q"):
            break
