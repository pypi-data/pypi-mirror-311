import os
import sys

__dir__ = os.path.dirname(__file__)

sys.path.append(os.path.join(__dir__, ""))

import cv2
import numpy as np

from ppstructure.utility import init_args
from tools.infer.utility import str2bool, check_gpu
from tools.infer import predict_system
from ppocr.utils.logging import get_logger
from ppocr.utils.utility import alpha_to_color, binarize_img
from ppocr.utils.network import confirm_model_dir_url

SUPPORT_OCR_MODEL_VERSION = ["PP-OCRv3", "PP-OCRv4"]
SUPPORT_DET_MODEL = ["DB"]
DEFAULT_OCR_MODEL_VERSION = "PP-OCRv4"
BASE_DIR = os.path.expanduser("~/.paddleocr/")
MODEL_URLS = {
    "OCR": {
        "PP-OCRv4": {
            "det": {
                "en": {
                    "url": "https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_det_infer.tar",
                },
            },
        },
        "PP-OCRv3": {
            "det": {
                "en": {
                    "url": "https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_det_infer.tar",
                },
            },
        },
    },
}


logger = get_logger()

def parse_args(mMain=True):
    import argparse

    parser = init_args()
    parser.add_help = mMain
    parser.add_argument("--lang", type=str, default="en")
    parser.add_argument("--det", type=str2bool, default=True)
    parser.add_argument(
        "--ocr_version",
        type=str,
        choices=SUPPORT_OCR_MODEL_VERSION,
        default="PP-OCRv3",
        help="OCR Model version, the current model support list is as follows: "
        "PP-OCRv4/v3 Support Chinese and English detection and recognition model, and direction classifier model",
    )
    if mMain:
        return parser.parse_args()
    else:
        inference_args_dict = {}
        for action in parser._actions:
            inference_args_dict[action.dest] = action.default
        return argparse.Namespace(**inference_args_dict)

def parse_lang(lang):
    return "en" if lang == "en" else "ml"

def get_model_config(version, model_type, lang):
    if version not in MODEL_URLS["OCR"]:
        version = DEFAULT_OCR_MODEL_VERSION
    model_config = MODEL_URLS["OCR"][version].get(model_type, {}).get(lang)
    if not model_config:
        logger.error("Model configuration not found for lang {}".format(lang))
        sys.exit(-1)
    return model_config

def img_decode(content: bytes):
    np_arr = np.frombuffer(content, dtype=np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)

def check_img(img, alpha_color=(255, 255, 255)):
    if isinstance(img, bytes):
        img = img_decode(img)
    if isinstance(img, np.ndarray) and len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if isinstance(img, np.ndarray) and len(img.shape) == 3 and img.shape[2] == 4:
        img = alpha_to_color(img, alpha_color)
    return img


class PaddleOCR(predict_system.TextSystem):
    def __init__(self, **kwargs):
        """
        paddleocr package
        args:
            **kwargs: other params show in paddleocr --help
        """
        params = parse_args(mMain=False)
        params.__dict__.update(**kwargs)
        assert (
            params.ocr_version in SUPPORT_OCR_MODEL_VERSION
        ), "ocr_version must in {}, but get {}".format(
            SUPPORT_OCR_MODEL_VERSION, params.ocr_version
        )
        params.use_gpu = check_gpu(params.use_gpu)
        det_lang = parse_lang(params.lang)

        # init model dir
        det_model_config = get_model_config(params.ocr_version, "det", det_lang)
        params.det_model_dir, det_url = confirm_model_dir_url(
            params.det_model_dir,
            os.path.join(BASE_DIR, "whl", "det", det_lang),
            det_model_config["url"],
        )

        if params.det_algorithm not in SUPPORT_DET_MODEL:
            logger.error("det_algorithm must in {}".format(SUPPORT_DET_MODEL))
            sys.exit(0)

        logger.debug(params)
        # init det_model
        super().__init__(params)

    def ocr(
        self,
        img,
        det=True,
        bin=False,
        inv=False,
        alpha_color=(255, 255, 255),
        slice={},
    ):
        """
        OCR with PaddleOCR

        Args:
            img: Image for OCR. It can be an ndarray, img_path, or a list of ndarrays.
            det: Use text detection or not. If False, only text recognition will be executed. Default is True.
            bin: Binarize image to black and white. Default is False.
            inv: Invert image colors. Default is False.
            alpha_color: Set RGB color Tuple for transparent parts replacement. Default is pure white.
            slice: Use sliding window inference for large images. Both det and rec must be True. Requires int values for slice["horizontal_stride"], slice["vertical_stride"], slice["merge_x_thres"], slice["merge_y_thres"] (See doc/doc_en/slice_en.md). Default is {}.

        Raises:
            AssertionError: If the input image is not of type ndarray, list, str, or bytes.
            SystemExit: If det is True and the input is a list of images.
        """
        assert isinstance(img, (np.ndarray, list, str, bytes))
        img= check_img(img, alpha_color)
        imgs = [img]

        def preprocess_image(_image):
            _image = alpha_to_color(_image, alpha_color)
            if inv:
                _image = cv2.bitwise_not(_image)
            if bin:
                _image = binarize_img(_image)
            return _image

        ocr_res = []
        for img in imgs:
            img = preprocess_image(img)
            dt_boxes, elapse = self.text_detector(img)
            if dt_boxes.size == 0:
                ocr_res.append(None)
                continue
            tmp_res = [box.tolist() for box in dt_boxes]
            ocr_res.append(tmp_res)
        return ocr_res
