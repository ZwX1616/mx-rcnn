# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import numpy as np
from easydict import EasyDict as edict

config = edict()

config.DEBUG = True

# network related params
config.PIXEL_MEANS = np.array([103.939, 116.779, 123.68])
config.IMAGE_STRIDE = 0
config.RPN_FEAT_STRIDE = 16
config.RCNN_FEAT_STRIDE = 16
config.FIXED_PARAMS = ['conv1', 'conv2']
config.FIXED_PARAMS_SHARED = ['conv1', 'conv2', 'conv3', 'conv4', 'conv5']

# dataset related params
config.NUM_CLASSES = 14
config.SCALES = [(600, 1000)]  # first is scale (the shorter side); second is max size
config.ANCHOR_SCALES = (8, 16, 32)
config.ANCHOR_RATIOS = (0.5, 1, 2)
config.NUM_ANCHORS = len(config.ANCHOR_SCALES) * len(config.ANCHOR_RATIOS)

config.TRAIN = edict()

# R-CNN and RPN
# size of images for each device, 2 for rcnn, 1 for rpn and e2e
config.TRAIN.BATCH_IMAGES = 2
# e2e changes behavior of anchor loader and metric
config.TRAIN.END2END = False
# group images with similar aspect ratio
config.TRAIN.ASPECT_GROUPING = True

# R-CNN
# rcnn rois batch size
config.TRAIN.BATCH_ROIS = 128
# rcnn rois sampling params
config.TRAIN.FG_FRACTION = 0.25
config.TRAIN.FG_THRESH = 0.5
config.TRAIN.BG_THRESH_HI = 0.5
config.TRAIN.BG_THRESH_LO = 0.0
# rcnn bounding box regression params
config.TRAIN.BBOX_REGRESSION_THRESH = 0.5
config.TRAIN.BBOX_WEIGHTS = np.array([1.0, 1.0, 1.0, 1.0])

# RPN anchor loader
# rpn anchors batch size
config.TRAIN.RPN_BATCH_SIZE = 256
# rpn anchors sampling params
config.TRAIN.RPN_FG_FRACTION = 0.5
config.TRAIN.RPN_POSITIVE_OVERLAP = 0.7
config.TRAIN.RPN_NEGATIVE_OVERLAP = 0.3
config.TRAIN.RPN_CLOBBER_POSITIVES = False
# rpn bounding box regression params
config.TRAIN.RPN_BBOX_WEIGHTS = (1.0, 1.0, 1.0, 1.0)
config.TRAIN.RPN_POSITIVE_WEIGHT = -1.0

# used for end2end training
# RPN proposal
config.TRAIN.CXX_PROPOSAL = True
config.TRAIN.RPN_NMS_THRESH = 0.7
config.TRAIN.RPN_PRE_NMS_TOP_N = 12000
config.TRAIN.RPN_POST_NMS_TOP_N = 2000
config.TRAIN.RPN_MIN_SIZE = config.RPN_FEAT_STRIDE
# approximate bounding box regression
config.TRAIN.BBOX_NORMALIZATION_PRECOMPUTED = False
config.TRAIN.BBOX_MEANS = (0.0, 0.0, 0.0, 0.0)
config.TRAIN.BBOX_STDS = (0.1, 0.1, 0.2, 0.2)

config.TEST = edict()

# R-CNN testing
# use rpn to generate proposal
config.TEST.HAS_RPN = False
# size of images for each device
config.TEST.BATCH_IMAGES = 1

# RPN proposal
config.TEST.CXX_PROPOSAL = True
config.TEST.RPN_NMS_THRESH = 0.7
config.TEST.RPN_PRE_NMS_TOP_N = 6000
config.TEST.RPN_POST_NMS_TOP_N = 300
config.TEST.RPN_MIN_SIZE = config.RPN_FEAT_STRIDE

# RPN generate proposal
config.TEST.PROPOSAL_NMS_THRESH = 0.7
config.TEST.PROPOSAL_PRE_NMS_TOP_N = 20000
config.TEST.PROPOSAL_POST_NMS_TOP_N = 2000
config.TEST.PROPOSAL_MIN_SIZE = config.RPN_FEAT_STRIDE

# RCNN nms
config.TEST.NMS = 0.3

# # default settings
# default = edict()

# # default network
# default.network = 'vgg'
# default.pretrained = 'model/vgg16'
# default.pretrained_epoch = 0
# default.base_lr = 0.001
# # default dataset
# default.dataset = 'PascalVOC'
# default.image_set = '2007_train'
# default.test_image_set = '2012_test'
# default.root_path = 'data'
# default.dataset_path = 'data/VOCdevkit'
# # default training
# default.frequent = 20
# default.kvstore = 'device'
# # default e2e
# default.e2e_prefix = 'model/e2e'
# default.e2e_epoch = 10
# default.e2e_lr = default.base_lr
# default.e2e_lr_step = '7'
# # default rpn
# default.rpn_prefix = 'model/rpn'
# default.rpn_epoch = 8
# default.rpn_lr = default.base_lr
# default.rpn_lr_step = '6'
# # default rcnn
# default.rcnn_prefix = 'model/rcnn'
# default.rcnn_epoch = 8
# default.rcnn_lr = default.base_lr
# default.rcnn_lr_step = '6'

