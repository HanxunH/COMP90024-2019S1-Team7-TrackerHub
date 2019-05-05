# @Author: Hanxun Huang <hanxunhuang>
# @Date:   2019-04-16T14:07:27+10:00
# @Email:  hanxunh@student.unimelb.edu.au
# @Filename: build_image_folder.py
# @Last modified by:   hanxunhuang
# @Last modified time: 2019-05-03T23:39:47+10:00



import os
import random
import pathlib
import shutil
import cv2
import numpy as np
from PIL import Image
from glob import glob

FROM_TARGET_DIR = '/Users/hanxunhuang/Data/nsfw'
PROCESS_DIR = '/Users/hanxunhuang/Data/food179/images'
TO_TARGET_DIR = '/Users/hanxunhuang/Data/comp90024_p2_food179_v3'
CHANNEL_NUM = 3
TEST_PERCENTAGE = 0.2
target_image_size = 256

# Update datasets
def update_nsfw():
    source_path = "/Users/hanxunhuang/Downloads/Chrome/test"
    image_file_path_list = []
    # for id in os.listdir(source_path):
    #     id_path = source_path + '/' + id
    for image_name in os.listdir(source_path):
        image_file_path = source_path + '/' + image_name
        image_file_path_list.append(image_file_path)

    test_count = 0
    train_file_path_list = []
    test_file_path_list = []

    while test_count < len(image_file_path_list) * TEST_PERCENTAGE:
        target_file_index = random.randint(0, len(image_file_path_list)-1)
        target_file_path = image_file_path_list[target_file_index]
        if target_file_path not in test_file_path_list:
            test_file_path_list.append(target_file_path)
            test_count = test_count + 1

    target_test_dir = '/Users/hanxunhuang/Data/comp90024_p2_nsfw_v3/test/neutral'
    target_train_dir = '/Users/hanxunhuang/Data/comp90024_p2_nsfw_v3/train/neutral'

    train_file_path_list = [item for item in image_file_path_list if item not in test_file_path_list]
    print(len(train_file_path_list)+ len(test_file_path_list))
    print(len(image_file_path_list))

    move_list_of_file_to_dir(train_file_path_list, target_train_dir)
    move_list_of_file_to_dir(test_file_path_list, target_test_dir)
    return

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
        print("%s has been resized to %s" % (ImageFilePath, str(background.size)))
    else:
        img = image
        print("%s is already a square, it has not been resized !" % (ImageFilePath))

    img = img.resize((target_image_size, target_image_size))
    print("%s has been resized to %s" % (ImageFilePath, str(img.size)))
    return img


# Helper Function calculate mean std
def cal_dir_stat(root):
    cls_dirs = [d for d in os.listdir(root) if os.listdir(os.path.join(root, d))]
    pixel_num = 0   # store all pixel number in the dataset
    channel_sum = np.zeros(CHANNEL_NUM)
    channel_sum_squared = np.zeros(CHANNEL_NUM)

    for idx, d in enumerate(cls_dirs):
        print("#{} class".format(idx))
        im_pths = glob(os.path.join(root, d, "*.jpg"))

        for path in im_pths:
            im = cv2.imread(path)   # image in M*N*CHANNEL_NUM shape, channel in BGR order
            im = im/255.0
            pixel_num += (im.size/CHANNEL_NUM)
            channel_sum += np.sum(im, axis=(0, 1))
            channel_sum_squared += np.sum(np.square(im), axis=(0, 1))

    bgr_mean = channel_sum / pixel_num
    bgr_std = np.sqrt(channel_sum_squared / pixel_num - np.square(bgr_mean))

    # change the format from bgr to rgb
    rgb_mean = list(bgr_mean)[::-1]
    rgb_std = list(bgr_std)[::-1]

    return rgb_mean, rgb_std


def process_files():
    print("-" * 80)
    print("Navigating to "+FROM_TARGET_DIR)
    id_path_list = []
    for item in os.listdir(FROM_TARGET_DIR):
        if item.startswith('.'):
            continue
        id_path_list.append(item)
    print('Total of %d class' % (len(id_path_list)))

    for id_folder in id_path_list:
        original_id_path = FROM_TARGET_DIR + '/' + id_folder
        processed_id_path = PROCESS_DIR + '/' + id_folder
        pathlib.Path(processed_id_path).mkdir(parents=True, exist_ok=True)
        for image_name in os.listdir(original_id_path):
            if image_name.startswith('.'):
                continue
            original_image_file_path = original_id_path + '/' + image_name
            processed_image_file_path = processed_id_path + '/' + image_name
            try:
                new_image = reformat_Image(original_image_file_path)
                if new_image.size[0] != target_image_size or new_image.size[1] != target_image_size:
                    raise('Inconsistent Size!')
                new_image.save(processed_image_file_path)
            except Exception as error:
                print(error)
                os.remove(original_image_file_path)
                print("%s Removed!" % (original_image_file_path))
                continue

    # validations
    # print("-" * 80)
    # for id_folder in id_path_list:
    #     original_id_path = FROM_TARGET_DIR + '/' + id_folder
    #     processed_id_path = PROCESS_DIR + '/' + id_folder
    #     for image_name in os.listdir(original_id_path):
    #         if not image_name.startswith('.') and image_name not in os.listdir(processed_id_path):
    #             print(original_id_path + '/' + image_name)
    #             raise('After Process Inconsistent image!')
    print('Valid!')


