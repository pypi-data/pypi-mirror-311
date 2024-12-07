import cv2
import json
import matplotlib.pyplot as plt
from azureml.core import Workspace, Model
import time
import os

def resize_image(img, target_width, target_height, interpolation=cv2.INTER_CUBIC):
    original_height, original_width = img.shape[:2]
    ratio_w = original_width / target_width
    ratio_h = original_height / target_height
    resized_img = cv2.resize(img, (target_width, target_height), interpolation=interpolation)
    return resized_img, ratio_w, ratio_h
    
def adjust_coordinates(bboxes, ratio_w, ratio_h):
    resized_bboxes = []
    for box in bboxes:
        x1, y1 = box[0]
        x2, y2 = box[1]
        x1_resized = x1 * ratio_w
        y1_resized = y1 * ratio_h
        x2_resized = x2 * ratio_w
        y2_resized = y2 * ratio_h
        resized_bboxes.append([[x1_resized, y1_resized], [x2_resized, y2_resized]])
    return resized_bboxes

class OCRDetector:
    def __init__(self, config_path, ocr_type=None):
        if config_path:
            self.config_loader(config_path, ocr_type)
        else:
            raise ValueError("Config_path has not been provided.")
        self.ocr_model = self.initialize_model()  

    def config_loader(self, config_path, ocr_type=None):
        if ocr_type:
            self.ocr_type = ocr_type
        else:
            with open(config_path, 'r') as f:
                data = json.load(f) 
                self.ocr_type = data["ocr_type"]
        with open(config_path, 'r') as f:
            data = json.load(f) 
            self.model_paths = data["model_paths"]
        self.model_path = self.model_paths[self.ocr_type]
        if not os.path.exists(self.model_path):
            if self.ocr_type=='easyocr':
                self.model_path = os.path.dirname(self.download_model_from_azure(self.model_path))
            else:
                self.model_path = self.download_model_from_azure(self.model_path)


    def download_model_from_azure(self, model_path):
        if self.ocr_type == "easyocr":
            model_azure_id = "text-det-easyocr-pretrained"
        elif self.ocr_type == "paddleocr":
            model_azure_id = "text-det-paddleocr-pretrained"
        else:
            raise ValueError("Unknown OCR Type.")
        from azureml.core.authentication import InteractiveLoginAuthentication
        interactive_auth = InteractiveLoginAuthentication()
        ws = Workspace(
            subscription_id="0feed943-d77c-41d7-b087-eba62f229479",
            resource_group="aiandml",
            workspace_name="AIandML",
            auth=interactive_auth
        )
        model = Model(ws, model_azure_id)
        if self.ocr_type=="easyocr":
            model_download_path = model.download(target_dir=model_path, exist_ok=True)
        else:
            model_download_path = model.download(target_dir="models", exist_ok=True)
        return model_download_path 

    def initialize_model(self):
        if self.ocr_type == "easyocr":
            from custom_easyocr.easyocr_custom_lib import Reader
            return Reader(['en'], model_storage_directory=self.model_path, gpu=True)
        elif self.ocr_type == "paddleocr":
            from custom_paddleocr.paddleocr_custom_lib import PaddleOCR
            return PaddleOCR(lang='en', det_model_dir=self.model_path, mode="det",
                             det_algorithm='DB', 
                             det_db_thresh=0.3, 
                             det_db_box_thresh=0.25,
                             det_db_unclip_ratio=1.5,
                             use_gpu=True,
                             det_max_candidates=10000,
                             det_db_min_area=3,
                             det_db_score_mode="fast",
                             use_dilation=False, 
                             merge_no_span_structure=False) 
        else:
            raise ValueError("Unknown OCR Type.(Choose easyocr/paddleocr)") 

    def detection(self, img, target_width=None, target_height=None):
        start = time.time()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        bboxes = []
        if target_width and target_height:
            img_rgb, ratio_w, ratio_h = resize_image(img_rgb, target_width, target_height)

        if self.ocr_type == 'easyocr':
            horizontal_list = self.ocr_model.detect(img_rgb, 
                text_threshold=0.5, 
                low_text=0.3,  
                link_threshold=0.4,
                ) 
            for box in horizontal_list[0]:  
                x_coords = box[::2]
                y_coords = box[1::2]
                x_min = min(x_coords)
                x_max = max(x_coords)
                y_min = min(y_coords)
                y_max = max(y_coords)
                bboxes.append([[x_min, y_min], [x_max, y_max]]) 

        elif self.ocr_type == 'paddleocr':
            result = self.ocr_model.ocr(img_rgb, det=True) 
            if not result[0]:
                raise ValueError("No text found on the image")
            for resp in result[0]:
                bboxes.append([resp[0], resp[2]])  
        else:
            raise ValueError("Unknown OCR Type.(Choose easyocr/paddleocr)")
        
        if target_width and target_height:
            bboxes = adjust_coordinates(bboxes, ratio_w, ratio_h)

        finish = time.time()
        print(f"Detection process took {finish - start} second(s)")
        return bboxes

def process_image(image_path, config_path, target_width=None, target_height=None, ocr_type=None): # if 'ocr_type' not specified = easyocr by default (in config)
    detector = OCRDetector(config_path, ocr_type)
    img = cv2.imread(image_path)
    result = detector.detection(img, target_width, target_height)
    return result

if __name__ == "__main__":
    config_path="config.json"
    image_path = "images/deepl.png"
    result = process_image(image_path, config_path=config_path,  target_width=1920, target_height=1080, ocr_type="easyocr")

    # Display how the bounding boxes look in the image
    plt.figure(figsize=(15, 15))
    img1 = cv2.imread(image_path)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img_with_boxes = img1.copy()

    for box in result:
        x1, y1 = box[0]
        x2, y2 = box[1]
        cv2.rectangle(img_with_boxes, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 1)

    plt.imshow(img_with_boxes)
    plt.show()