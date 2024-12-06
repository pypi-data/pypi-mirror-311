from ...environment import torch

__all__ = ['RPCANet']

'''
RPCANet:是论文 RPCANet: Deep Unfolding RPCA Based Infrared Small Target Detection中提出来，用于红外小目标检测。


Background Estimation Module (BEM)：作者采用BEM模块去评估下一阶段的背景秩，目的是保持并降低背景特征矩阵的低秩性，输入为（D-T）,维度为1到32的映射，最终输出为1

Target Extraction Module (TEM)：作者采用TEM模块去保持目标的稀疏性，



'''

class RPCANet(torch.nn.Module):
    def __init__(self, stage_num=6, slayers=6, llayers=3, mlayers=3, channel=32, mode='train'):
        super(RPCANet, self).__init__()
        self.stage_num = stage_num
        self.decos = torch.nn.ModuleList()
        self.mode = mode
        for _ in range(stage_num):
            self.decos.append(DecompositionModule(slayers=slayers, llayers=llayers,
                                                  mlayers=mlayers, channel=channel))
        # 迭代循环初始化参数
        for m in self.modules():
            # 也可以判断是否为conv2d，使用相应的初始化方式
            if isinstance(m, torch.nn.Conv2d):
                torch.nn.init.xavier_normal_(m.weight)
                #nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, torch.nn.BatchNorm2d):
                torch.nn.init.constant_(m.weight, 1)
                torch.nn.init.constant_(m.bias, 0)

    def forward(self, D):
        T = torch.zeros(D.shape).to(D.device)
        for i in range(self.stage_num):
            D, T = self.decos[i](D, T)
        if self.mode == 'train':
            return D,T
        else:
            return T



class DecompositionModule(torch.nn.Module):
    def __init__(self, slayers=6, llayers=3, mlayers=3, channel=32):
        super(DecompositionModule, self).__init__()
        self.lowrank = LowrankModule(channel=channel, layers=llayers)
        self.sparse = SparseModule(channel=channel, layers=slayers)
        self.merge = MergeModule(channel=channel, layers=mlayers)

    def forward(self, D, T):
        B = self.lowrank(D, T)
        T = self.sparse(D, B, T)
        D = self.merge(B, T)
        return D, T


# BEM
class LowrankModule(torch.nn.Module):
    def __init__(self, channel=32, layers=3):
        super(LowrankModule, self).__init__()

        convs = [torch.nn.Conv2d(1, channel, kernel_size=3, padding=1, stride=1),
                 torch.nn.BatchNorm2d(channel),
                 torch.nn.ReLU(True)]
        for i in range(layers):
            convs.append(torch.nn.Conv2d(channel, channel, kernel_size=3, padding=1, stride=1))
            convs.append(torch.nn.BatchNorm2d(channel))
            convs.append(torch.nn.ReLU(True))
        convs.append(torch.nn.Conv2d(channel, 1, kernel_size=3, padding=1, stride=1))
        self.convs = torch.nn.Sequential(*convs)
        #self.relu = torch.nn.ReLU()
        #self.gamma = torch.nn.Parameter(torch.Tensor([0.01]), requires_grad=True)

    def forward(self, D, T):
        x = D - T
        B = x + self.convs(x)
        return B


# TEM
class SparseModule(torch.nn.Module):
    def __init__(self, channel=32, layers=6) -> object:
        super(SparseModule, self).__init__()
        convs = [torch.nn.Conv2d(1, channel, kernel_size=3, padding=1, stride=1),
                 torch.nn.ReLU(True)]
        for i in range(layers):
            convs.append(torch.nn.Conv2d(channel, channel, kernel_size=3, padding=1, stride=1))
            convs.append(torch.nn.ReLU(True))
        convs.append(torch.nn.Conv2d(channel, 1, kernel_size=3, padding=1, stride=1))
        self.convs = torch.nn.Sequential(*convs)
        self.epsilon = torch.nn.Parameter(torch.Tensor([0.01]), requires_grad=True)

    def forward(self, D, B, T):
        x = T + D - B
        T = x - self.epsilon * self.convs(x)
        return T


class MergeModule(torch.nn.Module):
    def __init__(self, channel=32, layers=3):
        super(MergeModule, self).__init__()
        convs = [torch.nn.Conv2d(1, channel, kernel_size=3, padding=1, stride=1),
                 torch.nn.BatchNorm2d(channel),
                 torch.nn.ReLU(True)]
        for i in range(layers):
            convs.append(torch.nn.Conv2d(channel, channel, kernel_size=3, padding=1, stride=1))
            convs.append(torch.nn.BatchNorm2d(channel))
            convs.append(torch.nn.ReLU(True))
        convs.append(torch.nn.Conv2d(channel, 1, kernel_size=3, padding=1, stride=1))
        self.mapping = torch.nn.Sequential(*convs)

    def forward(self, B, T):
        x = B + T
        D = self.mapping(x)
        return D
