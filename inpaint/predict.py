# import matplotlib.pyplot as plt
import random
from PIL import Image
import gc
import os
import cv2
import glob
import socket
import tensorflow as tf
from .inpaint_model import *

height = 256
width = 256
model_path = 'inpaint/models/places2.ckpt-6666'


def infer(batch_data, mask, reuse=False):
    shape = batch_data.get_shape().as_list()
    batch_gt = batch_data / 127.5 - 1.
    batch_incomplete = batch_gt * mask

    image_p1, image_p2 = RW_generator(batch_incomplete, mask, reuse=reuse)

    image_c2 = batch_incomplete * mask + image_p2 * (1. - mask)
    image_c2 = (image_c2 + 1.) * 127.5
    return image_c2


images = tf.placeholder(tf.float32, [1, height, width, 3], name='image')
mask = tf.placeholder(tf.float32, [1, height, width, 1], name='mask')
sess = tf.Session()
inpainting_result = infer(images, mask)
saver_pre = tf.train.Saver()
init_op = tf.group(tf.initialize_all_variables(), tf.initialize_local_variables())
sess.run(init_op)
saver_pre.restore(sess, model_path)


def run_fill(file_test, file_mask):
    test_mask = cv2.resize(cv2.imread(file_mask), (height, width))
    test_mask = test_mask[:, :, 0:1]
    test_mask = 0. + test_mask // 255
    test_mask[test_mask >= 0.5] = 1
    test_mask[test_mask < 0.5] = 0
    test_mask = 1 - test_mask
    test_image = cv2.imread(file_test)[..., ::-1]
    test_image = cv2.resize(test_image, (height, width))
    test_mask = np.expand_dims(test_mask, 0)
    test_image = np.expand_dims(test_image, 0)
    img_out = sess.run(inpainting_result, feed_dict={mask: test_mask, images: test_image})

    # cv2.imwrite(file_output, img_out[0][..., ::-1])
    return img_out[0][..., ::-1]
