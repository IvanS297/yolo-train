import shutil
from pathlib import Path

OLD_LABELS_DIRECTORY = Path(r"C:/Users/Ваня/PycharmProjects/Tensorflow/yolo/labels")
NEW_LABELS_DIRECTORY = Path(r"C:/Users/Ваня/PycharmProjects/Tensorflow/yolo/train/key3")

key = ''


for file in OLD_LABELS_DIRECTORY.iterdir():
    extension = str(file)[-4:]
    print("Имя файла: ", file, ", Длинна файла: ", int(len(str(file))), ", Расширение файла: ", extension)
    with open(str(file), 'r') as text:
        data = text.read()
        rect = data[1:]
        key = data[0]
        print("Ключ: ", key, ", Координаты прямоугольника: ", rect)
        text.close()
    if key == '3':
        shutil.move(file, NEW_LABELS_DIRECTORY)

print("Готово!")