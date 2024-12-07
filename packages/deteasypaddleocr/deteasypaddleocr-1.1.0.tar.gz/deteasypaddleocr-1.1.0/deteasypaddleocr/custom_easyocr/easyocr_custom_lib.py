from .utils import calculate_md5, download_and_unzip, reformat_input

from .config import *
import torch
import os
import sys
from logging import getLogger

if sys.version_info[0] == 2:
    from io import open
    from six.moves.urllib.request import urlretrieve
    from pathlib2 import Path
else:
    from urllib.request import urlretrieve
    from pathlib import Path

from logging import getLogger
LOGGER = getLogger(__name__)

class Reader(object):
    def __init__(self, lang_list, gpu=True, model_storage_directory=None,
                 user_network_directory=None, detect_network="craft", 
                 download_enabled=True, 
                 detector=True, verbose=True, 
                 quantize=True, cudnn_benchmark=False):
        self.verbose = verbose
        self.download_enabled = download_enabled

        self.model_storage_directory = MODULE_PATH + '/model'
        if model_storage_directory:
            self.model_storage_directory = model_storage_directory
        Path(self.model_storage_directory).mkdir(parents=True, exist_ok=True)

        self.user_network_directory = MODULE_PATH + '/user_network'
        if user_network_directory:
            self.user_network_directory = user_network_directory
        Path(self.user_network_directory).mkdir(parents=True, exist_ok=True)
        sys.path.append(self.user_network_directory)

        if gpu is False:
            self.device = 'cpu'
            if verbose:
                LOGGER.warning('Using CPU. Note: This module is much faster with a GPU.')
        elif gpu is True:
            if torch.cuda.is_available():
                self.device = 'cuda'
            elif torch.backends.mps.is_available():
                self.device = 'mps'
            else:
                self.device = 'cpu'
                if verbose:
                    LOGGER.warning('Neither CUDA nor MPS are available - defaulting to CPU. Note: This module is much faster with a GPU.')
        else:
            self.device = gpu

        self.detection_models = detection_models

        # check and download detection model
        self.support_detection_network = ['craft', 'dbnet18']
        self.quantize=quantize, 
        self.cudnn_benchmark=cudnn_benchmark
        if detector:
            detector_path = self.getDetectorPath(detect_network)
        if detector:
            self.detector = self.initDetector(detector_path)
    
    def getDetectorPath(self, detect_network):
        if detect_network in self.support_detection_network:
            self.detect_network = detect_network
            if self.detect_network == 'craft':
                from .detection import get_detector, get_textbox
            elif self.detect_network in ['dbnet18']:
                from .detection_db import get_detector, get_textbox
            else:
                raise RuntimeError("Unsupport detector network. Support networks are craft and dbnet18.")
            self.get_textbox = get_textbox
            self.get_detector = get_detector
            corrupt_msg = 'MD5 hash mismatch, possible file corruption'
            detector_path = os.path.join(self.model_storage_directory, self.detection_models[self.detect_network]['filename'])
            if os.path.isfile(detector_path) == False:
                if not self.download_enabled:
                    raise FileNotFoundError("Missing %s and downloads disabled" % detector_path)
                LOGGER.warning('Downloading detection model, please wait. '
                               'This may take several minutes depending upon your network connection.')
                download_and_unzip(self.detection_models[self.detect_network]['url'], self.detection_models[self.detect_network]['filename'], self.model_storage_directory, self.verbose)
                assert calculate_md5(detector_path) == self.detection_models[self.detect_network]['md5sum'], corrupt_msg
                LOGGER.info('Download complete')
            elif calculate_md5(detector_path) != self.detection_models[self.detect_network]['md5sum']:
                if not self.download_enabled:
                    raise FileNotFoundError("MD5 mismatch for %s and downloads disabled" % detector_path)
                LOGGER.warning(corrupt_msg)
                os.remove(detector_path)
                LOGGER.warning('Re-downloading the detection model, please wait. '
                               'This may take several minutes depending upon your network connection.')
                download_and_unzip(self.detection_models[self.detect_network]['url'], self.detection_models[self.detect_network]['filename'], self.model_storage_directory, self.verbose)
                assert calculate_md5(detector_path) == self.detection_models[self.detect_network]['md5sum'], corrupt_msg
        else:
            raise RuntimeError("Unsupport detector network. Support networks are {}.".format(', '.join(self.support_detection_network)))
        
        return detector_path

    def initDetector(self, detector_path):
        return self.get_detector(detector_path, 
                                 device = self.device, 
                                 quantize = self.quantize, 
                                 cudnn_benchmark = self.cudnn_benchmark
                                 )
    
    def setDetector(self, detect_network):
        detector_path = self.getDetectorPath(detect_network)
        self.detector = self.initDetector(detector_path)




    def detect(self, img, text_threshold = 0.7, low_text = 0.4,\
               link_threshold = 0.4,
               reformat=True, optimal_num_chars=None,
               threshold = 0.2, bbox_min_score = 0.2, bbox_min_size = 3, max_candidates = 0,
               ):

        if reformat:
            img, img_cv_grey = reformat_input(img)

        horizontal_list = self.get_textbox(self.detector, 
                                    img,
                                    text_threshold = text_threshold, 
                                    link_threshold = link_threshold, 
                                    low_text = low_text,
                                    poly = False, 
                                    device = self.device, 
                                    optimal_num_chars = optimal_num_chars,
                                    threshold = threshold, 
                                    bbox_min_score = bbox_min_score, 
                                    bbox_min_size = bbox_min_size, 
                                    max_candidates = max_candidates,
                                    )

        return horizontal_list