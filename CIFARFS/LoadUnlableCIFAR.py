#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import torch
# from torch.utils.data import Dataset
# from torchvision.transforms import transforms
import numpy as np
import collections
import random


class UnlabData(object):
    def __init__(self, seed=None):
        tinyimg = np.array(np.load("stl_select.npy", allow_pickle=True))

        train_indices = np.arange(500)
        self.train_data = []

        for i in range(64):
            temp_tiny = [tinyimg[i][j] for j in train_indices]
            temp_tiny = np.array(temp_tiny)
            self.train_data.append(DataSubset(temp_tiny))

class DataSubset(object):
    def __init__(self, xs, num_examples=None, seed=None):

        if seed is not None:
            np.random.seed(99)
        self.xs = xs
        self.n = len(xs)
        self.batch_start = 0
        self.cur_order = np.random.permutation(self.n)

    def get_next_batch(self, batch_size, multiple_passes=False, reshuffle_after_pass=True):
        # np.random.seed(99)
        if self.n < batch_size:
            raise ValueError('Batch size can be at most the dataset size')
        if not multiple_passes:
            actual_batch_size = min(batch_size, self.n - self.batch_start)
            if actual_batch_size <= 0:
                raise ValueError('Pass through the dataset is complete.')
            batch_end = self.batch_start + actual_batch_size
            batch_xs = self.xs[self.cur_order[self.batch_start : batch_end], ...]
            self.batch_start += actual_batch_size
            return batch_xs
        actual_batch_size = min(batch_size, self.n - self.batch_start)
        if actual_batch_size < batch_size:
            if reshuffle_after_pass:
                self.cur_order = np.random.permutation(self.n)
            self.batch_start = 0
        batch_end = self.batch_start + batch_size


        batch_xs = self.xs[self.cur_order[self.batch_start : batch_end], ...]
       

        self.batch_start += actual_batch_size
        return batch_xs

    
    



if __name__ == '__main__':
    # the following episode is to view one set of images via tensorboard.
    from torchvision.utils import make_grid
    from matplotlib import pyplot as plt
    from tensorboardX import SummaryWriter
    import time

