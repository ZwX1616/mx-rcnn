#!/usr/bin/env bash

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


# run this experiment with
# nohup bash script/vgg_voc00712.sh 0,1 &> vgg_voc0712.log &
# to use gpu 0,1 to train, gpu 0 to test and write logs to vgg_voc0712.log
gpu=${1:0:1}

export MXNET_CUDNN_AUTOTUNE_DEFAULT=0
export PYTHONUNBUFFERED=1

# python3.6 train_end2end.py --network vgg --dataset PascalVOC --cpu
python3.6 train_end2end.py --network vgg --dataset PascalVOC --gpu 0
# python3.6 test.py --gpu $gpu