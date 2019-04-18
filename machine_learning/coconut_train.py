# @Author: Hanxun Huang <hanxunhuang>
# @Date:   2019-04-16T23:56:02+10:00
# @Email:  hanxunh@student.unimelb.edu.au
# @Filename: coconut_train.py
# @Last modified by:   hanxunhuang
# @Last modified time: 2019-04-18T21:33:28+10:00


import os
import time
import argparse
import numpy as np
import model
import adabound

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from utils.utils import AverageMeter

parser = argparse.ArgumentParser(description='COMP90024 Project Coconut Train')
parser.add_argument('--cuda', action='store_true')
parser.add_argument('--start_from_begining', action='store_true')
parser.add_argument('--load_gpu_model_on_cpu', action='store_true')
parser.add_argument('--train_data_dir', type=str, default='/data/cephfs/punim0784/comp90024_p2_food_179', help='Has to match with the model')
parser.add_argument('--data_loader_nums_workers', type=int, default=8)
parser.add_argument('--train_batch_size', type=int, default=256)
parser.add_argument('--test_batch_size', type=int, default=512)
parser.add_argument('--train_optimizer', type=str, default='sgd', help='sgd, adam, adabound')
parser.add_argument('--lr', type=float, default='0.01', help='Training Learning Rate')
parser.add_argument('--l2_reg', type=float, default=0.00025)
parser.add_argument('--grad_bound', type=float, default=5.0)
parser.add_argument('--num_epochs', type=int, default=350)
parser.add_argument('--model_type', type=str, default='food179', help='food179, nsfw')
parser.add_argument('--model_arc', type=str, default='resnet50', help='resnet')
parser.add_argument('--model_checkpoint_path', type=str, default='checkpoints/food179_resnet50_sgd.pth')
args = parser.parse_args()


# Static Vars
FOOD179_MEAN = [0.48369651859332485, 0.39450415872995226, 0.30613956430808564]
FOOD179_STD = [0.31260642838369135, 0.29686785305034863, 0.28606165329199507]
NSFW_MEAN = [0.4192032458303017, 0.3620132191886713, 0.3345888229001102]
NSFW_STD = [0.36833108995020036, 0.33885012952633026, 0.32902284057603554]

# Global Vars
NORM_MEAN = None
NORM_STD = None
coconut_model = None
train_history_dict = {}
class_to_idx = None

def load_datasets():
    global NORM_MEAN, NORM_STD, coconut_model, train_history_dict, class_to_idx
    data_loaders = {}
    normalize = transforms.Normalize(mean=NORM_MEAN,
                                     std=NORM_STD)

    train_transform = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        normalize])

    test_transform = transforms.Compose([
        transforms.ToTensor(),
        normalize])

    train_dataset = datasets.ImageFolder(root=args.train_data_dir+'/train', transform=train_transform)
    test_dataset = datasets.ImageFolder(root=args.train_data_dir+'/test', transform=test_transform)

    data_loaders['train_dataset'] = torch.utils.data.DataLoader(dataset=train_dataset,
                                                                batch_size=args.train_batch_size,
                                                                shuffle=True,
                                                                pin_memory=True,
                                                                num_workers=args.data_loader_nums_workers)

    data_loaders['test_dataset'] = torch.utils.data.DataLoader(dataset=test_dataset,
                                                               batch_size=args.test_batch_size,
                                                               shuffle=True,
                                                               pin_memory=True,
                                                               num_workers=args.data_loader_nums_workers)

    class_to_idx = train_dataset.class_to_idx
    print(class_to_idx)
    return data_loaders


def get_eval_accuracy(loader, shared_cnn):

    """Evaluate a given architecture.
    Args:
        loader: A single data loader.
        shared_cnn: CNN that contains all possible architectures, with shared weights.
        sample_arc: The architecture to use for the evaluation.
    Returns:
        acc: Average accuracy.
    """

    shared_cnn.eval()

    total = 0.
    acc_sum = 0.
    for (images, labels) in loader:
        if args.cuda:
            images = images.cuda(non_blocking=True)
            labels = labels.cuda(non_blocking=True)

        with torch.no_grad():
            pred = shared_cnn(images)
        acc_sum += torch.sum((torch.max(pred, 1)[1] == labels).type(torch.float))
        total += pred.shape[0]

    acc = acc_sum / total
    return acc.item()



