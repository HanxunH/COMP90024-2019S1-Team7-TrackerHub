import numpy as np
import cv2
import os

# REMOVE THIS FILE FROM ALL DIRS
TARGET_IMAGE_FILE_PATH = '/Users/hanxunhuang/Data/nsfw_processed/sexy/0A18yhC.jpg'
TARGET_DIR = '/Users/hanxunhuang/Data/nsfw_processed'
original = cv2.imread(TARGET_IMAGE_FILE_PATH)

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

for id_name in os.listdir(TARGET_DIR):
    if id_name.startswith('.'):
        continue
    id_dir_path = TARGET_DIR + '/' + id_name
    id_same_file_count = 0
    for image_file in os.listdir(id_dir_path):
        if image_file.startswith('.'):
            continue
        image_file_path = id_dir_path + '/' + image_file
        target = cv2.imread(image_file_path)
        # print(image_file_path)
        try:
            if target is None or mse(target, original) == 0:
                id_same_file_count = id_same_file_count + 1
                os.remove(image_file_path)
                # print('Remove Duplicate Content: %s' % (image_file_path))
        except Exception as e:
            print(image_file_path)
            print(e)
    print('%d removed in %s' % (id_same_file_count, id_dir_path))
