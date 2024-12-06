'''
IRSTD1kDataset与NUDTDataset

'''
# from ...environment import torch
# from ...environment import torchvision
#
# from ...environment import PIL
# from ...environment import cv2
# from ...environment import os
#
# from ...environment import random
# from ...environment import np

import torch, cv2, os
import numpy as np
# __all__ = ['Dataset']


def load_datasets(mode = 'train', img_size = 256, data_dir = r'/mnt/e/datasets/IRSTD-1k', batch_size = 8,shuffle = True, transform = None):
    return torch.utils.data.DataLoader(Dataset(mode = mode, img_size = img_size, data_dir = data_dir, transform = transform), batch_size = batch_size, shuffle = shuffle)


class Dataset(torch.utils.data.Dataset):
    '''
    Return: Single channel
    '''

    def __init__(self, data_dir=r'/mnt/e/datasets/IRSTD-1k',
                 mode='train', img_size=256, transform=None):
        assert mode in ['train', 'test', 'val']


        if mode == 'train':
            txtfile = 'train.txt'
        elif mode == 'test':
            txtfile = 'test.txt'
        elif mode == 'val':
            txtfile = 'val.txt'
        else:
            raise NotImplementedError


        list_dir = os.path.join(data_dir, txtfile)
        self.data_dir = data_dir
        self.img_size = img_size
        self.mode = mode
        self.transform = transform

        self.names = []
        with open(list_dir, 'r') as f:
            self.names += [line.strip() for line in f.readlines()]

    def __getitem__(self, i):
        name = self.names[i]
        img_path = os.path.join(self.data_dir, 'images', name+'.png')
        label_path = os.path.join(self.data_dir, 'masks', name+'.png')

        img, mask = cv2.imread(img_path, 0), cv2.imread(label_path, 0)

        img = cv2.resize(img, ( int(self.img_size), int(self.img_size)), interpolation=cv2.INTER_LINEAR)
        mask = cv2.resize(mask, ( int(self.img_size), int(self.img_size)), interpolation=cv2.INTER_NEAREST)



        row, col = img.shape
        img = img.reshape(1, row, col) / 255.

        # print(img.shape, img.dtype)
        # print(self.img_size)
        #
        #
        # img = cv2.resize(img[0], ( int(self.img_size), int(self.img_size)), interpolation=cv2.INTER_LINEAR)
        # mask = cv2.resize(mask[0], ( int(self.img_size), int(self.img_size)), interpolation=cv2.INTER_NEAREST)
        #
        #
        # print(img.shape, img.dtype)


        img = img.reshape(1, self.img_size, self.img_size) / 255.


        if np.max(mask) > 0:
            mask = mask.reshape(1, self.img_size, self.img_size) / np.max(mask)
        else:
            mask = mask.reshape(1, self.img_size, self.img_size)

        img = torch.from_numpy(img).type(torch.FloatTensor)
        mask = torch.from_numpy(mask).type(torch.FloatTensor)

        if self.transform is not None:
            img = self.transform(img)
            mask = self.transform(mask)
        return img, mask

    def __len__(self):
        return len(self.names)



# if __name__ == '__main__':
#     data = Dataset(data_dir=r'/mnt/e/algorithms/IRSTD/dataset/IRSTD-1k',
#                    mode='train', img_size=256, transform=None)
#
#     k = data.__getitem__(0)
















