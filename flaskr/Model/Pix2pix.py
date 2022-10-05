from keras.models import load_model
from tensorflow.keras.preprocessing.image import  img_to_array, array_to_img
from PIL import Image

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

def create(str):
    str = str.split(',')[1]
    str = base64.b64decode(str)
    buf = io.BytesIO(str)
    image = Image.open(buf)
    image = png2jpg(image)
    image = img_to_array(image)
    image = model(np.array([image]), training=True)
    image = array_to_img(image[0])
    output_buffer = io.BytesIO()
    image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    return base64.b64encode(byte_data)

