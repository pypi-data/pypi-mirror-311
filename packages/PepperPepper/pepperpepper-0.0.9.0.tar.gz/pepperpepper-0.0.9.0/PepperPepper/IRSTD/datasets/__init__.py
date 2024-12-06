# 数据集处理模块，要求数据合适如下所示：
'''
├──./datasets/
│    ├── NUDT-SIRST/ & IRSTD-1k/ & sirst_aug/
│    │    ├── images
│    │    │    ├── 000002.png
│    │    │    ├── 000004.png
│    │    │    ├── ...
│    │    ├── masks
│    │    │    ├── 000002.png
│    │    │    ├── 000004.png
│    │    │    ├── ...
│    │    ├── test.txt/val.txt/train.txt
│    │    │    ├── 000004
│    │    │    ├── ...
'''


from .datasets import Dataset, load_datasets



__all__ = ['Dataset',
           'load_datasets'
           ]