'''
Function:
    Implementation of utils, e.g., setrandomseed
Author:
    Zhenchao Jin
'''
import torch
import random
import numpy as np


'''setrandomseed'''
def setrandomseed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)