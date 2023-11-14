import tensorflow as tf
import cv2
import numpy as np
import os
import sys
import requests

VALID_CHAR = '2345678abcdefghkmnprwxy'
VALID_SIZE = 5
url_personal = "http://tracuunnt.gdt.gov.vn/tcnnt/mstcn.jsp"

# Solves Convolution CuDNN error
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

def decode_image(bytes_string):
    """Decode the captcha images from bytes string and extract the alpha channel"""
    img = cv2.imdecode(np.frombuffer(bytes_string, np.uint8),-1)
    img = img[:,:,-1]
    return img

def remove_grid(image):
    """Remove grid from captcha using MORPH_OPEN in cv2

    Args:
        image (cv2_image): valid 2D image array

    Returns:
        image: image after removing grid
    """
    kernel = np.full((3,3), 127, np.uint8)
    image[-2:] = 0
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def trim_border(image,pad=1):
    """Trim all zero pixel around captcha. Useful after calling remove_grid
    to simplify image structure

    Args:
        image (array): valid 2D image array
        pad (int, optional): add zero-pixel border around the image. Defaults to 1.

    Returns:
        image: image after trim and pad
    """
    column = np.nonzero(image.sum(axis=0))[0]
    left = column.min()-pad
    right = column.max()+1+pad
    row = np.nonzero(image.sum(axis=1))[0]
    top = row.min()-pad
    bottom = row.max()+1+pad
    return image[top:bottom,left:right]

def preprocess_raw_image(cv2_image, pad=1):
    """Standardize captcha image by consecutively apply remove_grid then trim

    Args:
        cv2_image (2D-array): 2D-array of image. Be careful with how cv2 and numpy treats array
        pad (int, optional): add zero-pixel border around the image. Defaults to 1.

    Returns:
        np.array: numpy array of image
    """
    image = cv2_image
    image = remove_grid(image)
    image = trim_border(image, pad)
    image = np.array(image)
    return image

def resize_then_pad(image, height, width):
    img_h, img_w = image.shape
    ratio = min(height / img_h, width / img_w)
    new_img = cv2.resize(image, (int(img_w*ratio), int(img_h*ratio)))
    new_img_h, new_img_w = new_img.shape
    delta_h = height - new_img_h
    delta_w = width - new_img_w
    top = delta_h // 2
    bottom = delta_h - top
    left = delta_w //2
    right = delta_w - left
    new_img = cv2.copyMakeBorder(new_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0)
    return new_img

def image_to_list(image):
    """convert and reshape into correct shape (bs,height,width,channel) and return as native Python list"""
    img = np.array(image)
    img = np.expand_dims(img, 0)
    img = np.expand_dims(img, -1)
    return img.tolist()

def preprocess_image(raw_input):
    img = decode_image(raw_input)
    img = preprocess_raw_image(img)
    img = resize_then_pad(img, 64, 128)
    img = image_to_list(img)
    return img

def show_wait_destroy(winname, img):
    cv2.imshow(winname, img)
    cv2.moveWindow(winname, 500, 0)
    cv2.waitKey(0)
    # cv.destroyWindow(winname)

def array_to_label(array, trans_char=VALID_CHAR):
        """reverse from one-hot coded array to label

            Args:
                array (np.array): one-hot coded array
                trans_char (iterable, optional): translation dictionary. Defaults to VALID_CHAR.

            Returns:
                [type]: [description]
        """
        label_vector = np.argmax(array, axis=-1)
        result = []
        for vector in label_vector:
            result.append(trans_char[vector])
        return result

# if __name__ == '__main__':
#     current_path = os.path.dirname(os.path.abspath(__file__))
#     raw_input = os.path.join(current_path, "captcha.png")
#     with open(raw_input, "rb") as image:
#         f = image.read()
#     image = preprocess_image(f)
#     with tf.compat.v1.Session(graph=tf.Graph()) as sess:
#         tf.compat.v1.saved_model.loader.load(sess, [tf.compat.v1.saved_model.tag_constants.SERVING], '../model/CNN5_v10_acc_98_tf220_ubuntu2204/1')
#         graph = tf.compat.v1.get_default_graph()
#         y_pred = sess.run('StatefulPartitionedCall:0', feed_dict={'serving_default_input_1:0': image})
#         print(''.join(array_to_label(np.array(y_pred[0]))))

class SolverManager():
    def __init__(self):
        super().__init__()
    
    def predict(self, raw_input):
        current_path, _ = os.path.split(os.path.abspath(__file__))
        image = preprocess_image(raw_input)
        with tf.compat.v1.Session(graph=tf.Graph()) as sess:
            tf.compat.v1.saved_model.loader.load(sess, [tf.compat.v1.saved_model.tag_constants.SERVING], os.path.join(current_path,'model/CNN5_v10_acc_98_tf220_ubuntu2204/1'))
            graph = tf.compat.v1.get_default_graph()
            y_pred = sess.run('StatefulPartitionedCall:0', feed_dict={'serving_default_input_1:0': image})
            
        return ''.join(array_to_label(np.array(y_pred[0])))