def train_cnn(epoch=None, model=None, optimizer=None, scheduler=None, data_loaders=None):
    global NORM_MEAN, NORM_STD, coconut_model, train_history_dict, class_to_idx

    model.train()
    train_acc_meter = AverageMeter()
    loss_meter = AverageMeter()
    train_loader = data_loaders['train_dataset']

    for i, (images, labels) in enumerate(train_loader):
        start = time.time()
        if args.cuda:
            images = images.cuda(non_blocking=True)
            labels = labels.cuda(non_blocking=True)

        model.zero_grad()
        pred = model(images)
        loss = nn.CrossEntropyLoss()(pred, labels)
        loss.backward()

        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_bound)
        optimizer.step()

        train_acc = torch.mean((torch.max(pred, 1)[1] == labels).type(torch.float))
        train_acc_meter.update(train_acc.item())
        loss_meter.update(loss.item())

        end = time.time()

        learning_rate = optimizer.param_groups[0]['lr']
        display = 'epoch=' + str(epoch) + \
                  '\tch_step=' + str(i) + \
                  '\tloss=%.5f' % (loss_meter.avg) + \
                  '\tlr=%.5f' % (learning_rate) + \
                  '\t|g|=%.4f' % (grad_norm) + \
                  '\tacc_avg=%.4f' % (train_acc_meter.avg) + \
                  '\ttime=%.2fit/s' % (1. / (end - start))
        print(display)

    train_history_dict[epoch]['train_loss'] = loss_meter.avg
    train_history_dict[epoch]['train_acc'] = train_acc_meter.avg



def train_ops(start_epoch=None, model=None, optimizer=None, scheduler=None, data_loaders=None, best_acc=None):
    global NORM_MEAN, NORM_STD, coconut_model, train_history_dict, class_to_idx

    for epoch in range(start_epoch, args.num_epochs):
        train_history_dict[epoch] = {}
        train_cnn(epoch=epoch,
                  model=model,
                  optimizer=optimizer,
                  data_loaders=data_loaders)
        test_loader = data_loaders['test_dataset']
        test_acc = get_eval_accuracy(loader=test_loader, shared_cnn=model)
        train_history_dict[epoch]['test_acc'] = test_acc

        filename = args.model_checkpoint_path

        if test_acc >= best_acc:
            best_acc = test_acc
            save_mode(epoch=epoch,
                      model=model,
                      optimizer=optimizer,
                      test_acc=test_acc,
                      best_acc=best_acc,
                      filename=filename + '_best.pth')

        save_mode(epoch=epoch,
                  model=model,
                  optimizer=optimizer,
                  test_acc=test_acc,
                  best_acc=best_acc,
                  filename=filename)

        print('Best Acc %5f' % (best_acc))
        print('Eval Acc %5f' % (test_acc))

    return


def save_mode(epoch=None, model=None, optimizer=None, test_acc=None, best_acc=None, filename=None):
    global NORM_MEAN, NORM_STD, coconut_model, train_history_dict, class_to_idx
    state = {'epoch': epoch + 1,
             'args': args,
             'test_acc': test_acc,
             'best_acc': best_acc,
             'class_to_idx': class_to_idx,
             'train_history_dict': train_history_dict,
             'model_state_dict': model.state_dict(),
             'model_optimizer': optimizer.state_dict()}
    torch.save(state, filename)
    print(filename + ' Saved!')
    return


def main():
    global NORM_MEAN, NORM_STD, coconut_model, train_history_dict

    for arg in vars(args):
        print(str(arg) + ': ' + str(getattr(args, arg)))
    print('=' * 100)

    # Build Model base on dataset and arc
    num_classes = None
    if args.model_type == 'food179':
        num_classes = 179
        NORM_MEAN = FOOD179_MEAN
        NORM_STD = FOOD179_STD
    elif args.model_type == 'nsfw':
        num_classes = 5
    else:
        raise('Not Implemented!')

    if args.model_arc == 'resnet50':
        coconut_model = model.resnet50(num_classes=num_classes)
    else:
        raise('Not Implemented!')

    coconut_model = nn.DataParallel(coconut_model)
    if args.cuda:
        coconut_model = coconut_model.cuda()
        torch.backends.benchmark = True
        print("CUDA Enabled")
        print('Total of %d GPU available' % (torch.cuda.device_count()))

    # Build Training
    start_epoch = 0
    best_acc = 0
    optimizer = None
    scheduler = None
    milestones = [50, 150, 250]
    if args.train_optimizer == 'sgd':
        optimizer = optim.SGD(coconut_model.parameters(), lr=args.lr, momentum=0.9, nesterov=True, weight_decay=args.l2_reg)
        scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=milestones, gamma=0.1)
    elif args.train_optimizer == 'adam':
        optimizer = optim.Adam(coconut_model.parameters(), lr=args.lr)
        scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=milestones, gamma=0.1)
    elif args.train_optimizer == 'adabound':
        optimizer = adabound.AdaBound(coconut_model.parameters(), lr=1e-3, final_lr=0.1)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=150, gamma=0.1, last_epoch=-1)

    if not args.start_from_begining:
        filename = args.model_checkpoint_path
        if args.load_gpu_model_on_cpu:
            checkpoint = torch.load(filename, map_location=lambda storage, loc: storage)
        else:
            checkpoint = torch.load(filename)

        coconut_model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['model_optimizer'])
        best_acc = checkpoint['best_acc']
        train_history_dict = checkpoint['train_history_dict']
        scheduler.optimizer = optimizer  # Not sure if this actually works
        start_epoch = checkpoint['epoch']
        print(filename + ' loaded!')

    data_loaders = load_datasets()
    train_ops(start_epoch=start_epoch,
              model=coconut_model,
              optimizer=optimizer,
              data_loaders=data_loaders,
              best_acc=best_acc)

if __name__ == "__main__":
    main()
