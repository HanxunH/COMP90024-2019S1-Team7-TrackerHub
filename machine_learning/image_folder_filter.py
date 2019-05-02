from mpi4py import MPI

import numpy as np
import cv2
import os
from PIL import Image

# REMOVE THIS FILE FROM ALL DIRS
TARGET_IMAGE_FILE_PATH = '/Users/hanxunhuang/Data/nsfw/sexy/0A18yhC.jpg'
TARGET_DIR = '/Users/hanxunhuang/Data/comp90024_p2_nsfw_v3/train'
original = cv2.imread(TARGET_IMAGE_FILE_PATH)
target_image_size = 256

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

# Helper Function that resize image to 256, add black padding
def reformat_Image(ImageFilePath):
    image = Image.open(ImageFilePath, 'r')
    image_size = image.size
    width = image_size[0]
    height = image_size[1]

    if(width != height):
        bigside = width if width > height else height
        background = Image.new('RGB', (bigside, bigside), (0, 0, 0))
        offset = (int(round(((bigside - width) / 2), 0)), int(round(((bigside - height) / 2),0)))
        background.paste(image, offset)
        img = background
        # print("%s has been resized to %s" % (ImageFilePath, str(background.size)))
    else:
        img = image
        # print("%s is already a square, it has not been resized !" % (ImageFilePath))

    img = img.resize((target_image_size, target_image_size))
    # print("%s has been resized to %s" % (ImageFilePath, str(img.size)))
    return img

# Check Image Files
def check_files_larger_than_required(image_file_path):
	image = Image.open(image_file_path, 'r')
	if image.size[0] < target_image_size or image.size[1] < target_image_size:
		print('Original Image Size: %s, %s' % (str(image.size), image_file_path))
		image = reformat_Image(image_file_path)
		image.save(image_file_path)
		print('New Image Size: %s, %s' % (str(image.size), image_file_path))


def compare_image(image_file_path):
	target = cv2.imread(image_file_path)
	if target is None:
		os.remove(image_file_path)
		print('Image Cannot open removed!: %s' %(image_file_path))
		return
	if target.size != original.size:
		return

	try:
		if target is None or mse(target, original) == 0:
			os.remove(image_file_path)
			print('Remove Duplicate Content: %s' % (image_file_path))
	except Exception as e:
		# x = 1
		# print(image_file_path)
		return
	return




comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
	image_path_list = []
	for id_name in os.listdir(TARGET_DIR):
		if id_name.startswith('.'):
			continue
		id_dir_path = TARGET_DIR + '/' + id_name
		print('id_dir_path: %s' % (id_dir_path))
		image_files = os.listdir(id_dir_path)
		for image_file in image_files:
			image_path_list.append(id_dir_path + '/' + image_file)
			# print(id_dir_path + '/' + image_file)

	print(len(image_path_list))
	chunks = [[] for _ in range(size)]
	for i, chunk in enumerate(image_path_list):
		chunks[i % size].append(chunk)
else:
	chunks = None
	image_path_list = None

image_path_list = comm.scatter(chunks, root=0)
print('recv %d' % (len(image_path_list)))

for image_file_path in image_path_list:
	if image_file_path.startswith('.'):
		continue
	# compare_image(image_file_path)
	check_files_larger_than_required(image_file_path)
