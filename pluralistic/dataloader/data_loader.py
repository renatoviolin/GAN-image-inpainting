from PIL import Image, ImageFile
import torchvision.transforms as transforms
import torch.utils.data as data
from .image_folder import make_dataset
from pluralistic.util import task
import random


class CreateDataset(data.Dataset):
    def __init__(self, opt):
        self.opt = opt
        # import ipdb; ipdb.set_trace()
        self.img_path = opt.img_file
        self.img_size = 1

        self.mask_path = opt.mask_file
        self.mask_size = 1

        self.transform = get_transform(opt)

    def __getitem__(self, index):
        img, img_path = self.load_img()
        mask = self.load_mask()

        return {'img': img, 'img_path': img_path, 'mask': mask}

    def __len__(self):
        return self.img_size

    def name(self):
        return "inpainting dataset"

    def load_img(self):
        # ImageFile.LOAD_TRUNCATED_IMAGES = True
        img_pil = Image.open(self.img_path).convert('RGB')
        img = self.transform(img_pil)
        img_pil.close()
        return img, self.img_path

    def load_mask(self):
        mask_pil = Image.open(self.mask_path).convert('RGB')
        size = mask_pil.size[0]
        if size > mask_pil.size[1]:
            size = mask_pil.size[1]
        mask_transform = transforms.Compose([
                                             
                                             transforms.ToTensor()
                                             ])
        mask = (mask_transform(mask_pil) == 0).float()
        mask_pil.close()
        return mask


def dataloader(opt):
    datasets = CreateDataset(opt)
    dataset = data.DataLoader(datasets, batch_size=opt.batchSize, shuffle=not opt.no_shuffle, num_workers=int(opt.nThreads))

    return dataset


def get_transform(opt):
    """Basic process to transform PIL image to torch tensor"""
    transform_list = []
    osize = [opt.loadSize[0], opt.loadSize[1]]
    fsize = [opt.fineSize[0], opt.fineSize[1]]
    if opt.isTrain:
        if opt.resize_or_crop == 'resize_and_crop':
            transform_list.append(transforms.Resize(osize))
            transform_list.append(transforms.RandomCrop(fsize))
        elif opt.resize_or_crop == 'crop':
            transform_list.append(transforms.RandomCrop(fsize))
        if not opt.no_augment:
            transform_list.append(transforms.ColorJitter(0.0, 0.0, 0.0, 0.0))
        if not opt.no_flip:
            transform_list.append(transforms.RandomHorizontalFlip())
        if not opt.no_rotation:
            transform_list.append(transforms.RandomRotation(3))
    else:
        transform_list.append(transforms.Resize(fsize))

    transform_list += [transforms.ToTensor()]

    return transforms.Compose(transform_list)
