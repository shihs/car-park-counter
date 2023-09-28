import os
import pickle

import cv2

import utils


def mouse_click(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x, y))

    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(pos_list):
            x1, y1 = pos
            if x1 < x < x1+utils.WIDTH and y1 < y < y1+utils.HEIGHT:
                pos_list.pop(i)

    with open(CAR_PARK_POS_PATH, "wb") as f:
        pickle.dump(pos_list, f)


if __name__ == "__main__":

    root_dirname = os.path.dirname(os.path.dirname(__file__))
    IMG_FILE_PATH = f"{root_dirname}/data/{utils.CAR_PARK_IMG_FNAME}"
    CAR_PARK_POS_PATH = f"{root_dirname}/data/{utils.CAR_PARK_POS_FNAME}"

    try:
        with open(CAR_PARK_POS_PATH, "rb") as f:
            pos_list = pickle.load(f)
    except:
        pos_list = []

    while True:
        img = cv2.imread(IMG_FILE_PATH)
        for pos in pos_list:
            utils.draw_rectangle(img=img, start_point=pos, color=utils.RED)

        cv2.imshow("Car Park Image", img)
        cv2.setMouseCallback("Car Park Image", mouse_click)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
