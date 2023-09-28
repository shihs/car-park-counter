import cv2
import cvzone

CAR_PARK_IMG_FNAME = "example_image.png"
CAR_PARK_VIDEO_FNAME = "carPark.mp4"
CAR_PARK_POS_FNAME = "car_park_pos"

# 一個車位的長&寬
WIDTH, HEIGHT = 104, 45

GREEN = (10, 215, 0)
RED = (255, 0, 255)
TEXT_COLOR = (0, 0, 0)


def draw_rectangle(img, start_point, color, thickness=2):
    x, y = start_point
    cv2.rectangle(
        img, (x, y), (x+WIDTH, y+HEIGHT), color, thickness)


def write_text(img, text, pos, color=TEXT_COLOR, scale=1, thickness=2, offset=10):
    cvzone.putTextRect(img, text,
                       pos,
                       font=cv2.FONT_HERSHEY_SIMPLEX,
                       colorR=color,
                       scale=scale,
                       thickness=thickness,
                       offset=offset)
