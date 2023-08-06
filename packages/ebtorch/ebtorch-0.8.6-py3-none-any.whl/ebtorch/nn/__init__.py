#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
#
# Copyright 2020-* Emanuele Ballarin <emanuele@ballarin.cc>
# All Rights Reserved. Unless otherwise explicitly stated.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ==============================================================================
#
# SPDX-License-Identifier: Apache-2.0
# Imports
from .architectures import ArgMaxLayer
from .architectures import beta_reco_bce
from .architectures import BinarizeLayer
from .architectures import CausalConv1d
from .architectures import FCBlock
from .architectures import FCBlockLegacy
from .architectures import GaussianReparameterizerSampler
from .architectures import pixelwise_bce_mean
from .architectures import pixelwise_bce_sum
from .architectures import SGRUHCell
from .conv2drp import BatchNorm2dRP
from .conv2drp import Conv2dRP
from .conv2drp import Dropout2dRP
from .conv2drp import patch_rp_train_network
from .convolutional_flatten import ConvolutionalFlattenLayer
from .coordconv import CoordConv1d
from .coordconv import CoordConv2d
from .coordconv import CoordConv3d
from .debuglayers import ProbePrintLayer
from .fieldtransform import FieldTransform
from .functional import field_transform
from .functional import mish
from .functional import mishpulse
from .functional import mishpulse_symmy
from .kwta import BrokenReLU
from .kwta import KWTA1d
from .kwta import KWTA2d
from .laplacenet import MultiSolvePoissonTensor
from .laplacenet import PoissonNetCifar
from .laplacenet import SolvePoisson
from .laplacenet import SolvePoissonTensor
from .lmu import LMUCell
from .mish import Mish
from .mish import mishlayer_init
from .mish import MishPulse
from .mish import MishPulseSymmY
from .nnsemble import NNEnsemble
from .reshapelayers import FlatChannelize2DLayer
from .reshapelayers import ReshapeLayer
from .serf import ScaledERF
from .serlu import SERLU
from .sinlu import SinLU
from .smelu import SmeLU
from .utils import *

# Deletions (from .)
del architectures
del conv2drp
del convolutional_flatten
del coordconv
del debuglayers
del fieldtransform
del kwta
del laplacenet
del lmu
del mish
del nnsemble
del reshapelayers
del serlu
del sinlu
del smelu
del serf

# Deletions (from .functional)
# del mish  # (already done by chance!)
# del serf  # (already done by chance!)

# Deletions (from .utils)
del AdverApply
del AutoClipper
del TA2ATAdapter
del argser_f
del argsink
del download_gdrive
del emplace_kv
del gather_model_repr
del model_reqgrad
del model_reqgrad_
del patchify_2d
del patchify_batch
del patchify_dataset
del store_repr_autohook
del store_repr_fx
del store_repr_hook
