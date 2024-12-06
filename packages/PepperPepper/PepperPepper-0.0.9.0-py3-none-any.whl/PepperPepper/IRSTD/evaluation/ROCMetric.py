from ...environment import np
from ...environment import cv2
from ...environment import plt
from ...environment import sklearn

'''
ROCMetric: ROC curve
    ROC曲线是一种用于评估二分类模型性能的图形工具。它通过绘制假阳性率（FPR）与真阳性率（TPR）之间的关系，帮助我们理解模型在不同阈值下的表现。
    TPR:也称为召回率（Recall），表示正确识别的正样本占所有实际正样本的比例。
    FPR:表示错误识别的负样本(本身是负样本确被认为正样本)占所有实际负样本的比例。
'''

class ROCMetric(object):
    def __init__(self, bins=100):
        self.bins = bins
        self.reset()

    def reset(self):
        self.false_detect = np.zeros(self.bins+1)
        self.true_detect = np.zeros(self.bins+1)
        self.background_area = 0
        self.target_nums = 0



    def update(self, pred, label):
        pred = pred / np.max(pred)  # normalize output to 0-1
        label = label.astype(np.uint8)

        # analysis target number
        num_labels, labels, _, centroids = cv2.connectedComponentsWithStats(label)

        #assert num_labels > 1
        if(num_labels <=1):
            return

        # get masks and update background area and targets number
        back_mask = labels == 0
        tmp_back_area = np.sum(back_mask)
        self.background_area += tmp_back_area
        self.target_nums += (num_labels - 1)

        for ibin in range(self.bins + 1):
            thre = ibin / self.bins
            pred_binary = pred >= thre

            # update false detection
            tmp_false_detect = np.sum(np.logical_and(back_mask, pred_binary))
            assert tmp_false_detect <= tmp_back_area
            self.false_detect[ibin] += tmp_false_detect

            # update true detection, there maybe multiple targets
            for t in range(1, num_labels):
                target_mask = labels == t
                self.true_detect[ibin] += np.sum(np.logical_and(target_mask, pred_binary)) > 0

    def get(self):
        fpr = self.false_detect / self.background_area  # X axis
        tpr = self.true_detect / self.target_nums       # Y axis
        return fpr, tpr, sklearn.metrics.auc(fpr, tpr)


    def get_all(self):
        return self.false_detect, self.background_area, self.true_detect, self.target_nums

