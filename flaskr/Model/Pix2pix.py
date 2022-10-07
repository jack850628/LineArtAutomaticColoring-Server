from keras.models import load_model
from tensorflow.keras.preprocessing.image import  img_to_array, array_to_img
from PIL import Image
import tensorflow as tf
import numpy as np
import base64, io

model = load_model('./flaskr/checkpoint/油creater.h5')

def png2jpg(image):

    # Create black background
    color = (0, 0, 0, 255)  # the last value is alpha
    bg = Image.new("RGBA", image.size, color)

    # Composite
    composited = Image.alpha_composite(bg, image)
    composited = composited.convert("RGB")

    return composited

def imgResize(img, imageSize=256):
    if img.size[0] > img.size[1]:
        newHeight = int(img.size[1] * imageSize / img.size[0])
        nimg = img.resize((imageSize, newHeight))
    else:
        newWidth = int(img.size[0] * imageSize / img.size[1])
        nimg = img.resize((newWidth, imageSize))
    
    nimg2 = Image.new(nimg.mode, (imageSize, imageSize), (255, 255, 255))
    if(nimg.size[0] > nimg.size[1]):
        nimg2.paste(nimg, (0, (imageSize - nimg.size[1]) // 2))
    else:
        nimg2.paste(nimg, ((imageSize - nimg.size[0]) // 2, 0))
    return nimg2

def create(str):
    str = str.split(',')[1]
    str = base64.b64decode(str)
    buf = io.BytesIO(str)
    image = Image.open(buf)
    # image.convert('RGB').save('./flaskr/checkpoint/test.jpg')
    image = imgResize(image)
    # image = png2jpg(image)
    image = img_to_array(image)
    image = (image / 127.5) - 1
    image = tf.cast(image, tf.float32)
    image = model(np.array([image]), training=True)
    image = array_to_img(image[0])
    output_buffer = io.BytesIO()
    image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    return base64.b64encode(byte_data)

