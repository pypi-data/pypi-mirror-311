from ...environment import os, time, datetime,tqdm,np, argparse, torch
from ..evaluation import *
from ..datasets import *
from ..models import *
from ..RPCANet import *






def parse_args():
    # Setting parameters
    parser = argparse.ArgumentParser(description='Implement of RPCANet_train')
    parser.add_argument('--img_size', type=int, default=256, help='base size of images')
    parser.add_argument('--data_dir', type=str, default='/mnt/e/algorithms/IRSTD/dataset/IRSTD-1k', help='datasets path')
    parser.add_argument('--dataset', type=str, default='IRSTD-1k', help='dataset')


    parser.add_argument('--epochs', type=int, default=400, help='number of epochs')
    parser.add_argument('--batch_size', type=int, default=8, help='batch size')
    parser.add_argument('--lr', type=float, default=1e-4, help='learning rate')
    parser.add_argument('--gpu', type=str, default='0', help='GPU number')
    parser.add_argument('--mode', type=str, default='train')
    parser.add_argument('--lr_scheduler', type=str, default='poly', help='learning rate scheduler')
    parser.add_argument('--save-iter-step', type=int, default=1, help='save model per step iters')
    # parser.add_argument('--model', type=str, default='RPCANet')

    parser.add_argument('--save_iter_step', type=int, default=1, help='save model per step iters')
    parser.add_argument('--log_per_iter', type=int, default=1, help='interval of logging')
    parser.add_argument('--base_dir', type=str, default='../result/', help='saving dir')


    args = parser.parse_args()

    # Save folders
    #args.base_dir = r'D:\WFY\dun_irstd\result'
    args.time_name = time.strftime('%Y%m%dT%H-%M-%S', time.localtime(time.time()))
    args.folder_name = '{}_{}_{}'.format('RPCANet', args.dataset, args.time_name)
    args.save_folder = os.path.join(args.base_dir, args.folder_name)


    return args




