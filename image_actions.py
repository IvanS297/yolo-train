import cv2


def resize_img(scl_percent, input_img):
    width = int(input_img.shape[1] * scl_percent / 100)
    height = int(input_img.shape[0] * scl_percent / 100)
    dimension = (width, height)
    resize_image = cv2.resize(input_img, dimension, interpolation=cv2.INTER_AREA)
    return resize_image


def img_to_gray(input_img, a, b):
    input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (a, b))
    bg = cv2.morphologyEx(input_img, cv2.MORPH_DILATE, se)
    out_gray = cv2.divide(input_img, bg, scale=255)
    return out_gray


def img_to_binary(input_img, thresh, bright):
    gray = img_to_gray(input_img=input_img, a=8, b=8)
    out_binary = cv2.threshold(gray, thresh, bright, cv2.THRESH_OTSU)[1]
    return out_binary