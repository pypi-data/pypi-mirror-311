from pathlib import Path
import os
import numpy as np

from midap.utils import get_inheritors
from midap.segmentation import *
from midap.segmentation import base_segmentator
from midap.apps import segment_cells

class_instance = "UNetSegmentation"
path_model_weights = "/Users/franziskaoschmann/Documents/midap/model/weights"
postprocessing = True
network_name = "model_weights_All-Celltypes.h5"
img_threshold = 255

# get the Predictor
pred = class_instance(
    path_model_weights=path_model_weights,
    postprocessing=postprocessing,
    model_weights=network_name,
    img_threshold=img_threshold,
)

# run the stack if we want to
# pred.run_image_stack(path_channel, clean_border)