# network settings
network = edict()

network.vgg = edict()
# dataset config
network.vgg.NUM_CLASSES = 21
network.vgg.SCALES = [(600, 1000)]
network.vgg.ANCHOR_SCALES = (8, 16, 32)
network.vgg.ANCHOR_RATIOS = (0.5, 1, 2)
network.vgg.NUM_ANCHORS = len(network.vgg.ANCHOR_SCALES) * len(network.vgg.ANCHOR_RATIOS)
# model config
network.vgg.pretrained = './model/vgg16'
network.vgg.pretrained_epoch = 0
network.vgg.PIXEL_MEANS = np.array([103.939, 116.779, 123.68])
network.vgg.IMAGE_STRIDE = 0
network.vgg.RPN_FEAT_STRIDE = 16
network.vgg.RCNN_FEAT_STRIDE = 16
network.vgg.FIXED_PARAMS = ['conv1', 'conv2']
# network.vgg.FIXED_PARAMS = []
network.vgg.FIXED_PARAMS_SHARED = ['conv1', 'conv2', 'conv3', 'conv4', 'conv5']
network.vgg.base_lr = 0.001
network.vgg.dataset = 'PascalVOC'
network.vgg.image_set = '2012_train'
network.vgg.test_image_set = '2012_val'
network.vgg.root_path = '/mnt/ckpt/vgg-voc2012'
network.vgg.dataset_path = '/mnt/data/VOCdevkit'
network.vgg.frequent = 20
network.vgg.kvstore = 'device'
network.vgg.e2e_prefix = 'model/e2e'
network.vgg.e2e_epoch = 10
network.vgg.e2e_lr = 0.001
network.vgg.e2e_lr_step = '7'
network.vgg.rpn_prefix = 'model/rpn'
network.vgg.rpn_epoch = 8
network.vgg.rpn_lr = 0.001
network.vgg.rpn_lr_step = '6'
network.vgg.rcnn_prefix = 'model/rcnn'
network.vgg.rcnn_epoch = 8
network.vgg.rcnn_lr = 0.001
network.vgg.rcnn_lr_step = '6'

network.resnet = edict()
# network.resnet.pretrained = 'model/resnet-101'
network.resnet.pretrained = 'model/resnet-50'
network.resnet.pretrained_epoch = 0
network.resnet.PIXEL_MEANS = np.array([0, 0, 0])
network.resnet.IMAGE_STRIDE = 0
network.resnet.RPN_FEAT_STRIDE = 16
network.resnet.RCNN_FEAT_STRIDE = 16
network.resnet.FIXED_PARAMS = ['conv0', 'stage1', 'gamma', 'beta']
network.resnet.FIXED_PARAMS_SHARED = ['conv0', 'stage1', 'stage2', 'stage3', 'gamma', 'beta']

# dataset settings
dataset = edict()

dataset.PascalVOC = edict()

dataset.coco = edict()
dataset.coco.dataset = 'coco'
dataset.coco.image_set = 'train2017'
dataset.coco.test_image_set = 'val2017'
dataset.coco.root_path = '/data'
dataset.coco.dataset_path = 'data/coco'
dataset.coco.NUM_CLASSES = 81

dataset.fashionai_kp = edict()
dataset.fashionai_kp.dataset = 'fashionai_kp'
dataset.fashionai_kp.image_set = 'train'
dataset.fashionai_kp.test_image_set = 'test'
# default config
dataset.fashionai_kp.NUM_CLASSES = 6
dataset.fashionai_kp.SCALES = [(312, 512)]  # first is scale (the shorter side); second is max size
dataset.fashionai_kp.ANCHOR_SCALES = (8, 16, 32)
dataset.fashionai_kp.ANCHOR_RATIOS = (0.5, 1, 2)
dataset.fashionai_kp.NUM_ANCHORS = len(dataset.fashionai_kp.ANCHOR_SCALES) * len(dataset.fashionai_kp.ANCHOR_RATIOS)
# training config list
dataset.fashionai_kp.vis = True
dataset.fashionai_kp.base_lr = 0.005
dataset.fashionai_kp.root_path = '/mnt/data/build'
dataset.fashionai_kp.dataset_path = '/mnt/data/base_dataset'
dataset.fashionai_kp.frequent = 20
dataset.fashionai_kp.kvstore = 'device'
dataset.fashionai_kp.e2e_prefix = '/mnt/models/e2e-coco'
dataset.fashionai_kp.e2e_epoch = 10
dataset.fashionai_kp.e2e_lr = 0.001
dataset.fashionai_kp.e2e_lr_step = '7'
dataset.fashionai_kp.rpn_prefix = '/mnt/models/rpn'
dataset.fashionai_kp.rpn_epoch = 8
dataset.fashionai_kp.rpn_lr = 0.001
dataset.fashionai_kp.rpn_lr_step = '6'
dataset.fashionai_kp.rcnn_prefix = '/mnt/models/rcnn'
dataset.fashionai_kp.rcnn_epoch = 8
dataset.fashionai_kp.rcnn_lr = 0.001
dataset.fashionai_kp.rcnn_lr_step = '6'

def generate_config(_network, _dataset):
    for k, v in network[_network].items():
        config[k] = v
    for k, v in dataset[_dataset].items():
        config[k] = v
