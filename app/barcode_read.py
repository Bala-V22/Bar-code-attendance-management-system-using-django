from pyzbar.pyzbar import decode
import cv2

def decode():
    img = cv2.imread('new_code1.png')
    result = decode(img)
    for i in result:
        print(i.data.decode("utf-8"))
# print(result)