class Trainer(object):
    def __init__(self, args):
        self.args = args
        self.iter_num = 0
        self.mode = args.mode

        # datasets
        self.train_loader = load_datasets(mode='train', img_size=args.img_size, data_dir=args.data_dir, batch_size=args.batch_size, shuffle=True, transform=None)
        self.val_loader = load_datasets(mode='val', img_size=args.img_size, data_dir=args.data_dir, batch_size=1, shuffle=True, transform=None)
        self.test_loader = load_datasets(mode='test', img_size=args.img_size, data_dir=args.data_dir, batch_size=1, shuffle=True, transform=None)
        self.iter_per_epoch = len(self.train_loader)
        self.max_iter = args.epochs * self.iter_per_epoch


        # GPU
        if torch.cuda.is_available():
            os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu
        self.device = torch.device("cuda:{}".format(args.gpu) if torch.cuda.is_available() else "cpu")

        self.net = RPCANet()
        self.net.to(self.device)

        self.softiou = SoftLoULoss()
        self.mse = torch.nn.MSELoss()

        ## lr scheduler
        self.scheduler = LR_Scheduler_Head(args.lr_scheduler, args.lr,
                                           args.epochs, len(self.train_loader), lr_step=10)

        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=args.lr)

        self.metric = SegmentationMetricTPFNFP(nclass=1)

        self.best_miou = 0
        self.best_fmeasure = 0
        self.eval_loss = 0  # tmp values
        self.miou = 0
        self.fmeasure = 0
        self.eval_PD_FA = PD_FA()

    def training(self):
        # training step
        start_time = time.time()
        base_log = "Epoch-Iter: [{:d}/{:d}]-[{:d}/{:d}] || Lr: {:.6f} || Loss: {:.4f} || " \
                   "Cost Time: {} || Estimated Time: {}"


        for epoch in range(self.args.epochs):
            tbar = tqdm.tqdm(self.train_loader)
            self.net.train()
            for i, (data, mask) in enumerate(tbar):
                self.scheduler(self.optimizer, i, epoch, self.best_miou)
                data, mask = data.to(self.device), mask.to(self.device)

                out_D, out_T = self.net(data)

                loss_softiou = self.softiou(out_T, mask)

                loss_mse = self.mse(out_D, data)

                gamma = torch.Tensor([0.1]).to(self.device)


                loss_all = loss_softiou + torch.mul(gamma, loss_mse)

                self.optimizer.zero_grad()
                loss_all.backward()
                self.optimizer.step()

                self.iter_num += 1

                cost_string = str(datetime.timedelta(seconds=int(time.time() - start_time)))
                eta_seconds = ((time.time() - start_time) / self.iter_num) * (self.max_iter - self.iter_num)
                eta_string = str(datetime.timedelta(seconds=int(eta_seconds)))

                tbar.set_description(f'Epoch-Iter: [{epoch+1:d}/{self.args.epochs:d}] || Loss: {loss_all.item():.4f}')

            self.validation()


    def validation(self):
        self.metric.reset()
        self.eval_PD_FA.reset()
        self.net.eval()
        # base_log = "Data: {:s}, mIoU: {:.4f}/{:.4f}, F1: {:.4f}/{:.4f} "
        # base_log = "Mode:{:s}, Data: {:s}, mIoU: {:.4f}/{:.4f}, F1: {:.4f}/{:.4f}, Pd:{:.4f}, Fa:{:.8f} "
        if self.args.mode == 'train':
            tbar = tqdm.tqdm(self.val_loader)
            # data_loader = self.val_loader
        elif self.args.mode == 'test':
            # data_loader = self.test_loader
            tbar = tqdm.tqdm(self.test_loader)
        else:
            raise NotImplementedError




        for i, (data, labels) in enumerate(tbar):
            with torch.no_grad():
                out_D, out_T = self.net(data.to(self.device))
            out_D, out_T = out_D.cpu(), out_T.cpu()

            self.metric.update(labels.detach().numpy(), out_T.detach().numpy())
            self.eval_PD_FA.update(out_T.detach().numpy(), labels.detach().numpy())

            miou, prec, recall, fmeasure = self.metric.get()
            PD, FA = self.eval_PD_FA.get()
            tbar.set_description(f'mIoU: {miou:.4f}/{self.best_miou:.4f}, F1: {fmeasure:.4f}/{self.best_fmeasure:.4f}, Pd:{PD:.4f}, Fa:{FA:.8f}')




        miou, prec, recall, fmeasure = self.metric.get()
        PD, FA = self.eval_PD_FA.get()

        if self.mode == 'train':
            torch.save(self.net.state_dict(), os.path.join(self.args.save_folder, 'latest.pkl'))
            if miou > self.best_miou:
                self.best_miou = miou
                torch.save(self.net.state_dict(), os.path.join(self.args.save_folder, 'best.pkl'))
            if fmeasure > self.best_fmeasure:
                self.best_fmeasure = fmeasure

            with open(os.path.join(self.args.save_folder, 'metric_train.txt'), 'a') as f:
                f.write('{} - {:04d}\t - IoU {:.4f}\t - PD {:.4f}\t - FA {:.4f}\n'.format(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())),
                                                                                          int(self.iter_num / self.iter_per_epoch) + 1, self.best_miou, PD, FA * 1000000))
        elif self.mode == 'test':
            with open(os.path.join(self.args.save_folder, 'metric_test.txt'), 'a') as f:
                f.write('{} - {:04d}\t - IoU {:.4f}\t - PD {:.4f}\t - FA {:.4f}\n'.format(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())),
                                int(self.iter_num / self.iter_per_epoch) + 1, self.best_miou, PD, FA * 1000000))





# if __name__ == '__main__':
#     args = parse_args()
#
#
#     trainer = Trainer(args)
#     trainer.training()
#
#     print('Best mIoU: %.5f, Best Fmeasure: %.5f\n\n' % (trainer.best_miou, trainer.best_fmeasure))