import datetime as dt
import json, time

from utils import create_dataset
from cnn_train import train, evaluate
import models


####  Hyperparameters ####


config = {
    'name': 'no_noise',
    # training
    'lr': 8e-5,
    'decay': 1e-6,
    'relu_type': 'relu',
    'epochs': 250,
    'full_cycls_per_epoch': 8,
    'batch_size': 32,
    'lr_patience': 15,
    'stop_patience': 60,
    # data augmentation
    'hflip_prob': .5,
    'vflip_prob': .5,
    'rot90_prob': .999,
    'rot_prob': .16,
    'rotate_rg': 20,
    'shift_prob': .2,
    'shift_width_rg': .1,
    'shift_height_rg': .1,
    'zoom_prob': .3,
    'zoom_rg': (.6, 1.4),
    'noise_prob': .001,
    'noise_rg': .02,
    # model
    'use_meta': False,
    'model_fn': 'model0',
    # preprocessing
    'preproc_strat': 'band3',
    'inc_angle_fill': -1,
    'band3_op': 'lambda x1, x2: (x1+x2)/2',
    'soft_targets': False,
    'soft_val': 0.99,  # only if soft_targets = True, must be 0.5 < x <= 1.0
}


def runtime(start):
    end_time = time.time()
    sec_elapsed = end_time - start
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


if __name__ == '__main__':
    start = time.time()

    model_fn = getattr(models, config['model_fn'])
    model = model_fn(**config)
    model.summary()
    print('Model compiled after {}'.format(runtime(start)))

    tmp = dt.datetime.now().strftime("%Y-%m-%d-%H-%M")
    config['tmp'] = tmp
    config_name = '../config/config_{}_{}.json'.format(tmp, config['name'])
    print('Saving configuration file to: {}'.format(config_name), flush=True)
    with open(config_name, 'w') as f:
        json.dump(config, f, indent=4)

    labels, data, meta = create_dataset('train.json', True, **config)
    print('Data loaded after {}'.format(runtime(start)))

    dataset = (labels, data, meta)
    model = train(dataset, model, **config)
    print('Model trained after {}'.format(runtime(start)))

    idxs, test, test_meta = create_dataset('test.json', False, **config)
    dataset = (idxs, test, test_meta)
    evaluate(model, dataset, **config)
    print('Scriped successfully completed after {}'.format(runtime(start)))
