# @Author: Hanxun Huang <hanxunhuang>
# @Date:   2019-04-18T21:17:43+10:00
# @Email:  hanxunh@student.unimelb.edu.au
# @Filename: coconut_inference.py
# @Last modified by:   hanxunhuang
# @Last modified time: 2019-05-04T18:45:50+10:00

import torch
import torch.nn as nn
import model
import requests
from torchvision import transforms
from PIL import Image
from io import BytesIO

class coconut_inference():
    def __init__(self, model_checkpoint_file_path=None, cpu_mode=True):
        self.model_checkpoint_file_path = model_checkpoint_file_path
        self.cpu_mode = cpu_mode
        self.load_model()
        self.target_image_size = 256
        return

    def load_model(self):
        self.checkpoint = torch.load(self.model_checkpoint_file_path, map_location=lambda storage, loc: storage)
        self.model_args = self.checkpoint['args']

        self.num_classes = None
        if self.model_args.model_type == 'food179':
            self.num_classes = 179
        elif self.model_args.model_type == 'nsfw':
            self.num_classes = 5
        else:
            raise('Not Implemented!')

        if self.model_args.model_arc == 'resnet18':
            self.model = model.resnet18(num_classes=self.num_classes, zero_init_residual=True)
        elif self.model_args.model_arc == 'resnet34':
            self.model = model.resnet34(num_classes=self.num_classes, zero_init_residual=True)
        elif self.model_args.model_arc == 'resnet50':
            self.model = model.resnet50(num_classes=self.num_classes, zero_init_residual=True)
        elif self.model_args.model_arc == 'resnet101':
            self.model = model.resnet101(num_classes=self.num_classes, zero_init_residual=True)
        elif self.model_args.model_arc == 'resnet152':
            self.model = model.resnet152(num_classes=self.num_classes, zero_init_residual=True)
        elif self.model_args.model_arc == 'mobilenet':
            self.model = model.MobileNetV2(n_class=self.num_classes, input_size=256)
        else:
            raise('Not Implemented!')

        self.model = nn.DataParallel(self.model)
        self.model.load_state_dict(self.checkpoint['model_state_dict'])
        self.model_epoch = self.checkpoint['epoch']
        self.model_test_acc = self.checkpoint['test_acc']
        self.model_best_acc = self.checkpoint['best_acc']
        self.model_test_acc_top5 = self.checkpoint['test_acc_top5']
        self.model_class_to_idx = self.checkpoint['class_to_idx']
        self.model_idx_to_class = {v: k for k, v in self.model_class_to_idx.items()}
        self.model_train_history_dict = self.checkpoint['train_history_dict']
        self.mean = self.checkpoint['NORM_MEAN']
        self.std = self.checkpoint['NORM_STD']
        self.model.eval()

        return

    def print_model_details(self):
        display = 'model_arc: ' + self.model_args.model_arc + \
                  '\nmodel_type: ' + self.model_args.model_type + \
                  '\ntrain_optimizer: ' + self.model_args.train_optimizer + \
                  '\ntest_acc: %.4f' % (self.model_test_acc) + \
                  '\tbest_acc: %.4f' % (self.model_best_acc) + \
                  '\ttest_acc_top5: %.4f' % (self.model_test_acc_top5) + '\n'
        print(display)
        return

    def reformat_Image(self, image_file_path, is_url_image=False):
        if is_url_image:
            response = requests.get(image_file_path)
            image = Image.open(BytesIO(response.content))
        else:
            image = Image.open(image_file_path, 'r')
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

        img = img.resize((self.target_image_size, self.target_image_size))
        # print("%s has been resized to %s" % (ImageFilePath, str(img.size)))
        return img

    def load_image(self, image_path=None, is_url_image=False):
        image = self.reformat_Image(image_path, is_url_image=is_url_image)
        normalize = transforms.Normalize(mean=self.mean, std=self.std)
        loader = transforms.Compose([transforms.ToTensor(), normalize])
        image = loader(image).float()
        image = torch.autograd.Variable(image, requires_grad=True)
        image = image.unsqueeze(0)
        return image

    def inference(self, image_path=None, num_of_perdict=1, is_url_image=False):
        if image_path == None:
            raise("Image does not exist!")
        target_image = self.load_image(image_path, is_url_image=is_url_image)
        pred = self.model(target_image)
        softmax = torch.nn.Softmax(dim=1)
        probabilities = softmax(pred)

        predicts = probabilities.topk(num_of_perdict)
        score_list, class_id_list = predicts
        score_list = score_list.tolist()[0]
        class_id_list = class_id_list.tolist()[0]
        # print(torch.max(pred, 1)[1])
        rs = []
        for index in range(len(score_list)):
            score = score_list[index]
            class_id = class_id_list[index]
            # print(self.model_idx_to_class[class_id], class_id, score)
            rs.append((self.model_idx_to_class[class_id], score, class_id))

        return rs


# coconut = coconut_inference(model_checkpoint_file_path='checkpoints/nsfw_resnet101_adabound.pth_best.pth')
# coconut.print_model_details()
# rs = coconut.inference(image_path='http://pbs.twimg.com/media/D5PeSHgU0AAzy_G.jpg', num_of_perdict=5, is_url_image=True)
# for item in rs:
#     print(item)

# for i, item in enumerate(coconut.model_idx_to_class):
#     print(coconut.model_idx_to_class[item])
