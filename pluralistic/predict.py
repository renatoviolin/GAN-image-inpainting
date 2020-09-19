from .options import test_options
from .dataloader import data_loader
from .model import create_model
from .util import visualizer
from itertools import islice
from types import SimpleNamespace

opt = SimpleNamespace()
opt.name = 'places2_random'
opt.model = 'pluralistic'
opt.ntest = 1
opt.how_many = 1
opt.phase = 'test'
opt.nsampling = 6
opt.save_number = 1
opt.mask_type = [3]
opt.checkpoints_dir = './pluralistic/checkpoints'
opt.which_iter = 'latest'
opt.gpu_ids = []
opt.loadSize = [276, 276]
opt.fineSize = [256, 256]
opt.resize_or_crop = 'resize_and_crop'
opt.no_flip = False
opt.no_rotation = True
opt.no_augment = True
opt.batchSize = 1
opt.nThreads = 1
opt.no_shuffle = True
opt.display_winsize = 256
opt.display_id = 1
opt.display_port = 8097
opt.display_single_pane_ncols = 0
opt.isTrain = False
opt.output_scale = 4

model = create_model(opt)
model.eval()


def run_fill(input_path, mask_path, output_path):
    opt.img_file = input_path
    opt.mask_file = mask_path
    opt.results_dir = output_path
    dataset = data_loader.dataloader(opt)
    dataset_size = len(dataset) * opt.batchSize
    data = iter(dataset).__next__()
    model.set_input(data)
    return model.test('plural')
