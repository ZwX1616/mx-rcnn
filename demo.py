import argparse
import ast
import pprint
import cv2

import mxnet as mx
from mxnet.module import Module

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from data.bbox import im_detect
from data.loader import load_test, generate_batch
from data.vis import vis_detection
from net.model import load_param, check_shape

def box_to_rect(box_x, box_y, color, linewidth):
	return plt.Rectangle(
		(box_x[0], box_y[0]), box_x[1]-box_x[0], box_y[1]-box_y[0],
		fill=False, edgecolor=color, linewidth=linewidth)

# save the image with detections
def save_result(image,det,thresh,class_names):
	img=cv2.imread(image)
	# BGR to RGB
	b,g,r=cv2.split(img)
	img=cv2.merge([r,g,b])
	plt.imshow(img)
	pycolors=list(colors.cnames.keys())
	for [cls, conf, x1, y1, x2, y2] in det:
		if cls > 0 and conf > thresh:
			# print(class_names[int(cls)], conf, [x1, y1, x2, y2])
			box_x=[x1,x2]
			box_y=[y1,y2]
			cls_text = class_names[int(cls)]
			color=pycolors[int((ord(cls_text[-1])+ord(cls_text[-2]))*0.5)]
			rect = box_to_rect(box_x,box_y,color,1)
			plt.gca().add_patch(rect)
			plt.gca().text(box_x[0], box_y[0],cls_text,
					  color=color,
					  fontsize=10
					  )
	# plt.show()
	plt.savefig(image[:-4]+'_det.png', format='png')

def demo_net(sym, class_names, args):
	# print config
	print('called with args\n{}'.format(pprint.pformat(vars(args))))

	# setup context
	if args.gpu:
		ctx = mx.gpu(int(args.gpu))
	else:
		ctx = mx.cpu(0)

	# load single test
	im_tensor, im_info, im_orig = load_test(args.image, short=args.img_short_side, max_size=args.img_long_side,
											mean=args.img_pixel_means, std=args.img_pixel_stds)

	# generate data batch
	data_batch = generate_batch(im_tensor, im_info)

	# load params
	arg_params, aux_params = load_param(args.params, ctx=ctx)

	# produce shape max possible
	data_names = ['data', 'im_info']
	label_names = None
	data_shapes = [('data', (1, 3, args.img_long_side, args.img_long_side)), ('im_info', (1, 3))]
	label_shapes = None

	# check shapes
	check_shape(sym, data_shapes, arg_params, aux_params)

	# create and bind module
	mod = Module(sym, data_names, label_names, context=ctx)
	mod.bind(data_shapes, label_shapes, for_training=False)
	mod.init_params(arg_params=arg_params, aux_params=aux_params)

	# forward
	mod.forward(data_batch)
	rois, scores, bbox_deltas = mod.get_outputs()
	rois = rois[:, 1:]
	scores = scores[0]
	bbox_deltas = bbox_deltas[0]
	im_info = im_info[0]

	# decode detection
	det = im_detect(rois, scores, bbox_deltas, im_info,
					bbox_stds=args.rcnn_bbox_stds, nms_thresh=args.rcnn_nms_thresh,
					conf_thresh=args.rcnn_conf_thresh)

	# print out
	for [cls, conf, x1, y1, x2, y2] in det:
		if cls > 0 and conf > args.vis_thresh:
			print(class_names[int(cls)], conf, [x1, y1, x2, y2])

	# if vis
	if args.vis:
		vis_detection(im_orig, det, class_names, thresh=args.vis_thresh)

	save_result(args.image,det,0.5,class_names)
		
