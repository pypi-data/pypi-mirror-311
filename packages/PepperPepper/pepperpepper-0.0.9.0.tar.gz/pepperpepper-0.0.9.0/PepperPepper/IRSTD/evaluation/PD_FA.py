from ...environment import np, cv2

'''
因为IRSTD环境中可以看为分割任务，所以上述指标，可以单位可以看作像素。

PD:红外小目标检测中检测率
    检测率 = 正确检测的目标数/真实目标总数
    注：检测结果与图像中的真实目标有重叠（overlap pixels）是判断检测成功的一个标准。这意味着，如果检测结果的区域与真实目标的区域有交集，那么该检测就被视为成功。

FA:虚警率是指在所有检测结果中，错误地将非目标区域识别为目标的比例。
    虚警率 = 错误检测的目标数 / 非真实目标总数
    错误检测的目标数：指的是被算法错误识别为目标的非目标区域的数量。
    检测结果总数：指的是算法输出的所有检测结果的数量，包括正确检测的目标和错误检测的目标。


'''

# class PD_FA(object):
#     def __init__(self):
#         # print('Initializing PD_FA')
#         self.reset()
#
#
#
#     def reset(self):
#         self.false_detect = 0
#         self.true_detect = 0
#         self.background_area = 0
#         self.target_nums = 0
#
#
#
#     def update(self, pred, label):
#         pred = pred[0][0]
#         label = label[0][0]
#         max_pred= np.max(pred)
#         # max_label = np.max(label, axis=(2,3))
#         pred = pred / max_pred  # normalize output to 0-1
#         label = label.astype(np.uint8)
#
#         # analysis target number
#         num_labels, labels, _, centroids = cv2.connectedComponentsWithStats(label)
#
#         # assert num_labels > 1
#         if (num_labels <= 1):
#             return
#
#         # get masks and update background area and targets number
#         back_mask = labels == 0
#         tmp_back_area = np.sum(back_mask)
#         self.background_area += tmp_back_area
#         self.target_nums += (num_labels - 1)
#
#         pred_binary = pred > 0.5
#
#         tmp_false_detect = np.sum(np.logical_and(back_mask, pred_binary))
#         assert tmp_false_detect <= tmp_back_area
#         self.false_detect += tmp_false_detect
#
#         # update true detection, there maybe multiple targets
#         for t in range(1, num_labels):
#             target_mask = labels == t
#             self.true_detect += np.sum(np.logical_and(target_mask, pred_binary)) > 0
#
#     def get(self):
#         FA = self.false_detect / self.background_area  #
#         PD = self.true_detect / self.target_nums       #
#         return PD,FA
#
#
#     def get_all(self):
#         return self.false_detect, self.background_area, self.true_detect, self.target_nums
#



class PD_FA():
    def __init__(self, bins=10, size=256):
        self.bins = bins
        self.size = size
        self.reset()

    def reset(self):
        self.FA = np.zeros(self.bins + 1)
        self.PD = np.zeros(self.bins + 1)
        self.target = np.zeros(self.bins + 1)
        self.background_area = np.zeros(self.bins + 1)

    def update(self, pred, label):
        pred = pred[0][0]
        label = label[0][0]
        label = label.astype(np.uint8)

        # 分析目标数量
        num_labels, labels, _, _ = cv2.connectedComponentsWithStats(label)
        if num_labels <= 1:
            return

        # 获取背景掩码和目标数量
        back_mask = labels == 0
        tmp_back_area = np.sum(back_mask)
        tmp_target_nums = num_labels - 1

        for iBin in range(self.bins + 1):
            score_thresh = iBin * (1.0 / self.bins)
            pred_binary = pred > score_thresh

            # 更新误检
            tmp_false_detect = np.sum(np.logical_and(back_mask, pred_binary))

            # 更新正确检测
            tmp_true_detect = 0
            for t in range(1, num_labels):
                target_mask = labels == t
                if np.sum(np.logical_and(target_mask, pred_binary)) > 0:
                    tmp_true_detect += 1

            self.FA[iBin] += tmp_false_detect
            self.PD[iBin] += tmp_true_detect
            self.target[iBin] += tmp_target_nums
            self.background_area[iBin] += tmp_back_area

    def get(self, img_num):
        Final_FA = self.FA / self.background_area
        Final_PD = np.where(self.target != 0, self.PD / self.target, 0)
        return Final_FA, Final_PD

    def get_all(self):
        return self.FA, self.background_area, self.PD, self.target