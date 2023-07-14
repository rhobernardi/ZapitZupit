import sys
import cv2
import pytesseract
import numpy as np
from log import log
from logging import ERROR, WARNING
from PIL import Image, ImageFilter, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r'/bin/tesseract'

def read_image(img_path: str):
    phone_numbers = str(pytesseract.image_to_string(Image.open(img_path)))
    if len(phone_numbers) == 0:
        return None
    return

def enhance_image(img_path: str):
    log(f"Begining image improvement", funcname=enhance_image.__name__)
    image = cv2.imread(img_path)

    # config new scale
    scale_percent = 300 # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image and save
    scaled_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    log(f"Image rescaled to {scale_percent}%", funcname=enhance_image.__name__)
    try:
        log(f"Saving rescaled image...", funcname=enhance_image.__name__)
        file = "./img/bin.png"
        cv2.imwrite(file, scaled_image)
        log(f"Done", funcname=enhance_image.__name__)
    except:
        log(f"Fail to save rescaled image", funcname=enhance_image.__name__, type=ERROR)
        return None

    # open as Pillow image to enhance, save and return
    log(f"Opening new image to enhance...", funcname=enhance_image.__name__)
    new_img = Image.open(file)
    new_img = new_img.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(new_img)
    new_img = enhancer.enhance(2)
    log(f"Done", funcname=enhance_image.__name__)
    try:
        new_img.save(file)
        log(f"Image enhanced was saved successfully", funcname=enhance_image.__name__)
    except:
        log(f"Could not save enhanced image", funcname=enhance_image.__name__, type=WARNING)
    return new_img

if __name__ == "__main__":
    img_path = sys.argv[1]
    read_image(img_path)