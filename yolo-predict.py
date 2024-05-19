import time
import image_actions
import serial_control
import os
import cv2
import threading
from ultralytics import YOLO

serial_control.serialSend(data=[1, 105])

MODEL_PATH = "src/models/trained/lego_model.pt"
model = YOLO(model=MODEL_PATH)

PHOTO_COUNTER = 0
SCALE_PERCENT = 50
IMG_WIDTH = 400
IMG_HEIGHT = 460
DIV_NUM = 0
thread_list = []

capture = cv2.VideoCapture(0)


def start_threads(static_thread_list):
    for thread_name in static_thread_list:
        thread_name.start()


def main_loop():
    photo_counter = 0
    while True:
        success, img = capture.read()
        img = img[DIV_NUM:IMG_HEIGHT, DIV_NUM:IMG_WIDTH]
        img = image_actions.img_to_binary(input_img=img, thresh=255, bright=255)
        resized_image = image_actions.resize_img(scl_percent=SCALE_PERCENT, input_img=img)
        cv2.imshow("", resized_image)
        k = cv2.waitKey(1) & 0xFF
        if k == ord("p"):
            cv2.imwrite("img.png", resized_image)
            photo_counter += 1
            print(f"Снимок №{photo_counter}")
            results = model("img.png")
            for result in results:
                class_ids = result.boxes.cls
                class_names = [model.names[int(cls_id)] for cls_id in class_ids]
                serial_control.rotate(data=str(class_names))
                time.sleep(5.5)
                serial_control.serialSend(data=[0, 255])
            os.remove("img.png")

        if k == ord("q"):
            break


thread_serial = threading.Thread(target=serial_control.onRead)
main_thread = threading.Thread(target=main_loop)
thread_list.append(main_thread)
thread_list.append(thread_serial)

if __name__ == "__main__":
    start_threads(static_thread_list=thread_list)
    main_thread.join()
    thread_serial.join()
    capture.release()
    cv2.destroyAllWindows()
    serial_control.ClosePort()