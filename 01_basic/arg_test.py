__author__ = 'binzhou'
__time__ = '20190116'

import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument('--train_path', action='store', dest='train_path',
                    help='Path to train data')
parser.add_argument('--dev_path', action='store', dest='dev_path',
                    help='Path to dev data')
parser.add_argument('--log-level', dest='log_level',
                    default='info',
                    help='Logging level.')

opt = parser.parse_args()
print(opt)

print('----------------------------------------')

LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=getattr(logging, opt.log_level.upper()))
# logging.info(opt)

if opt.train_path is not None:
	print(opt.train_path)
if opt.dev_path is not None:
	print(opt.dev_path)

print('done.')