def move_list_of_file_to_dir(file_path_list, dir_path):
    print('Move %d files to %s' % (len(file_path_list), dir_path))
    for item in file_path_list:
        shutil.copy2(item, dir_path)
    return


def build_image_foler():
    print("-" * 80)
    print("Navigating to "+PROCESS_DIR)
    id_name_list = []
    for item in os.listdir(PROCESS_DIR):
        if item.startswith('.'):
            continue
        id_name_list.append(item)
    print('Total of %d class' % (len(id_name_list)))

    image_folder_train_path = TO_TARGET_DIR + '/' + 'train'
    image_folder_test_path = TO_TARGET_DIR + '/' + 'test'
    pathlib.Path(image_folder_train_path).mkdir(parents=True, exist_ok=True)
    pathlib.Path(image_folder_test_path).mkdir(parents=True, exist_ok=True)

    for id_name in id_name_list:
        image_path_list = []
        id_path = PROCESS_DIR + '/' + id_name
        for image_name in os.listdir(id_path):
            if item.startswith('.'):
                continue
            image_file_path = id_path + '/' + image_name
            image_path_list.append(image_file_path)

        test_image_path_list = []
        train_image_path_list = []

        # Select test images
        test_image_file_threshold = len(image_path_list) * TEST_PERCENTAGE
        while True:
            target_file_index = random.randint(0, len(image_path_list)-1)
            target_file_path = image_path_list[target_file_index]
            if not os.path.exists(target_file_path):
                raise Exception('target dir does not exist')
            if target_file_path not in test_image_path_list:
                test_image_path_list.append(target_file_path)
            if len(test_image_path_list) >= test_image_file_threshold:
                break

        # Select Train Images
        for image_file_path in image_path_list:
            if image_file_path not in test_image_path_list:
                train_image_path_list.append(image_file_path)

        # Move Files
        image_folder_train_path_id = image_folder_train_path + '/' + id_name
        image_folder_test_path_id = image_folder_test_path + '/' + id_name
        pathlib.Path(image_folder_train_path_id).mkdir(parents=True, exist_ok=True)
        pathlib.Path(image_folder_test_path_id).mkdir(parents=True, exist_ok=True)
        move_list_of_file_to_dir(train_image_path_list, image_folder_train_path_id)
        move_list_of_file_to_dir(test_image_path_list, image_folder_test_path_id)

    print('-' * 20 + 'Validations' + '-' * 20)
    for id_name in id_name_list:
        original_id_path = PROCESS_DIR + '/' + id_name
        new_id_train_path = image_folder_train_path + '/' + id_name
        new_id_test_path = image_folder_test_path + '/' + id_name
        original_image_file_list = []
        new_id_train_image_file_list = []
        new_id_test_image_file_list = []

        for image_file in os.listdir(original_id_path):
            if item.startswith('.'):
                continue
            original_image_file_list.append(image_file)

        for image_file in os.listdir(new_id_train_path):
            if item.startswith('.'):
                continue
            new_id_train_image_file_list.append(image_file)

        for image_file in os.listdir(new_id_test_path):
            if item.startswith('.'):
                continue
            new_id_test_image_file_list.append(image_file)

        if len(original_image_file_list) != (len(new_id_train_image_file_list) + len(new_id_test_image_file_list)):
            print('id: %s, original: %d, train: %d, test: %d' %(id_name, len(original_image_file_list), len(new_id_train_image_file_list), len(new_id_test_image_file_list)))
            # raise('In Inconsistent number of files!')

        for image_file in original_image_file_list:
            if image_file not in new_id_train_image_file_list and image_file not in new_id_test_image_file_list:
                print(original_id_path + '/' + image_file)
                raise('File not found!')
    print('Valid!')
    return


def main():
    # process_files()
    build_image_foler()
    # update_nsfw()
    # rgb_mean, rgb_std = cal_dir_stat(root=PROCESS_DIR)
    # print('rgb_mean: %s' % (str(rgb_mean)))
    # print('rgb_std: %s' % (str(rgb_std)))

    return

if __name__ == '__main__':
    main()

# Food179 Mean [0.48369651859332485, 0.39450415872995226, 0.30613956430808564]
# Food179 STD [0.31260642838369135, 0.29686785305034863, 0.28606165329199507]
# NSFW    Mean [0.4192032458303017, 0.3620132191886713, 0.3345888229001102]
# NSFW    STD [0.36833108995020036, 0.33885012952633026, 0.32902284057603554]