def parse_args():
	parser = argparse.ArgumentParser(description='Demonstrate a Faster R-CNN network',
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--network', type=str, default='resnet50', help='base network')
	parser.add_argument('--params', type=str, default='', help='path to trained model')
	parser.add_argument('--dataset', type=str, default='voc', help='training dataset')
	parser.add_argument('--image', type=str, default='', help='path to test image')
	parser.add_argument('--gpu', type=str, default='', help='gpu device eg. 0')
	parser.add_argument('--vis', action='store_true', default=False, help='display results')
	parser.add_argument('--vis-thresh', type=float, default=0.7, help='threshold display boxes')
	# faster rcnn params
	parser.add_argument('--img-short-side', type=int, default=600)
	parser.add_argument('--img-long-side', type=int, default=1000)
	parser.add_argument('--img-pixel-means', type=str, default='(0.0, 0.0, 0.0)')
	parser.add_argument('--img-pixel-stds', type=str, default='(1.0, 1.0, 1.0)')
	parser.add_argument('--rpn-feat-stride', type=int, default=16)
	parser.add_argument('--rpn-anchor-scales', type=str, default='(8, 16, 32)')
	parser.add_argument('--rpn-anchor-ratios', type=str, default='(0.5, 1, 2)')
	parser.add_argument('--rpn-pre-nms-topk', type=int, default=6000)
	parser.add_argument('--rpn-post-nms-topk', type=int, default=300)
	parser.add_argument('--rpn-nms-thresh', type=float, default=0.7)
	parser.add_argument('--rpn-min-size', type=int, default=16)
	parser.add_argument('--rcnn-num-classes', type=int, default=21)
	parser.add_argument('--rcnn-feat-stride', type=int, default=16)
	parser.add_argument('--rcnn-pooled-size', type=str, default='(14, 14)')
	parser.add_argument('--rcnn-batch-size', type=int, default=1)
	parser.add_argument('--rcnn-bbox-stds', type=str, default='(0.1, 0.1, 0.2, 0.2)')
	parser.add_argument('--rcnn-nms-thresh', type=float, default=0.3)
	parser.add_argument('--rcnn-conf-thresh', type=float, default=1e-3)
	args = parser.parse_args()
	args.img_pixel_means = ast.literal_eval(args.img_pixel_means)
	args.img_pixel_stds = ast.literal_eval(args.img_pixel_stds)
	args.rpn_anchor_scales = ast.literal_eval(args.rpn_anchor_scales)
	args.rpn_anchor_ratios = ast.literal_eval(args.rpn_anchor_ratios)
	args.rcnn_pooled_size = ast.literal_eval(args.rcnn_pooled_size)
	args.rcnn_bbox_stds = ast.literal_eval(args.rcnn_bbox_stds)
	return args


def get_voc_names(args):
	from imdb.pascal_voc import PascalVOC
	args.rcnn_num_classes = len(PascalVOC.classes)
	return PascalVOC.classes


def get_coco_names(args):
	from imdb.coco import coco
	args.rcnn_num_classes = len(coco.classes)
	return coco.classes


def get_vgg16_test(args):
	from net.symbol_vgg import get_vgg_test
	if not args.params:
		args.params = 'model/vgg16-0010.params'
	args.img_pixel_means = (123.68, 116.779, 103.939)
	args.img_pixel_stds = (1.0, 1.0, 1.0)
	args.net_fixed_params = ['conv1', 'conv2']
	args.rpn_feat_stride = 16
	args.rcnn_feat_stride = 16
	args.rcnn_pooled_size = (7, 7)
	return get_vgg_test(anchor_scales=args.rpn_anchor_scales, anchor_ratios=args.rpn_anchor_ratios,
						rpn_feature_stride=args.rpn_feat_stride, rpn_pre_topk=args.rpn_pre_nms_topk,
						rpn_post_topk=args.rpn_post_nms_topk, rpn_nms_thresh=args.rpn_nms_thresh,
						rpn_min_size=args.rpn_min_size,
						num_classes=args.rcnn_num_classes, rcnn_feature_stride=args.rcnn_feat_stride,
						rcnn_pooled_size=args.rcnn_pooled_size, rcnn_batch_size=args.rcnn_batch_size)


def get_resnet50_test(args):
	from net.symbol_resnet import get_resnet_test
	if not args.params:
		args.params = 'model/resnet50-0010.params'
	args.img_pixel_means = (0.0, 0.0, 0.0)
	args.img_pixel_stds = (1.0, 1.0, 1.0)
	args.rpn_feat_stride = 16
	args.rcnn_feat_stride = 16
	args.rcnn_pooled_size = (14, 14)
	return get_resnet_test(anchor_scales=args.rpn_anchor_scales, anchor_ratios=args.rpn_anchor_ratios,
						   rpn_feature_stride=args.rpn_feat_stride, rpn_pre_topk=args.rpn_pre_nms_topk,
						   rpn_post_topk=args.rpn_post_nms_topk, rpn_nms_thresh=args.rpn_nms_thresh,
						   rpn_min_size=args.rpn_min_size,
						   num_classes=args.rcnn_num_classes, rcnn_feature_stride=args.rcnn_feat_stride,
						   rcnn_pooled_size=args.rcnn_pooled_size, rcnn_batch_size=args.rcnn_batch_size,
						   units=(3, 4, 6, 3), filter_list=(256, 512, 1024, 2048))


def get_resnet101_test(args):
	from net.symbol_resnet import get_resnet_test
	if not args.params:
		args.params = 'ckpt/resnet101-0010.params'
	args.img_pixel_means = (0.0, 0.0, 0.0)
	args.img_pixel_stds = (1.0, 1.0, 1.0)
	args.rpn_feat_stride = 16
	args.rcnn_feat_stride = 16
	args.rcnn_pooled_size = (14, 14)
	return get_resnet_test(anchor_scales=args.rpn_anchor_scales, anchor_ratios=args.rpn_anchor_ratios,
						   rpn_feature_stride=args.rpn_feat_stride, rpn_pre_topk=args.rpn_pre_nms_topk,
						   rpn_post_topk=args.rpn_post_nms_topk, rpn_nms_thresh=args.rpn_nms_thresh,
						   rpn_min_size=args.rpn_min_size,
						   num_classes=args.rcnn_num_classes, rcnn_feature_stride=args.rcnn_feat_stride,
						   rcnn_pooled_size=args.rcnn_pooled_size, rcnn_batch_size=args.rcnn_batch_size,
						   units=(3, 4, 23, 3), filter_list=(256, 512, 1024, 2048))

def get_class_names(dataset, args):
	datasets = {
		'voc': get_voc_names,
		'coco': get_coco_names
	}
	if dataset not in datasets:
		raise ValueError("dataset {} not supported".format(dataset))
	return datasets[dataset](args)


def get_network(network, args):
	networks = {
		'vgg16': get_vgg16_test,
		'resnet50': get_resnet50_test,
		'resnet101': get_resnet101_test
	}
	if network not in networks:
		raise ValueError("network {} not supported".format(network))
	return networks[network](args)


def main():
	args = parse_args()
	class_names = get_class_names(args.dataset, args)
	sym = get_network(args.network, args)
	demo_net(sym, class_names, args)


if __name__ == '__main__':
	main()
